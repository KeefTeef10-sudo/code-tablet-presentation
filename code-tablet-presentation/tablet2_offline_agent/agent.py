from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import sqlite3

conn = sqlite3.connect("agent_memory.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS logs (prompt TEXT, response TEXT)")
conn.commit()

app = FastAPI()

llm = Ollama(model="llama3")  # change to any local model you've pulled
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

class Query(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(query: Query):
    response = conversation.run(query.prompt)
    cursor.execute("INSERT INTO logs VALUES (?, ?)", (query.prompt, response))
    conn.commit()
    return {"response": response}

@app.get("/history")
async def history():
    cursor.execute("SELECT * FROM logs")
    return {"history": cursor.fetchall()}
