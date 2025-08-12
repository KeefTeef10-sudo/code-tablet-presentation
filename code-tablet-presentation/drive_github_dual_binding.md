# Dual-Binding: Google Drive + GitHub

1. Mount Drive (Colab or google-drive-ocamlfuse).
2. Put this project under `~/gdrive/Codex/`.
3. `git init`, set username/email, add `.gitignore`.
4. Create a private GitHub repo and set `origin` remote.
5. (Optional) Install `extras/post-commit.sample` as `.git/hooks/post-commit` for auto-push.
6. (Optional) Run `extras/codex-autosync.sh` for background auto-commit+push on changes.

**CLI Alias:**
```bash
alias codex="$HOME/gdrive/Codex/living_codex/codex.sh"
```

**Environment for auto-push during forge:**
```bash
export CODEX_PUSH=1
export CODEX_REMOTE=origin
```
