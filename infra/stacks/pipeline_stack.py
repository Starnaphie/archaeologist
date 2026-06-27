import aws_cdk as cdk
from aws_cdk import (
    aws_s3 as s3,
    aws_sqs as sqs,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)
from constructs import Construct


class PipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ── S3 Bucket ─────────────────────────────────────────────────────
        # Stores findings.json, outline.json, deck.pptx per execution.
        # 7-day lifecycle keeps costs near zero.
        self.bucket = s3.Bucket(
            self,
            "PipelineBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            lifecycle_rules=[
                s3.LifecycleRule(
                    expiration=cdk.Duration.days(7),
                    id="ExpireExecutionArtifacts",
                )
            ],
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.GET],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                    max_age=3000,
                )
            ],
        )

        # ── SQS Dead Letter Queue ──────────────────────────────────────────
        # Captures failed Step Functions state payloads for inspection and replay.
        # 14-day retention gives enough time to diagnose and fix failures.
        self.dlq = sqs.Queue(
            self,
            "PipelineDLQ",
            queue_name="ResearchToDeckDLQ",
            retention_period=cdk.Duration.days(14),
            visibility_timeout=cdk.Duration.seconds(300),
        )

        shared_env = {
            "PIPELINE_BUCKET": self.bucket.bucket_name,
            "AWS_ACCOUNT_ID": self.account,
        }

        # ── Orchestrator Lambda ────────────────────────────────────────────────
        # Lightweight — only needs boto3 (built into runtime). Zip deployment.
        self.orchestrator_fn = lambda_.Function(
            self,
            "Orchestrator",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("../lambdas/orchestrator"),
            handler="handler.handler",
            timeout=cdk.Duration.seconds(30),
            memory_size=256,
            environment={
                **shared_env,
                # STATE_MACHINE_ARN injected after state machine is created below
            },
        )

        # ── Archaeologist Lambda ───────────────────────────────────────────────
        # Heavy: faiss, langchain, tiktoken. Container image via ECR.
        self.archaeologist_fn = lambda_.DockerImageFunction(
            self,
            "Archaeologist",
            code=lambda_.DockerImageCode.from_image_asset(
                "../lambdas/archaeologist",
                build_args={"PLATFORM": "linux/amd64"},
            ),
            timeout=cdk.Duration.seconds(300),
            memory_size=3008,
            ephemeral_storage_size=cdk.Size.mebibytes(2048),
            environment={
                **shared_env,
                "OPENAI_API_KEY": "PLACEHOLDER",  # injected via Secrets Manager in production
            },
        )

        # ── Summarizer Lambda ──────────────────────────────────────────────────
        # Medium: openai, python-pptx (for outline validation). Container image.
        self.summarizer_fn = lambda_.DockerImageFunction(
            self,
            "Summarizer",
            code=lambda_.DockerImageCode.from_image_asset(
                "../lambdas/summarizer",
                build_args={"PLATFORM": "linux/amd64"},
            ),
            timeout=cdk.Duration.seconds(300),
            memory_size=1024,
            environment={
                **shared_env,
                "OPENAI_API_KEY": "PLACEHOLDER",
            },
        )

        # ── Slides Lambda ──────────────────────────────────────────────────────
        # Medium: python-pptx. Container image.
        self.slides_fn = lambda_.DockerImageFunction(
            self,
            "Slides",
            code=lambda_.DockerImageCode.from_image_asset(
                "../lambdas/slides",
                build_args={"PLATFORM": "linux/amd64"},
            ),
            timeout=cdk.Duration.seconds(120),
            memory_size=1024,
            ephemeral_storage_size=cdk.Size.mebibytes(1024),
            environment={
                **shared_env,
                "OPENAI_API_KEY": "PLACEHOLDER",
            },
        )

        # ── URL Generator Lambda ───────────────────────────────────────────────
        # Lightweight — only needs boto3. Zip deployment.
        self.url_generator_fn = lambda_.Function(
            self,
            "URLGenerator",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("../lambdas/url_generator"),
            handler="handler.handler",
            timeout=cdk.Duration.seconds(30),
            memory_size=256,
            environment={
                **shared_env,
                "PRESIGNED_URL_EXPIRY_SECONDS": "3600",
            },
        )

        # ── S3 permissions ─────────────────────────────────────────────────────
        self.bucket.grant_read_write(self.archaeologist_fn)
        self.bucket.grant_read_write(self.summarizer_fn)
        self.bucket.grant_read_write(self.slides_fn)
        self.bucket.grant_read(self.url_generator_fn)

        # URL generator needs s3:GetObject for presigned URL generation
        self.url_generator_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[self.bucket.arn_for_objects("*")],
            )
        )

        # ── Step Functions task definitions ────────────────────────────────────
        # Each LambdaInvoke passes its full output as the input to the next state
        # via result_selector and result_path so the payload threads through cleanly.
        research = tasks.LambdaInvoke(
            self,
            "Research",
            lambda_function=self.archaeologist_fn,
            output_path="$.Payload",
            retry_on_service_exceptions=False,
        ).add_retry(
            max_attempts=2,
            interval=cdk.Duration.seconds(5),
            backoff_rate=2,
            errors=[
                "Lambda.ServiceException",
                "Lambda.AWSLambdaException",
                "Lambda.SdkClientException",
            ],
        ).add_catch(
            handler=self._make_failure_chain("Research"),
            errors=["States.ALL"],
            result_path="$.errorInfo",
        )

        summarize = tasks.LambdaInvoke(
            self,
            "Summarize",
            lambda_function=self.summarizer_fn,
            output_path="$.Payload",
            retry_on_service_exceptions=False,
        ).add_retry(
            max_attempts=2,
            interval=cdk.Duration.seconds(5),
            backoff_rate=2,
            errors=[
                "Lambda.ServiceException",
                "Lambda.AWSLambdaException",
                "Lambda.SdkClientException",
            ],
        ).add_catch(
            handler=self._make_failure_chain("Summarize"),
            errors=["States.ALL"],
            result_path="$.errorInfo",
        )

        generate = tasks.LambdaInvoke(
            self,
            "GenerateSlides",
            lambda_function=self.slides_fn,
            output_path="$.Payload",
            retry_on_service_exceptions=False,
        ).add_retry(
            max_attempts=2,
            interval=cdk.Duration.seconds(5),
            backoff_rate=2,
            errors=[
                "Lambda.ServiceException",
                "Lambda.AWSLambdaException",
                "Lambda.SdkClientException",
            ],
        ).add_catch(
            handler=self._make_failure_chain("Generate"),
            errors=["States.ALL"],
            result_path="$.errorInfo",
        )

        sign = tasks.LambdaInvoke(
            self,
            "SignURL",
            lambda_function=self.url_generator_fn,
            output_path="$.Payload",
            retry_on_service_exceptions=False,
        ).add_retry(
            max_attempts=3,
            interval=cdk.Duration.seconds(2),
            backoff_rate=2,
            errors=[
                "Lambda.ServiceException",
                "Lambda.AWSLambdaException",
                "Lambda.SdkClientException",
            ],
        ).add_catch(
            handler=self._make_failure_chain("Sign"),
            errors=["States.ALL"],
            result_path="$.errorInfo",
        )

        # ── State machine ──────────────────────────────────────────────────────
        chain = research.next(summarize).next(generate).next(sign)

        self.state_machine = sfn.StateMachine(
            self,
            "Pipeline",
            state_machine_name="ResearchToDeckPipeline",
            definition_body=sfn.DefinitionBody.from_chainable(chain),
            timeout=cdk.Duration.minutes(15),
            tracing_enabled=True,
        )

        # ── DLQ permission ─────────────────────────────────────────────────────
        self.dlq.grant_send_messages(self.state_machine)

        # ── Inject state machine ARN into orchestrator ─────────────────────────
        # Must happen after state machine is defined.
        self.orchestrator_fn.add_environment(
            "STATE_MACHINE_ARN",
            self.state_machine.state_machine_arn,
        )

        # ── Step Functions start permission for orchestrator ───────────────────
        self.state_machine.grant_start_execution(self.orchestrator_fn)

        # ── CloudFormation outputs ─────────────────────────────────────────────
        cdk.CfnOutput(self, "StateMachineArn", value=self.state_machine.state_machine_arn)
        cdk.CfnOutput(self, "StateMachineName", value=self.state_machine.state_machine_name)

        # Expose bucket name and DLQ URL as CloudFormation outputs
        cdk.CfnOutput(self, "BucketName", value=self.bucket.bucket_name)
        cdk.CfnOutput(self, "DLQUrl", value=self.dlq.queue_url)

        # ── Secrets Manager — OpenAI API Key ──────────────────────────────────
        # Store the real key with:
        #   aws secretsmanager create-secret --name ResearchToDeck/OpenAIApiKey --secret-string "sk-..."
        # CDK grants read access; the key is never hardcoded.
        openai_secret = secretsmanager.Secret.from_secret_name_v2(
            self,
            "OpenAISecret",
            secret_name="ResearchToDeck/OpenAIApiKey",
        )

        # Replace PLACEHOLDER environment variable with Secrets Manager value
        for fn in [self.archaeologist_fn, self.summarizer_fn, self.slides_fn]:
            # Remove the placeholder — add the real secret value
            fn.add_environment(
                "OPENAI_API_KEY",
                openai_secret.secret_value.unsafe_unwrap(),
            )
            # Grant read access so the Lambda can fetch it at runtime if needed
            openai_secret.grant_read(fn)

        # ── X-Ray tracing grants ───────────────────────────────────────────────
        # State machine already has tracing_enabled=True.
        # Each Lambda needs xray:PutTraceSegments and xray:PutTelemetryRecords.
        xray_policy = iam.PolicyStatement(
            actions=[
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords",
                "xray:GetSamplingRules",
                "xray:GetSamplingTargets",
            ],
            resources=["*"],
        )
        for fn in [
            self.orchestrator_fn,
            self.archaeologist_fn,
            self.summarizer_fn,
            self.slides_fn,
            self.url_generator_fn,
        ]:
            fn.add_to_role_policy(xray_policy)

    def _make_failure_chain(self, stage_name: str) -> sfn.IChainable:
        dlq_task = tasks.SqsSendMessage(
            self,
            f"NotifyFailure{stage_name}",
            queue=self.dlq,
            message_body=sfn.TaskInput.from_object(
                {
                    "execution_id.$": "$$.Execution.Name",
                    "failed_at": stage_name,
                    "error.$": "$.Error",
                    "cause.$": "$.Cause",
                    "input.$": "$$.Execution.Input",
                }
            ),
            result_path=sfn.JsonPath.DISCARD,
        )
        fail_state = sfn.Fail(
            self,
            f"Fail{stage_name}",
            error=f"{stage_name}Failed",
            cause="See DLQ for details",
        )
        return dlq_task.next(fail_state)
