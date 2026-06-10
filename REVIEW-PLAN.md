# REVIEW-PLAN.md



# REVIEW #1

## Pre-review by Jackson Loeffler (A17375053)
## Review of Stephanie Xu

### 1. Project summary/implementation

#### a. Summary
_In a few sentences: which project option is this (run-it-locally, auth + live
URL, embed-in-a-tool, generation, agentic programming, or their own), who are
the intended users, and what does the tool do? If you can't tell from the
README/DESIGN.md, say so — that's useful feedback._

The project seems to be a new project rather than an extension of an existing project from the class. The project is a Git repository analyzer for Python projects. The tool downloads Git repositories, feeds every Python file to an LLM, then summarizes the repository, provides a dependency graph, and lists TODOs.

#### b. Demo attempt
_Follow the team's DEMO.md. Did you reach a running tool (or live URL /
install)? Note exactly how far you got: what worked, where it broke, any error
messages._

I was able to follow the DEMO.md file and run the tool, but I did run into some issues with the provided steps. After running the provided steps, I got several missing package errors for sse_starlette, langchain-core, langchain_openai, GitPython, and tree-sitter-python. I was able to fix this pretty easily by installing the missing packages, but it did take several trials. Another minor issue I encountered is that the manual backend steps did not work because of an import issue, but I was able to work around this issue by running the uvicorn command from the `start.sh` script.

- added missing dependencies to requirements.txt

_If you could NOT get it running, don't skip this — instead reconstruct the
intended flow by reading the code. Pick one user story (their first
deliverable, or what they put in their video, is a good choice), find the entry
point, and trace it through the major components: for each step name the
file/function, say what data goes in and out, and quote the prompt(s) sent to
the model if any. Describe what *should* happen end to end, and flag any place
where the code path looks broken or incomplete. No matter what, say
specifically what blocked the demo so the team can fix it (installation, code
bug, platform issue, etc.)._

N/A

#### c. Proposal component check
_Open the marked-up proposal in `proposal/`. Pick two components the team marked
"implemented as written" and find them in the code — quote the file path (and
route/function) where each lives, and say whether the code matches what the
proposal claims. Then pick one component they marked "planned" or "no longer
planned" and note whether that seems reasonable to you for the final deadline._

Implemented: React frontend in the frontend folder. I think that the implementation looks very good and uses modern tools like Vite which ran very quickly on my machine. The frontend does everything that was mentioned in the proposal, which is basically just providing the Git repository URL and showing the results (dependency graph, summary, TODOs).

Implemented: GitPython ingestion script in backend/ingestion. As described in the proposal, it clones the git repository and searches for Python files.

Planned: Commit history retrieval. I think that this is very reasonable and seems very straightforward to implement, especially given the existing GitPython implementation that can be extended.

_If there's no marked-up proposal (or it's too vague to use), do the mapping as
the reviewer: take the component list from their original proposal and, for 3-4
components, locate each in the code (file + function/route) or note that you
can't find it. If even the original proposal isn't usable, build the inventory
from scratch — list the 5-10 major components you can identify in the codebase
and where each lives — and flag the missing/vague proposal as feedback._

#### d. One confusing thing
_Identify one thing you find confusing in the implementation, and describe why
it's confusing and what you tried reading to understand it._

I am a little confused by the _PASS_STUB_RE RegEx. It seems very complicated and it would be nice to have a comment explaining what exactly it is supposed to be matching and how, since its purpose seems unclear to me. Based on the name I would think that it would detect empty functions but the RegEx seems too complicated for that, so I'm not sure if there is some additional nuance I'm missing.

#### e. A conversation starter for Tuesday
_Come up with a conversation starter for Tuesday – what's something you want
to see **them** demo, or explain, or justify in their system._

I would be interested in hearing the specific use case and seeing this work on some sample abandoned repositories. When I first read the README and set up the DEMO, I didn't actually realize that the purpose of the project was specifically focused on abandoned repositories, so it would be cool to hear more of that story.

### 2. Suggestions

#### a. Scope feedback for the final deliverable
_Look at the team's "after first deliverable goals." Given what's working now,
what should they prioritize before the final deadline — and is there a gotcha
you'd flag (e.g. sensitive data going public, a local model that may not be
capable enough, an auth/cost-ceiling gap)? Be specific and grounded in their
setup._

I would probably focus on the evaluation, additional languages, multi-agent, and Q&A features since those sound the most useful. Each goal on its own sounds reasonable, but implementing all seven would likely be too much work. I would hesitate to implement a full timeline visualization based on git diffs since the commit history can get quite big, folders can be renamed causing large diffs for little actual change, and visualizations still require human interpretation anyways.

#### b. One concrete suggestion
_Suggest one improvement or extension. Give a substantive argument grounded in
details of the implementation or the project's domain — not a generic "add
tests" or "use a smaller model."_

The backend/agent.py file currently uses _THIRD_PARTY_PREFIXES, a hard-coded list of package names to detect third-party modules. I think it would be much nicer to detect requirements.txt or pyproject.toml and use pip to determine the list of third-party module names dynamically instead of depending on hard-coded lists.

- did not implement
- third party modules give a better idea of the project's purpose and package dependencies can easily get messy and unreadable

#### c. Something you learned or thought was cool
_Call out one specific thing from this project you learned from or genuinely
enjoyed — a technique, a design decision, a clever prompt, a tool or library you
hadn't seen. Be concrete about what it was and why it stuck with you._

I thought it was cool to see how the embedding module gives the LLM relevant information without having to manually extract specific parts of the codebase. I don't know how common this is, but I had never seen embedding modules used for vague queries like "what does this code do" before, so it was interesting to see.



# REVIEW #2

## Pre-review by Ethan Jenkins, A17711518
## Review of Stephanie Xu0

### 1. Project summary/implementation

#### a. Summary
_In a few sentences: which project option is this (run-it-locally, auth + live
URL, embed-in-a-tool, generation, agentic programming, or their own), who are
the intended users, and what does the tool do? If you can't tell from the
README/DESIGN.md, say so — that's useful feedback._

- This is a run-it-locally project. The README gives local setup instructions, starts a FastAPI backend and Vite frontend on localhost, and explicitly says there is no authentication or persistence.

- The intended users seem to be developers working with Python GitHub repositories, especially people who want a quick “archaeology report” on an unfamiliar codebase. The tool takes a GitHub URL, clones and parses the Python repo, embeds code chunks, uses an LLM to infer purpose/architecture/incomplete features, and presents a streamed report with module summaries, a dependency graph, and TODO-style gaps.

#### b. Demo attempt
_Follow the team's DEMO.md. Did you reach a running tool (or live URL /
install)? Note exactly how far you got: what worked, where it broke, any error
messages._

_If you could NOT get it running, don't skip this — instead reconstruct the
intended flow by reading the code. Pick one user story (their first
deliverable, or what they put in their video, is a good choice), find the entry
point, and trace it through the major components: for each step name the
file/function, say what data goes in and out, and quote the prompt(s) sent to
the model if any. Describe what *should* happen end to end, and flag any place
where the code path looks broken or incomplete. No matter what, say
specifically what blocked the demo so the team can fix it (installation, code
bug, platform issue, etc.)._

- I reached the running local tool after some manual fixes. The frontend opened successfully, but the documented ./start.sh did not work from PowerShell, and the backend setup instructions were incomplete: I had to install missing dependencies such as sse-starlette, GitPython, tree-sitter, tree-sitter-python, langchain-openai, and numpy.

- added in missing dependencies

#### c. Proposal component check
_Open the marked-up proposal in `proposal/`. Pick two components the team marked
"implemented as written" and find them in the code — quote the file path (and
route/function) where each lives, and say whether the code matches what the
proposal claims. Then pick one component they marked "planned" or "no longer
planned" and note whether that seems reasonable to you for the final deadline._

_If there's no marked-up proposal (or it's too vague to use), do the mapping as
the reviewer: take the component list from their original proposal and, for 3-4
components, locate each in the code (file + function/route) or note that you
can't find it. If even the original proposal isn't usable, build the inventory
from scratch — list the 5-10 major components you can identify in the codebase
and where each lives — and flag the missing/vague proposal as feedback._

- The proposal says the backend should use FastAPI and provide an analysis endpoint plus a way to retrieve finished reports. That matches backend/main.py: the code accepts a GitHub URL, streams progress/results back to the frontend, and stores completed reports in memory so they can be fetched later.

- The proposal also says the system should index repositories by chunking source code, embedding those chunks, and storing them in FAISS for retrieval. That matches backend/parser.py and backend/embedder.py: the code extracts top-level Python functions/classes, turns them into embedding vectors, builds an in-memory FAISS index, and supports semantic lookup. The main caveat is that chunking is limited to top-level functions/classes rather than deeper code structure.

- For a planned component, interactive repository Q&A is marked [PLANNED]. That seems reasonable to leave out for the final deadline since the project already has retrieval and report generation, but a real chat endpoint would need new backend routing, conversational state, frontend UI, and probably persistence/session handling. Given the MVP scope, prioritizing the one-shot archaeology report over Q&A makes sense.

#### d. One confusing thing
_Identify one thing you find confusing in the implementation, and describe why
it's confusing and what you tried reading to understand it._

- One confusing thing is the project’s setup/dependency story. The instructions make it sound like there are only a few packages to install and that one startup script will run everything, but in practice the app depends on several additional backend libraries and the provided virtual environment is tied to another platform. I had to compare the setup instructions against the actual imports in the backend to understand what was missing. The tool’s architecture made sense after that, but the path from “fresh clone” to “running app” was harder to follow than the docs suggest.

#### e. A conversation starter for Tuesday
_Come up with a conversation starter for Tuesday – what's something you want
to see **them** demo, or explain, or justify in their system._

- I’d ask to demo one full analysis run on a small unfamiliar Python repo and explain how they judge whether the generated “purpose” and “unfinished work” sections are actually trustworthy. The tool is interesting when it makes interpretive claims about a codebase, so I’d like to hear how they think about accuracy, hallucination, and what evidence from the repo the report should expose to users.

### 2. Suggestions

#### a. Scope feedback for the final deliverable
_Look at the team's "after first deliverable goals." Given what's working now,
what should they prioritize before the final deadline — and is there a gotcha
you'd flag (e.g. sensitive data going public, a local model that may not be
capable enough, an auth/cost-ceiling gap)? Be specific and grounded in their
setup._

- Before the final deadline, I think they should focus on tightening the current report flow instead of adding the bigger planned features like Q&A, timelines, or multi-language support. The main thing already works, so the biggest steps would be better setup docs, a real requirements.txt, removing the committed venv/.env, and clearer errors when analysis fails.

- One gotcha is trust in the generated report. The tool makes confident claims about a repo’s purpose, architecture, and unfinished work, but it doesn’t really show the evidence behind those claims. I’d want file/chunk citations or links back to the relevant code so users can tell whether the AI summary is actually grounded.

#### b. One concrete suggestion
_Suggest one improvement or extension. Give a substantive argument grounded in
details of the implementation or the project's domain — not a generic "add
tests" or "use a smaller model."_

- One concrete improvement would be to add source citations to the generated report. The backend already retrieves representative chunks for the purpose and module summaries, and each chunk includes its file path, name, kind, and source. Instead of only returning a plain summary, the report could include the specific files or symbols that supported each claim.

- added! footnotes are added to claims made in the writeup

#### c. Something you learned or thought was cool
_Call out one specific thing from this project you learned from or genuinely
enjoyed — a technique, a design decision, a clever prompt, a tool or library you
hadn't seen. Be concrete about what it was and why it stuck with you._

- I thought the live progress streaming was a really good design choice. Since the analysis can take a while, the tool shows updates like cloning, parsing, embedding, and running analysis instead of just showing a spinner. That made the app feel much more understandable and less frozen to me.


## Review from TAs
Here's our meta-review,

Fix the setup/dependency story. Both reviewers ran into missing packages, so make a real backend/requirements.txt and make sure DEMO.md installs everything needed.
Add source citations/file links to the generated report. Since the tool makes claims about a repo's purpose, architecture, and unfinished work, users need to see what code chunks supported those claims.
Focus on part of your 7 proposed features, like 4-5. You should try to do all of them if you have time, but I would prioritize completing 5 fully rather than having 7 completed at 80%. My recommendations would be multi-agent reasoning system, auto README generation, repo Q&A, support for additional languages, and evaluation on abandoned projects. Once again, I would love to see all the planned deliverables implemented! But I worry about time constraints and I want you to have a completed project.
If you do commit-history retrieval, start small. Full timeline visualization over git diffs can get messy very quickly with huge diffs, renames, and noisy history.
Replace _THIRD_PARTY_PREFIXES with something based on requirements.txt / pyproject.toml instead of a hard-coded package list.
Add a comment or simplify _PASS_STUB_RE, since it is not obvious what exactly it is matching.
Make the abandoned-repository use case clearer in README/DEMO. Reviewers did not immediately understand that this was the main story.
Improve errors when analysis fails, especially for dependency/setup problems and unsupported/non-Python repositories.
Nice live progress stream!

- fixed dependencies
- added source citations
- implemented mutli agent reasoning and readme generation
- only makes shallow clones with commit history of 1
- added comment to _PASS_STUB_RE
- added project description to DEMO.md
- frontend shows error box with reset button upon error