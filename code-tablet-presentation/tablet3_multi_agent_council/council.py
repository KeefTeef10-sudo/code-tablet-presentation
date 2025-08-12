from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

app = FastAPI()

roles = {
    "Strategist": "You are a master strategist. Plan steps clearly.",
    "Researcher": "You find and summarize facts concisely.",
    "Coder": "You write clean, functioning Python code.",
    "Reviewer": "You critique plans and code, ensuring quality."
}

agents = { role: Ollama(model="llama3") for role in roles }

prompt_template = PromptTemplate(
    input_variables=["role", "task"],
    template="{role}:\n{task}"
)

def run_agent(role, task):
    llm = agents[role]
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run({"role": roles[role], "task": task})

class TaskRequest(BaseModel):
    query: str

@app.post("/solve")
async def solve(req: TaskRequest):
    log = {}
    for role in roles:
        log[role] = run_agent(role, req.query)
    return {"Council Decision": log}

@app.websocket("/council")
async def council_ws(ws: WebSocket):
    await ws.accept()
    task = await ws.receive_text()
    for role in roles:
        response = run_agent(role, task)
        await ws.send_text(f"{role}: {response}")
    await ws.close()
