import asyncio
import json
import uuid
from dataclasses import asdict
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from . import agent, embedder, ingestion
from . import parser as code_parser

app = FastAPI(title="archaeologist")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPORTS: Dict[str, dict] = {}


class AnalyzeRequest(BaseModel):
    github_url: str


async def _run_pipeline(github_url: str, job_id: str):
    yield {"event": "job_id", "data": job_id}

    yield {"event": "progress", "data": "Cloning repo..."}
    manifest = await asyncio.to_thread(ingestion.clone_and_manifest, github_url)

    yield {"event": "progress", "data": f"Parsing {manifest['file_count']} files..."}
    parse_result = await asyncio.to_thread(code_parser.parse_manifest, manifest)

    yield {"event": "progress", "data": "Embedding chunks..."}
    await asyncio.to_thread(embedder.build_index, parse_result.chunks)

    yield {"event": "progress", "data": "Running analysis..."}
    report = await asyncio.to_thread(
        agent.generate_report, parse_result.symbol_map, manifest["temp_dir"]
    )

    report_dict = asdict(report)
    REPORTS[job_id] = report_dict
    yield {"event": "done", "data": json.dumps(report_dict)}


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    job_id = str(uuid.uuid4())
    return EventSourceResponse(_run_pipeline(req.github_url, job_id))


@app.get("/report/{job_id}")
async def get_report(job_id: str):
    if job_id not in REPORTS:
        raise HTTPException(status_code=404, detail="report not found")
    return REPORTS[job_id]
