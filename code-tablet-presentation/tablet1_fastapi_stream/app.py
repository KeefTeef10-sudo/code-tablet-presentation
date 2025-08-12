"""
README:
Run with: uvicorn app:app --reload --port 8080
Endpoints:
 - /healthz GET
 - /infer POST: streams text/event-stream chunks
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio

app = FastAPI()

class InferenceRequest(BaseModel):
    prompt: str

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

async def run_inference(prompt: str):
    for i in range(1, 6):
        yield f"data: chunk {i} for '{prompt}'\n\n"
        await asyncio.sleep(0.4)

@app.post("/infer")
async def infer(req: InferenceRequest):
    async def streamer():
        async for chunk in run_inference(req.prompt):
            yield chunk
    return StreamingResponse(streamer(), media_type="text/event-stream")
