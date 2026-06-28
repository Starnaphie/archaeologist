import sys


MODEL_COSTS = {
    "gpt-4o": {"input_per_1m": 2.50, "output_per_1m": 10.00},
    "gpt-4o-2024-08-06": {"input_per_1m": 2.50, "output_per_1m": 10.00},
    "gpt-4o-mini": {"input_per_1m": 0.15, "output_per_1m": 0.60},
    "gpt-4o-mini-2024-07-18": {"input_per_1m": 0.15, "output_per_1m": 0.60},
    "text-embedding-3-small": {"input_per_1m": 0.02, "output_per_1m": 0.0},
    "text-embedding-3-large": {"input_per_1m": 0.13, "output_per_1m": 0.0},
}


def _lookup_cost(model: str) -> dict | None:
    if model in MODEL_COSTS:
        return MODEL_COSTS[model]

    for known_model, pricing in MODEL_COSTS.items():
        if model.startswith(known_model):
            return pricing

    return None


def compute_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    pricing = _lookup_cost(model)
    if pricing is None:
        print(
            f"[cost_config] Unknown model '{model}' — cost will be 0.0",
            file=sys.stderr,
        )
        return 0.0

    cost = (
        prompt_tokens / 1_000_000 * pricing["input_per_1m"]
        + completion_tokens / 1_000_000 * pricing["output_per_1m"]
    )
    return round(cost, 6)


def format_cost(cost_usd: float) -> str:
    if cost_usd == 0.0:
        return "$0.000000"
    if cost_usd < 0.01:
        return f"${cost_usd:.6f}"
    if cost_usd < 1.0:
        return f"${cost_usd:.4f}"
    return f"${cost_usd:.2f}"
