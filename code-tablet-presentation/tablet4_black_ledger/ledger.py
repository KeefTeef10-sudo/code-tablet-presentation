from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import git, os, subprocess

app = FastAPI()

roles = {
    "Architect": "Designs the architecture of the requested project.",
    "Developer": "Writes fully functional, clean code.",
    "Tester": "Writes and runs tests for the project.",
    "Deployer": "Creates deployment scripts (Docker, etc.)."
}

agents = { role: Ollama(model="llama3") for role in roles }

prompt_template = PromptTemplate(
    input_variables=["role", "task"],
    template="{role}:\n{task}"
)

def run_agent(role, task):
    chain = LLMChain(llm=agents[role], prompt=prompt_template)
    return chain.run({"role": roles[role], "task": task})

class BuildRequest(BaseModel):
    description: str
    repo_path: str = "./generated_project"

@app.post("/forge")
async def forge(req: BuildRequest):
    os.makedirs(req.repo_path, exist_ok=True)
    log = {}

    log["Architecture"] = run_agent("Architect", req.description)

    code = run_agent("Developer", log["Architecture"])
    with open(f"{req.repo_path}/app.py", "w") as f:
        f.write(code)

    tests = run_agent("Tester", log["Architecture"])
    with open(f"{req.repo_path}/test_app.py", "w") as f:
        f.write(tests)
    subprocess.run(["pytest", req.repo_path])

    deploy = run_agent("Deployer", log["Architecture"])
    with open(f"{req.repo_path}/Dockerfile", "w") as f:
        f.write(deploy)

    repo = git.Repo.init(req.repo_path)
    repo.git.add(all=True)
    repo.index.commit("Initial commit from Black Ledger")

    return {"log": log, "status": "Project forged successfully."}
