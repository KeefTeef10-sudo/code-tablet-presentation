#!/usr/bin/env bash
set -e
sudo apt update
sudo apt install -y curl python3 python3-pip sqlite3
curl -fsSL https://ollama.com/install.sh | sh
pip3 install fastapi uvicorn langchain langchain_community
echo "Run with: uvicorn agent:app --reload --port 8000"
