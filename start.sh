#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
  echo "Shutting down…"
  jobs -p | xargs -r kill 2>/dev/null || true
}
trap cleanup EXIT INT TERM

(
  cd "$ROOT"
  exec lambdas/archaeologist/venv/bin/python -m uvicorn lambdas.archaeologist.main:app --reload
) &

(
  cd "$ROOT/frontend"
  exec npm run dev
) &

wait
