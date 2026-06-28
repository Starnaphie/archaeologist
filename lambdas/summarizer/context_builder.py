"""Builds presentation context from archaeologist findings. Extracts the most presentation-relevant content from findings.json and assembles it into a description string for generate_outline."""

from lambdas.shared.schemas import FindingsSchema


def build_description(findings: dict, topic: str) -> str:
    purpose = findings.get("purpose", "")
    one_liner = findings.get("one_liner", "")
    modules = findings.get("modules", [])
    incomplete_features = findings.get("incomplete_features", [])
    repo_owner = findings.get("repo_owner", {})
    acronyms = findings.get("acronyms", [])

    sections = []

    owner = repo_owner.get("owner") if isinstance(repo_owner, dict) else None
    repo_name = repo_owner.get("repo_name") if isinstance(repo_owner, dict) else None
    if owner:
        sections.append(f"Repo: {owner}/{repo_name}")

    if purpose:
        sections.append(f"Purpose: {purpose}")
    elif one_liner:
        sections.append(f"Purpose: {one_liner}")

    if modules:
        lines = []
        for module in modules[:6]:
            if not isinstance(module, dict):
                continue
            name = module.get("name", "")
            description = module.get("description", "")
            if name or description:
                lines.append(f"- {name}: {description}")
        if lines:
            sections.append("Key components:\n" + "\n".join(lines))

    if incomplete_features:
        lines = [f"- {feature}" for feature in incomplete_features[:3] if feature]
        if lines:
            sections.append("Known gaps:\n" + "\n".join(lines))

    if acronyms:
        pairs = []
        for entry in acronyms[:8]:
            if not isinstance(entry, dict):
                continue
            acronym = entry.get("acronym", "")
            full_name = entry.get("full_name", "")
            if acronym and full_name:
                pairs.append(f"{acronym} ({full_name})")
        if pairs:
            sections.append("Key acronyms: " + ", ".join(pairs))

    description = "\n\n".join(sections)
    if len(description) > 1500:
        return description[:1500] + "..."
    return description


def infer_audience(findings: dict, topic: str) -> str:
    text = " ".join(
        [
            findings.get("purpose", ""),
            findings.get("one_liner", ""),
        ]
    )
    text_lower = text.lower()

    if any(term in text_lower for term in ("machine learning", "ml", "ai", "model")):
        return "software engineers and data scientists"
    if any(
        term in text_lower
        for term in ("infrastructure", "kubernetes", "docker", "aws", "cloud")
    ):
        return "platform and infrastructure engineers"
    if any(term in text_lower for term in ("api", "backend", "service", "microservice")):
        return "backend software engineers"
    if any(term in text_lower for term in ("frontend", "ui", "react", "vue")):
        return "frontend software engineers"
    return "software engineers"
