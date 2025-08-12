#!/usr/bin/env bash
set -e
sudo apt-get update -y >/dev/null 2>&1 || true
if ! command -v inotifywait >/dev/null 2>&1; then
  sudo apt-get install -y inotify-tools
fi
cd "$(dirname "$0")/.."
echo "👁️  Watching $(pwd) for changes… (Ctrl+C to stop)"
while inotifywait -e modify,create,delete,move -r .; do
  git add -A
  git commit -m "autosync: $(date -Iseconds)" || true
  git push -u origin "$(git rev-parse --abbrev-ref HEAD)" || true
done
