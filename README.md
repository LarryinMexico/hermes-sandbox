# Hermes Sandbox

A personal AI coding agent that lives in GitHub Codespaces and responds via Telegram.

## What it does

Send a project idea from Telegram → Hermes asks clarifying questions → you confirm → it researches, codes, tests, and creates a new GitHub repo automatically.

## Architecture

```
Telegram ──► Hermes Agent (Codespaces) ──► OpenRouter (Gemma 4 free)
                    │
                    └──► GitHub CLI → creates new repos on your account
```

## Required Codespaces Secrets

Set at: **GitHub → Profile Settings → Codespaces → Secrets**

| Secret | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | From BotFather |
| `OPENROUTER_API_KEY` | From openrouter.ai (free) |
| `GH_PAT` | GitHub PAT with `repo` + `workflow` scope |

## Setup

1. Add the three secrets above
2. Open a Codespace on this repo
3. Wait for `postCreateCommand` to finish installing Hermes (~2 min)
4. Run: `hermes setup` → choose OpenRouter → model: `google/gemma-4-31b-it:free`
5. Run: `hermes gateway setup` → choose Telegram → enter bot token
6. Run: `hermes gateway` to start (auto-starts on future boots)

## Memory Warning

Hermes memories and skills are stored in `~/.hermes/` inside the Codespace.  
**Pausing** the Codespace preserves them. **Deleting** it loses them.  
To back up memories: `cp -r ~/.hermes/memory /workspaces/hermes-sandbox/memory-backup/`
