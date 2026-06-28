# archaeologist

A multi-agent pipeline that analyzes a GitHub repository and generates a downloadable slide deck — end to end, no human in the loop.

## What it does

Submit a GitHub URL and a presentation topic → the pipeline researches the repo, summarizes findings, generates a `.pptx`, and returns a presigned download URL.
User (browser)

│

▼

API Gateway (POST /generate)

│

▼

Step Functions State Machine

├── Archaeologist Lambda   (repo analysis → findings.json → S3)

├── Summarizer Lambda      (findings → outline.json → S3)

├── Slides Lambda          (outline → deck.pptx → S3)

└── URL Generator Lambda   (presigned URL → returned to user)

## Project structure
lambdas/

archaeologist/   Repo analysis agent (LangChain, FAISS, OpenAI)

summarizer/      Findings → slide outline (4-pass GPT-4o pipeline)

slides/          Outline → .pptx (python-pptx, layout builders)

url_generator/   Presigned S3 URL generator

orchestrator/    Step Functions trigger (API Gateway entry point)

status/          Execution status poller (frontend polls this)

shared/          S3 I/O, schemas, validation (shared across all Lambdas)

evals/             Eval suite for archaeologist and slides pipeline

infra/             AWS CDK stacks (Step Functions, Lambda, S3, API Gateway)

frontend/          React/Vite UI with Analyze, README, and Slides modes

## Local setup

```bash
# 1. Clone and create venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# 3. Configure environment
cp .env.example .env
# Fill in OPENAI_API_KEY in .env

# 4. Start local dev servers
bash start.sh
```

Runs the archaeologist FastAPI backend on `http://localhost:8000` and the Vite frontend on `http://localhost:5173`.

## Eval suite

```bash
# Smoke test (no API calls)
python -m evals.smoke_test

# Slides pipeline eval
python -m evals.run_evals --mode pipeline --topic "RAG" --audience "engineers"

# Archaeologist eval
python -m evals.run_evals --mode archaeologist --repo-root .

# Tool selection eval
python -m evals.run_evals --mode tool-calls
```

## Deploy to AWS

See [infra/DEPLOY.md](infra/DEPLOY.md).

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for all LLM calls |
| `PIPELINE_BUCKET` | Yes (AWS) | S3 bucket name provisioned by CDK |
| `AWS_REGION` | No | AWS region (default: us-east-1) |
| `S3_ENDPOINT_URL` | No | LocalStack endpoint for local testing |
