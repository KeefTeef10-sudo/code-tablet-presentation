#!/usr/bin/env bash
echo "🔍 Searching for files over 500MB..."
find / -type f -size +500M -exec ls -lh {} \; 2>/dev/null
echo "⚠️  To delete a file, run: rm /path/to/file"
