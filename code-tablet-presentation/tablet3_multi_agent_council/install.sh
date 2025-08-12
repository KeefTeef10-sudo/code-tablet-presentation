#!/usr/bin/env bash
set -e
sudo apt update
sudo apt install -y python3 python3-pip sqlite3 curl
curl -fsSL https://ollama.com/install.sh | sh
pip3 install fastapi uvicorn langchain langchain_community websockets
echo "Run with: uvicorn council:app --reload --port 9000"
