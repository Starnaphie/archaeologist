import aws_cdk as cdk
from aws_cdk import (
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_stepfunctions as sfn,
)
from constructs import Construct


class ApiStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        state_machine: sfn.StateMachine,
        orchestrator_fn: lambda_.IFunction,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # -- Status Lambda -------------------------------------------------
        # Lightweight: only needs boto3. Zip deployment.
        self.status_fn = lambda_.Function(
            self,
            "StatusChecker",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("../lambdas/status"),
            handler="handler.handler",
            timeout=cdk.Duration.seconds(15),
            memory_size=256,
            environment={
                "AWS_ACCOUNT_ID": self.account,
                "AWS_REGION_NAME": self.region,
            },
        )

        self.status_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "xray:PutTraceSegments",
                    "xray:PutTelemetryRecords",
                ],
                resources=["*"],
            )
        )

        # Grant status Lambda permission to describe any execution.
        self.status_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["states:DescribeExecution"],
                resources=[
                    f"arn:aws:states:{self.region}:{self.account}:execution:{state_machine.state_machine_name}:*"
                ],
            )
        )

        # -- REST API ------------------------------------------------------
        self.api = apigw.RestApi(
            self,
            "ResearchToDeckApi",
            rest_api_name="ResearchToDeckApi",
            description="Research to deck pipeline API",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=[
                    "Content-Type",
                    "Authorization",
                    "X-Amz-Date",
                    "X-Api-Key",
                ],
            ),
            deploy_options=apigw.StageOptions(
                stage_name="prod",
                throttling_rate_limit=10,
                throttling_burst_limit=20,
                logging_level=apigw.MethodLoggingLevel.INFO,
                data_trace_enabled=False,
                metrics_enabled=True,
            ),
        )

        # -- POST /generate -----------------------------------------------
        # Routes to orchestrator Lambda which starts the Step Functions execution.
        generate_resource = self.api.root.add_resource("generate")
        generate_resource.add_method(
            "POST",
            apigw.LambdaIntegration(
                orchestrator_fn,
                proxy=True,
                allow_test_invoke=True,
            ),
            method_responses=[
                apigw.MethodResponse(status_code="202"),
                apigw.MethodResponse(status_code="400"),
                apigw.MethodResponse(status_code="500"),
            ],
        )

        # -- GET /status ---------------------------------------------------
        # Polls Step Functions via status Lambda. Frontend calls every 5s.
        status_resource = self.api.root.add_resource("status")
        status_resource.add_method(
            "GET",
            apigw.LambdaIntegration(
                self.status_fn,
                proxy=True,
                allow_test_invoke=True,
            ),
            method_responses=[
                apigw.MethodResponse(status_code="200"),
                apigw.MethodResponse(status_code="400"),
                apigw.MethodResponse(status_code="404"),
                apigw.MethodResponse(status_code="500"),
            ],
            request_parameters={
                "method.request.querystring.arn": True,
            },
        )

        # -- CloudFormation outputs ---------------------------------------
        cdk.CfnOutput(self, "ApiUrl", value=self.api.url)
        cdk.CfnOutput(self, "GenerateEndpoint", value=f"{self.api.url}generate")
        cdk.CfnOutput(self, "StatusEndpoint", value=f"{self.api.url}status")
