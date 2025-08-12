#!/usr/bin/env bash
set -e
echo "📦 Installing Living Codex environment..."
sudo apt update
sudo apt install -y python3 python3-pip docker.io git curl sqlite3
echo "🐫 Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh
pip3 install fastapi uvicorn langchain langchain_community websockets gitpython pytest docker
echo "✅ The Living Codex awakens."
echo "Run with: uvicorn codex:app --reload --port 9700"
