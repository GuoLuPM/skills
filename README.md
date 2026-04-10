# GuoLuPM Skills

Public Codex skills. This repo currently contains one frontend debug-only skill and does not provide UI design, page generation, or styling capabilities.

## Paste This Into Codex

`Use skill-installer to install the skill \`manual-frontend-debugging\` from GitHub repo \`GuoLuPM/skills\`, then remind me to restart Codex.`

## Full Repo Install

`Fetch and follow instructions from https://raw.githubusercontent.com/GuoLuPM/skills/main/.codex/INSTALL.md`

## Included Skills

- `manual-frontend-debugging`: A frontend debug-only skill for browser UI bugs that are faster to reproduce manually than through automation.

## Manual Single-Skill Install

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuoLuPM/skills \
  --path manual-frontend-debugging
```

Restart Codex after installation so the new skill is discovered.
