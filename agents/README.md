# Vitiflow agents/

This directory is the **agent workspace** for the Vitiflow partner repo.

It is cloned on CT 231 to `/opt/vitiflow` (or `/workspace/vitiflow` inside the hermes-grok container).

## Purpose

- Source of truth for code changes, specs, runbooks, and agent memory via Git.
- Paired with the Obsidian AI Brain vault (`/opt/ai-brain` via Nextcloud) for notes, context, handoffs, and logs.

## Key files for agents

- `SOUL.md` — Core instructions / personality / routing rules for the `hermes-grok` agent.
- `prompts/` — Reusable prompts (e.g. grok-build-orchestrator.md).
- `runbooks/` — Execution plans and dated notes (start with `grok-hermes-pi-plan.md`).
- `workspace/` — Scratch / active work area (gitignored or for temp clones).

## How to use (desktop)

1. Edit here with Grok Build.
2. Commit + push to the Vitiflow GitHub repo.
3. On the Pi side, the agent pulls or works directly in the mounted clone.

## How the Pi agent uses it

See `SOUL.md` and the main plan `runbooks/grok-hermes-pi-plan.md`.

General homelab conventions: always start by reading `/opt/homelab-agentic/guidelines/agentic-homelab-guidelines.md`.

## Related

- AI Brain vault: `ai-brain/` in Nextcloud (mounted at `/opt/ai-brain`)
- Homelab harness: `/opt/homelab-agentic/`
- Existing ERP Hermes: unchanged responsibilities.
