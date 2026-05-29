# DESIGN.md

### Python-only Repositories
Rather than building a language-agnostic system upfront, the MVP deliberately targets Python only. This eliminated a whole dimension of complexity (multi-language Tree-sitter grammars, language-specific chunk strategies) and let the team validate the core archaeology report concept first. If the report isn't useful for Python repos, it won't be useful for Go repos either.
This was primarily a human decision due to the fact the agent was struggling with more complex languages.

### Stream Progress 
Analysis takes 60–90 seconds. Rather than showing a spinner and hoping users wait, the pipeline emits live progress events ("Cloning repo... Parsing 47 files... Running analysis...") via SSE. This reframes the wait as transparency rather than latency, and gives users enough signal to know the tool is actually working rather than frozen.
This was a mixture of human and AI decision making as I was prompted by an AI to make the decision to add in a stream visual for progress.

### No Persistence for the MVP
The MVP stores nothing to disk — no user accounts, no saved reports, no re-use of previous embeddings. This cut weeks of backend work (auth, databases, cache invalidation) in exchange for one real limitation: every analysis run starts from scratch. The bet is that validating the report quality matters more right now than validating the infrastructure around it.
This was a human decision as I wanted to take this ambitious project piece-by-piece. My deconstructing the project into parts I can evaluate individually, I can ensure the whole will be properly functional.