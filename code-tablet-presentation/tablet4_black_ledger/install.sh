#!/usr/bin/env bash
set -e
sudo apt update
sudo apt install -y python3 python3-pip docker.io git curl sqlite3
curl -fsSL https://ollama.com/install.sh | sh
pip3 install fastapi uvicorn langchain langchain_community gitpython pytest docker
echo "Run with: uvicorn ledger:app --reload --port 9500"
