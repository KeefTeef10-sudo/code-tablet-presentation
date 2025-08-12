from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain.llms import Ollama
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os, subprocess, sqlite3, git, asyncio, json, sys

app = FastAPI()

# Persistent Memory DB
conn = sqlite3.connect("codex_memory.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS logs (prompt TEXT, response TEXT)")
conn.commit()

def llm_base(): 
    return Ollama(model="llama3")

roles = {
    "Strategist": "Plan the approach.",
    "Researcher": "Gather and summarize knowledge.",
    "Coder": "Write clean, functional code.",
    "Reviewer": "Critique and improve output.",
    "Deployer": "Prepare deployment scripts."
}
agents = { role: llm_base() for role in roles }

prompt_template = PromptTemplate(
    input_variables=["role", "task"],
    template="{role}:\n{task}"
)

def run_agent(role, task):
    chain = LLMChain(llm=agents[role], prompt=prompt_template)
    return chain.run({"role": roles[role], "task": task})

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm_base(), memory=memory)

class Query(BaseModel):
    prompt: str

class BuildRequest(BaseModel):
    description: str
    repo_path: str = "./codex_build"

@app.post("/infer")
async def infer(req: Query):
    cursor.execute("INSERT INTO logs VALUES (?, ?)", (req.prompt, ""))
    conn.commit()
    return {"response": conversation.run(req.prompt)}

@app.post("/agent")
async def agent(req: Query):
    res = conversation.run(req.prompt)
    cursor.execute("INSERT INTO logs VALUES (?, ?)", (req.prompt, res))
    conn.commit()
    return {"response": res}

@app.get("/history")
async def history():
    cursor.execute("SELECT * FROM logs")
    return {"history": cursor.fetchall()}

@app.post("/council")
async def council(req: Query):
    log = { role: run_agent(role, req.prompt) for role in roles }
    return {"Council": log}

@app.websocket("/council_ws")
async def council_ws(ws: WebSocket):
    await ws.accept()
    task = await ws.receive_text()
    for role in roles:
        await ws.send_text(f"{role}: {run_agent(role, task)}")
    await ws.close()

# --- SSE helpers for streaming forge ---
def sse(event: str, data):
    payload = data if isinstance(data, str) else json.dumps(data)
    return f"event: {event}\ndata: {payload}\n\n"

async def sse_forge(description: str, repo_path: str):
    try:
        yield sse("stage", "Planning architecture…")
        arch = run_agent("Strategist", description)
        yield sse("architecture", arch)

        yield sse("stage", "Coding…")
        os.makedirs(repo_path, exist_ok=True)
        code = run_agent("Coder", arch)
        with open(f"{repo_path}/app.py", "w") as f:
            f.write(code)
        yield sse("file", "app.py written")

        yield sse("stage", "Authoring tests…")
        tests = run_agent("Reviewer", arch)
        with open(f"{repo_path}/test_app.py", "w") as f:
            f.write(tests)
        yield sse("file", "test_app.py written")

        yield sse("stage", "Running tests…")
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "pytest", repo_path, "-q",
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )
        assert proc.stdout is not None
        async for line in proc.stdout:
            yield sse("test", line.decode(errors="ignore").rstrip())
        rc = await proc.wait()
        yield sse("test_result", f"pytest exit code {rc}")

        yield sse("stage", "Preparing Dockerfile…")
        dockerfile = run_agent("Deployer", arch)
        with open(f"{repo_path}/Dockerfile", "w") as f:
            f.write(dockerfile)
        yield sse("file", "Dockerfile written")

        yield sse("stage", "Initializing git repo…")
        repo = git.Repo.init(repo_path)
        repo.git.add(all=True)
        repo.index.commit("Initial commit from Codex Forge (stream)")
        yield sse("git", "Initial commit created")

        # Optional push controlled by env
        if os.environ.get("CODEX_PUSH", "0") == "1":
            remote = os.environ.get("CODEX_REMOTE", "origin")
            try:
                subprocess.run(["git", "-C", repo_path, "push", remote, "HEAD:main"], check=False)
                yield sse("git", "Pushed to remote")
            except Exception as e:
                yield sse("error", f"push failed: {e}")

        yield sse("done", "Project forged successfully.")
    except Exception as e:
        yield sse("error", f"{type(e).__name__}: {e}")

class ForgeStreamRequest(BaseModel):
    description: str
    repo_path: str = "./codex_build"

@app.post("/forge_stream")
async def forge_stream(req: ForgeStreamRequest):
    async def streamer():
        async for chunk in sse_forge(req.description, req.repo_path):
            yield chunk
    return StreamingResponse(streamer(), media_type="text/event-stream")

@app.post("/forge")
async def forge(req: BuildRequest):
    # non-streaming variant for convenience
    os.makedirs(req.repo_path, exist_ok=True)
    log = {}
    log["Architecture"] = run_agent("Strategist", req.description)
    code = run_agent("Coder", log["Architecture"])
    with open(f"{req.repo_path}/app.py", "w") as f:
        f.write(code)
    tests = run_agent("Reviewer", log["Architecture"])
    with open(f"{req.repo_path}/test_app.py", "w") as f:
        f.write(tests)
    subprocess.run(["pytest", req.repo_path])
    dockerfile = run_agent("Deployer", log["Architecture"])
    with open(f"{req.repo_path}/Dockerfile", "w") as f:
        f.write(dockerfile)
    repo = git.Repo.init(req.repo_path)
    repo.git.add(all=True)
    repo.index.commit("Initial commit from Living Codex")
    return {"Forge Log": log}
