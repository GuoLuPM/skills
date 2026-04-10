# Installing GuoLuPM Skills For Codex

Paste this into Codex:

`Use skill-installer to install the skill \`manual-frontend-debugging\` from GitHub repo \`GuoLuPM/skills\`, then remind me to restart Codex.`

This repo currently contains one frontend debug-only skill. It does not provide design or UI generation skills.

## Option 1: Install The Whole Collection

1. Clone the repository:

```bash
git clone https://github.com/GuoLuPM/skills.git ~/.codex/guolupm-skills
```

2. Create the discovery symlink:

```bash
mkdir -p ~/.agents/skills
ln -s ~/.codex/guolupm-skills ~/.agents/skills/guolupm-skills
```

### Windows

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\guolupm-skills" "$env:USERPROFILE\.codex\guolupm-skills"
```

3. Restart Codex so it discovers the skills.

## Option 2: Install One Skill

If you only want one skill, use the built-in installer:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuoLuPM/skills \
  --path manual-frontend-debugging
```

Then restart Codex.

## Verify

For the whole collection install:

```bash
ls -la ~/.agents/skills/guolupm-skills
```

For single-skill install:

```bash
ls -la ~/.codex/skills/manual-frontend-debugging
```
