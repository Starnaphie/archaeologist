# archaeologist

Generate AI-powered archaeology reports for Python repositories. Feed in a GitHub URL, get back an automated understanding of what the codebase does, how it's structured, and what work remains unfinished.

## Demo

https://youtu.be/7Rx5fHxdWVI

## Tech stack

### Backend
| Library | Purpose |
|---------|---------|
| **FastAPI** | REST API framework with async support |
| **uvicorn** | ASGI server for running FastAPI |
| **Tree-sitter** (tree-sitter-python) | AST parsing for Python code extraction |
| **FAISS** | Vector similarity search for code chunks |
| **OpenAI** | LLM for report generation and embeddings |
| **LangChain** | LLM orchestration and structured output |
| **GitPython** | Repository cloning and management |
| **pydantic** | Data validation and structured outputs |
| **sse-starlette** | Server-Sent Events for progress streaming |

### Frontend
| Library | Purpose |
|---------|---------|
| **React** | UI component framework |
| **Vite** | Build tool and dev server |
| **Mermaid** | Dependency graph visualization |

## Project structure

```
archaeologist/
├── backend/
│   ├── main.py              FastAPI app with /analyze (SSE) and /report/{job_id} endpoints
│   ├── ingestion.py         GitHub repo cloning and Python file discovery
│   ├── parser.py            Tree-sitter AST parsing; extracts functions, classes, imports
│   ├── embedder.py          OpenAI embeddings with FAISS indexing for similarity search
│   ├── agent.py             Report generation pipeline: purpose, architecture, incomplete features
│   ├── __init__.py          Package initialization
│   ├── .env                 Environment variables (OPENAI_API_KEY)
│   └── requirements.txt     Python dependencies (generated from venv)
├── frontend/
│   ├── src/
│   │   ├── App.jsx          Main form; SSE listener; state management
│   │   ├── ReportView.jsx   Renders purpose, modules table, dependency graph, TODOs
│   │   ├── ProgressLog.jsx  Real-time progress stream display
│   │   ├── App.module.css   App styling
│   │   ├── ReportView.module.css
│   │   ├── ProgressLog.module.css
│   │   └── main.jsx         React entry point
│   ├── package.json         Dependencies: React, Vite, Mermaid
│   ├── vite.config.js       Vite configuration
│   └── index.html           HTML template
├── start.sh                 Bash script to run backend + frontend concurrently
├── README.md                This file
├── DESIGN.md                Design rationale (Python-only, streaming, no persistence)
└── LICENSE                  MIT License
```

## Prerequisites

- **Python 3.12+**
- **Node 18+** and **npm 9+**
- **OpenAI API key** (required for embeddings and LLM calls)

## Setup and installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/archaeologist.git
cd archaeologist
```

### 2. Backend setup
```bash
# Create and activate virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate  # On Windows: backend\venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env and add your OpenAI API key:
# OPENAI_API_KEY=sk-...
```

### 3. Frontend setup
```bash
cd frontend
npm install
cd ..
```

### 4. Running the application

**Option A: Using the startup script (recommended)**
```bash
./start.sh
```
This spawns the FastAPI backend on `http://localhost:8000` and the React dev server on `http://localhost:5173`.

**Option B: Manual startup**
```bash
# Terminal 1: Backend
source backend/venv/bin/activate
uvicorn backend.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

## How it works

The analysis pipeline runs in four stages:

### 1. Ingestion
Clone the target GitHub repository and discover all Python files, excluding virtual environments, node_modules, test directories, and pycache. Returns a manifest with file paths and total file count.

### 2. Parsing & Embedding
Use Tree-sitter to parse each Python file and extract top-level functions and classes with their docstrings. Build a symbol map of all imports (internal and external). Generate vector embeddings of code chunks using OpenAI's `text-embedding-3-small` model (1536 dimensions) and index them with FAISS for semantic search.

### 3. Agent Reasoning
The agent runs three parallel analysis steps:
- **Purpose**: Retrieve top 10 code chunks semantically similar to "what does this project do," then ask Claude to infer the project's 1-3 sentence purpose and a ≤15 word one-liner.
- **Architecture**: For each file, retrieve its top 3 code chunks, then summarize each module in one sentence.
- **Incomplete Features**: Find code chunks with TODO, FIXME, NotImplemented, or empty pass stubs. Ask Claude to describe each as a user-readable feature gap.
- **Dependency Graph**: Build a Mermaid diagram of internal module dependencies (max 20 nodes, truncated if larger).

### 4. Report Generation
Return a JSON report containing all analysis results. The frontend streams progress events via SSE and renders the final report with formatted tables, a module dependency graph, and a checklist of unfinished work.

## API reference

### POST /analyze
Submit a GitHub URL and receive a streaming JSON event source.

**Request body:**
```json
{
  "github_url": "https://github.com/owner/repo"
}
```

**SSE event shapes:**

| Event | Data | Notes |
|-------|------|-------|
| `job_id` | UUID string | Unique identifier for this analysis run |
| `progress` | String | Human-readable stage update (e.g., "Cloning repo...", "Parsing 47 files...") |
| `done` | JSON string | Full report (see below) |

**Report JSON shape:**
```json
{
  "purpose": "String describing what the project does (1-3 sentences)",
  "one_liner": "Brief description (≤15 words)",
  "modules": [
    {
      "name": "relative/file/path.py",
      "description": "One-sentence summary"
    }
  ],
  "incomplete_features": [
    "Feature gap 1",
    "Feature gap 2"
  ],
  "dependency_graph": "graph LR\n  ..."
}
```

### GET /report/{job_id}
Retrieve a cached report by job ID.

**Response:** Same JSON shape as the `done` event above.

## Scope and known limits

- **Python repositories only** — Other languages not supported in the MVP.
- **Up to ~500 files** — No hard limit, but performance degrades with very large repos.
- **3-minute timeout** — Long-running analyses may be interrupted.
- **No authentication** — All endpoints are public.
- **No persistence** — Reports exist only in memory during the session. Restarting the server clears all cached reports. No database, no user accounts.
- **Dependency graph truncated to 20 nodes** — Larger codebases show only the first 20 internal modules.
- **8000-token limit per code chunk** — Chunks are truncated for embedding efficiency.

## Roadmap

Post-MVP features planned or under consideration:

- **Multi-agent system** — Specialized agents for different analysis tasks (testing patterns, API design, performance bottlenecks).
- **README generation** — Auto-generate project README from the analysis.
- **Interactive Q&A** — Chat interface to ask follow-up questions about the codebase.
- **Timeline visualization** — Show commit history and refactoring patterns over time.
- **Multi-language support** — Extend AST parsing to JavaScript, Go, Rust, etc.
- **Persistence layer** — Save reports to a database; support user accounts and saved analyses.
- **Incremental updates** — Diff-based re-analysis for updated repositories.

## Contributing

Contributions welcome! Please submit issues and pull requests on [GitHub](https://github.com/yourusername/archaeologist).

## License

MIT License — see [LICENSE](LICENSE) for details.
