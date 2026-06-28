## Eval Suite

### Modes
- `archaeologist` — evaluates repo analysis agent steps against a local repo
- `pipeline` — evaluates the 4-pass slide generation pipeline against a topic
- `both` — runs both in sequence and prints a combined report with grand totals
- `tool-calls` — tests whether the revision agent selects the correct tool for 18 natural-language instructions

### Usage

```bash
# Archaeologist only
python -m evals.run_evals --mode archaeologist --repo-root /path/to/repo

# Pipeline only
python -m evals.run_evals --mode pipeline --topic "Serverless Architecture" --audience "senior engineers" --tone professional

# Both
python -m evals.run_evals --mode both --repo-root /path/to/repo --topic "Serverless Architecture" --audience "senior engineers"

# Tool call evals only
python -m evals.run_evals --mode tool-calls

# Optional pipeline flags
--tone casual|professional|academic
--description "Additional context about the topic"
--num-slides 10   # cap slide count; omit for auto (max 20)

# Smoke test (no API calls)
python -m evals.smoke_test
```

### Output columns
| Column | Description |
|--------|-------------|
| Step | Name of the instrumented step |
| Runtime (s) | Wall clock time including I/O and network |
| Compute (s) | CPU time only — excludes network wait |
| Prompt Tokens | Tokens sent to the model |
| Completion Tokens | Tokens returned by the model |
| Total Tokens | Sum — use this for cost estimation |
| Status | OK or FAILED |
