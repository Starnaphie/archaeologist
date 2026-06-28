"""S3-backed deck registry. Reads deck.meta.json sidecar files written by the slides Lambda to provide a queryable index of all generated presentations and their source repos. Run as a script to print a summary of all decks in the pipeline bucket."""

import json
import logging

from botocore.exceptions import ClientError

from .s3_io import BUCKET, _get_client


logger = logging.getLogger(__name__)


def list_decks(bucket: str = "", max_results: int = 50) -> list[dict]:
    bucket = bucket or BUCKET
    if not bucket:
        raise ValueError("No bucket specified")

    client = _get_client()
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix="executions/",
        Delimiter="/",
    )

    results = []
    for prefix in response.get("CommonPrefixes", []):
        meta_key = f"{prefix['Prefix']}deck.meta.json"
        try:
            obj = client.get_object(Bucket=bucket, Key=meta_key)
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code == "NoSuchKey":
                continue
            raise

        body = obj["Body"].read().decode("utf-8")
        meta = json.loads(body)
        execution_id = meta_key.removeprefix("executions/").removesuffix(
            "/deck.meta.json"
        )
        meta["execution_id"] = execution_id
        results.append(meta)

    results.sort(key=lambda item: item.get("generated_at") or "", reverse=True)
    return results[:max_results]


def find_decks_by_repo(repo_source: str, bucket: str = "") -> list[dict]:
    decks = list_decks(bucket)
    normalized_repo_source = repo_source.rstrip("/")
    return [
        deck
        for deck in decks
        if deck.get("repo_source") == repo_source
        or deck.get("repo_source", "").rstrip("/") == normalized_repo_source
    ]


def get_deck_summary(bucket: str = "") -> dict:
    decks = list_decks(bucket, max_results=200)
    repos = sorted(
        {
            deck.get("repo_source", "")
            for deck in decks
            if deck.get("repo_source", "")
        }
    )
    layout_totals = {}
    for deck in decks:
        for layout, count in deck.get("layout_summary", {}).items():
            layout_totals[layout] = layout_totals.get(layout, 0) + count

    return {
        "total_decks": len(decks),
        "unique_repos": len(repos),
        "repos": repos,
        "most_recent": decks[0] if decks else None,
        "layout_totals": layout_totals,
    }


if __name__ == "__main__":
    import os
    import sys
    from pathlib import Path

    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    bucket = os.environ.get("PIPELINE_BUCKET", "")
    if not bucket:
        print("Set PIPELINE_BUCKET env var", file=sys.stderr)
        sys.exit(1)
    summary = get_deck_summary(bucket)
    print(json.dumps(summary, indent=2))
