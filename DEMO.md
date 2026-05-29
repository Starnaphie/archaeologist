# Building Archaeologist from Scratch

Archaeologist is a tool that analyzes Python repositories and generates AI-powered insights about codebase structure, dependencies, and architectural patterns. This guide walks you through building it locally.

## Prerequisites

- **Python 3.12+** installed on your system
- **Node.js 18+** and npm
- **OpenAI API key** (for embeddings and analysis)
- Git

## Step 1: Clone & Setup the Repository

```bash
git clone <repository-url> archaeologist
cd archaeologist
```

## Step 2: Set Up the Backend

### 2a. Create Python Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2b. Install Python Dependencies

```bash
pip install --upgrade pip
pip install openai faiss-cpu python-dotenv uvicorn fastapi tiktoken
```

If you're on Apple Silicon (M1/M2/M3), use `faiss-cpu` instead of `faiss-gpu`.

### 2c. Configure Environment Variables

Create or update `.env` in the `backend/` directory:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Get your OpenAI API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

## Step 3: Set Up the Frontend

### 3a. Install Node Dependencies

```bash
cd frontend
npm install
```

### 3b. Build the Frontend (Optional)

For production builds:

```bash
npm run build
```

For development, the dev server will be started automatically in the next step.

## Step 4: Run the Tool

From the project root directory:

```bash
./start.sh
```

This script:
- Activates the Python virtual environment
- Starts the FastAPI backend on `http://localhost:8000`
- Starts the Vite dev server for the frontend on `http://localhost:5173`

The tool will be available at `http://localhost:5173` in your browser.

### Manual Startup (if you prefer separate terminals)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Step 5: Using the Tool

1. Open `http://localhost:5173` in your browser
2. Paste a GitHub repository URL (must be a Python repository)
3. Click "Analyze" to begin the analysis
4. Watch real-time progress as the tool:
   - Clones the repository
   - Parses Python files
   - Builds embeddings
   - Runs analysis with Claude
5. View the generated architectural report with dependency graphs and insights

## Architecture Overview

### Backend (`backend/`)

- **`main.py`** — FastAPI application with WebSocket support for streaming progress
- **`ingestion.py`** — Clones and prepares repositories
- **`parser.py`** — Parses Python files into chunks using Tree-sitter
- **`embedder.py`** — Creates vector embeddings using OpenAI's text-embedding-3-small
- **`agent.py`** — Runs analysis with Claude to generate insights
- **`.env`** — Environment configuration (OpenAI API key)

### Frontend (`frontend/`)

- Built with **React 19** and **Vite**
- Real-time progress streaming via Server-Sent Events (SSE)
- Visualizes dependency graphs using **Mermaid**
- Responsive UI with architectural report display

## Troubleshooting

### "Module not found" errors

Ensure the Python virtual environment is activated:
```bash
source backend/venv/bin/activate
```

### OpenAI API errors

- Verify your API key is correct in `backend/.env`
- Check that your account has API credits
- Ensure the key has permissions for embeddings and chat completions

### Port already in use

If port 8000 (backend) or 5173 (frontend) is already in use:

**Backend:**
```bash
uvicorn backend.main:app --reload --port 8001
```

**Frontend:**
```bash
npm run dev -- --port 5174
```

### Frontend won't connect to backend

Check that the backend is running on `http://localhost:8000`. The frontend expects the API at this address. If you change the port, update the API base URL in the frontend code.

## Development Tips

- The backend auto-reloads on file changes (thanks to uvicorn's `--reload` flag)
- The frontend hot-reloads via Vite
- Check the browser console and terminal output for debugging
- Analysis typically takes 60–90 seconds; progress updates stream in real-time

## Next Steps

- Explore the `DESIGN.md` for architectural decisions
- Review `backend/agent.py` to understand how Claude analyzes repositories
- Customize the analysis prompt or add new report sections
