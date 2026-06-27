## Prerequisites
- AWS CLI configured: `aws configure`
- CDK bootstrapped: `cdk bootstrap aws://ACCOUNT_ID/us-east-1`
- Docker running (required for container image Lambdas)
- Node.js installed (required for CDK CLI)

## Store OpenAI API Key
```bash
aws secretsmanager create-secret \
  --name ResearchToDeck/OpenAIApiKey \
  --secret-string "sk-your-key-here"
```

## Deploy
```bash
cd infra
pip install -r requirements.txt
cdk synth          # verify template generates cleanly
cdk deploy --all   # deploys PipelineStack then ApiStack
```

## After deploy
CDK outputs these values — save them:
- `BucketName` — S3 bucket for pipeline artifacts
- `StateMachineArn` — Step Functions ARN
- `ApiUrl` — Base URL for API Gateway
- `GenerateEndpoint` — POST here to start a pipeline run
- `StatusEndpoint` — GET here with ?arn= to poll status

## Test the deployed API
```bash
# Start a pipeline run
curl -X POST https://YOUR_API_URL/prod/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Introduction to RAG", "repo_source": "https://github.com/owner/repo"}'

# Poll status (use execution_arn from response above)
curl "https://YOUR_API_URL/prod/status?arn=EXECUTION_ARN"
```

## Teardown
```bash
cdk destroy --all
```
Note: S3 bucket auto-deletes objects on destroy due to `auto_delete_objects=True`.
