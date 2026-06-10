# Archaeologist

Archaeologist is built for abandoned and poorly-documented repositories — the kind you inherit with no README, no architecture diagram, and no one left to ask. Point it at a GitHub URL and it clones the repo, parses every Python file with Tree-sitter, embeds the chunks with OpenAI, and runs a multi-step LLM agent that reconstructs the project's purpose, summarizes each module, surfaces incomplete or stubbed features, and produces a dependency graph. The goal is to compress what would normally be a multi-hour archaeology session into a single streamed report.

## Setup

1. **Clone the repo**

   ```bash
   git clone <repository-url> archaeologist
   cd archaeologist
   ```

2. **Create a Python virtual environment**

   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Copy `.env.example` to `.env`**

   ```bash
   cp .env.example .env
   ```

   Then open `backend/.env` and set `OPENAI_API_KEY` to your key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

5. **Install frontend dependencies**

   ```bash
   cd ../frontend
   npm install
   ```

6. **Run the app**

   From the project root:

   ```bash
   cd ..
   ./start.sh
   ```

   This starts the FastAPI backend on `http://localhost:8000` and the Vite frontend on `http://localhost:5173`. Open the frontend URL in your browser, paste a GitHub repo URL, and watch the analysis stream in.
