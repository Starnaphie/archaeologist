import aws_cdk as cdk
from stacks.pipeline_stack import PipelineStack
from stacks.api_stack import ApiStack

app = cdk.App()

pipeline = PipelineStack(
    app,
    "ResearchToDeckPipeline",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1",
    ),
)

ApiStack(
    app,
    "ResearchToDeckApi",
    state_machine=pipeline.state_machine,
    orchestrator_fn=pipeline.orchestrator_fn,
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1",
    ),
)

app.synth()
