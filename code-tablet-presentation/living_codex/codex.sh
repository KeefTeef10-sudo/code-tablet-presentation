#!/usr/bin/env bash
# 📜 Codex CLI – interface to the Living Codex
# Streaming output for /infer, role-by-role council, and SSE forge

API_URL="${API_URL:-http://localhost:9700}"

stream_infer() {
  curl -s -N -X POST "$API_URL/infer"       -H "Content-Type: application/json"       -d "{"prompt": "$1"}"     | jq -r --unbuffered '.response'     | while IFS= read -r line; do echo -n "$line"; done
  echo
}

stream_council() {
  echo "📜 Convening the council..."
  curl -s -X POST "$API_URL/council"       -H "Content-Type: application/json"       -d "{"prompt": "$1"}"     | jq -r '."Council" | to_entries[] | "\(.key): \(.value)"'     | while IFS= read -r line; do
        echo -e "\n🗣 $line\n"
        sleep 0.4
      done
}

stream_forge() {
  local desc="$1"
  local repo="${2:-./codex_build}"
  echo "🛠 Forging: $desc"
  echo "📁 Repo:   $repo"
  echo
  curl -s -N -X POST "$API_URL/forge_stream"       -H "Content-Type: application/json"       -d "{"description": "$desc", "repo_path": "$repo"}" |   while IFS= read -r line; do
      if [[ "$line" == event:* ]]; then
          evt="${line#event: }"
          read -r data_line || break
          data="${data_line#data: }"
          read -r _ || true
          case "$evt" in
            stage)        echo "➡️  $data" ;;
            architecture) echo -e "📐 Architecture:\n$data\n" ;;
            file)         echo "📄 $data" ;;
            test)         echo "🧪 $data" ;;
            test_result)  echo "✅ $data" ;;
            git)          echo "🔗 $data" ;;
            done)         echo -e "\n✨ $data" ;;
            error)        echo -e "\n❌ $data" >&2 ;;
            *)            echo "$evt: $data" ;;
          esac
      fi
  done
}

case "$1" in
  infer)   shift; stream_infer "$*" ;;
  agent)   shift; curl -s -X POST "$API_URL/agent"   -H "Content-Type: application/json" -d "{"prompt": "$*"}" | jq -r '.response' ;;
  council) shift; stream_council "$*" ;;
  forge)   shift; stream_forge "$1" "$2" ;;
  *)
    cat <<USAGE
Usage:
  $(basename "$0") infer "your prompt here"       # streamed output
  $(basename "$0") agent "your prompt here"
  $(basename "$0") council "your question here"   # role-by-role output
  $(basename "$0") forge "Project description" [repo]
USAGE
    ;;
esac
