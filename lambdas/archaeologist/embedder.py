import os
from pathlib import Path
from typing import List

import faiss
import numpy as np
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent / ".env")

EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536
BATCH_SIZE = 100
MAX_TOKENS_PER_TEXT = 8000
TOKEN_ENCODER = tiktoken.encoding_for_model(EMBED_MODEL)

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_index: faiss.IndexFlatL2 | None = None
_chunks: List[dict] = []


def _truncate_text(text: str, max_tokens: int = MAX_TOKENS_PER_TEXT) -> str:
    tokens = TOKEN_ENCODER.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        return TOKEN_ENCODER.decode(tokens)
    return text


def _embed_texts(texts: List[str]) -> np.ndarray:
    vectors: List[List[float]] = []
    truncated_texts = [_truncate_text(t) for t in texts]
    for start in range(0, len(truncated_texts), BATCH_SIZE):
        batch = truncated_texts[start:start + BATCH_SIZE]
        response = _client.embeddings.create(model=EMBED_MODEL, input=batch)
        vectors.extend(item.embedding for item in response.data)
    return np.asarray(vectors, dtype="float32")


def build_index(chunks: List[dict]) -> None:
    global _index, _chunks
    _index = faiss.IndexFlatL2(EMBED_DIM)
    _chunks = []

    if not chunks:
        return

    embeddings = _embed_texts([c["source"] for c in chunks])
    _index.add(embeddings)
    _chunks = list(chunks)


def retrieve(query: str, k: int = 10) -> List[dict]:
    if _index is None or _index.ntotal == 0:
        return []

    query_vec = _embed_texts([query])
    k = min(k, _index.ntotal)
    _, indices = _index.search(query_vec, k)
    return [_chunks[i] for i in indices[0] if 0 <= i < len(_chunks)]
