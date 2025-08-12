# Code Tablet Presentation (Bound Codex)

This package contains the code tablets we discussed:
1) FastAPI Streaming Inference Server
2) Offline AI Agent (Ollama + LangChain)
3) Multi‑Agent Council
4) Black Ledger (Autonomous Builder)
5) Living Codex (all four bound) + CLI spells
6) Extras (budget forecaster, disk cleaner, React client, autosync)

## Quick start (Living Codex)
```bash
cd living_codex
bash install.sh
uvicorn codex:app --reload --port 9700
```
In another terminal, try the CLI:
```bash
# make it executable
chmod +x codex.sh
# stream a response
./codex.sh infer "Write a poem about moonlight on frozen pine trees"
# stream a council
./codex.sh council "Plan a low-cost solar generator"
# stream a live forge
./codex.sh forge "Minimal FastAPI + SQLite task tracker" ./task_tracker
```

## Structure
- `tablet1_fastapi_stream/` – Minimal streaming server (chunked SSE)
- `tablet2_offline_agent/` – Local agent over FastAPI with SQLite logs
- `tablet3_multi_agent_council/` – Role agents + WebSocket live session
- `tablet4_black_ledger/` – Autonomous builder (architecture/code/tests/docker)
- `living_codex/` – Unified system with streaming forge (`/forge_stream`) and CLI
- `extras/` – Utility scripts and samples
- `drive_github_dual_binding.md` – Guide to bind Google Drive + GitHub

> Notes: These files target Linux/WSL. Ollama must be installed to run the agent/council/codex components. Replace `llama3` with any model you have locally (e.g., `qwen2.5`, `phi3`, etc.).
