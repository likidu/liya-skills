# Scripts

Utility scripts for managing Claude Code skills development.

## setup-skill-link

Creates or removes symlinks between your skill source folder and `.claude/skills/` for local testing.

### Why Symlinks?

When developing a Claude Code skill, you need the skill files in `.claude/skills/<skill-name>/` for Claude to load them. Instead of copying files back and forth, a symlink lets you edit files in one place and have changes reflected immediately.

```
my-agent-skills/
├── tidb-cloud-e2e-validation/     # Source (edit here)
│   ├── SKILL.md
│   └── references/
└── .claude/skills/
    └── tidb-cloud-e2e-validation/ # Symlink → points to source
```

### Usage

#### Windows (PowerShell)

```powershell
# Create symlink (may need Admin or Developer Mode)
.\scripts\setup-skill-link.ps1 add

# Remove symlink
.\scripts\setup-skill-link.ps1 remove

# For a different skill
.\scripts\setup-skill-link.ps1 add my-other-skill
```

**Note**: On Windows, creating symlinks requires either:
- Running PowerShell as Administrator, OR
- Enabling Developer Mode: Settings → Privacy & Security → For developers → Developer Mode

#### macOS / Linux

```bash
# Make script executable (first time only)
chmod +x scripts/setup-skill-link.sh

# Create symlink
./scripts/setup-skill-link.sh add

# Remove symlink
./scripts/setup-skill-link.sh remove

# For a different skill
./scripts/setup-skill-link.sh add my-other-skill
```

### Features

- **Backup existing folders**: If `.claude/skills/<skill-name>` already exists as a real folder, it's backed up to `.claude/skills/<skill-name>.backup`
- **Restore on remove**: When removing the symlink, any backup folder is automatically restored
- **Relative paths**: Uses relative symlinks so the repo can be moved without breaking links
- **Idempotent**: Safe to run multiple times

### Troubleshooting

#### Windows: "You do not have permission to create a symbolic link"

Enable Developer Mode:
1. Open **Settings**
2. Go to **Privacy & Security** → **For developers**
3. Enable **Developer Mode**

Or run PowerShell as Administrator.

#### macOS: "Operation not permitted"

This shouldn't happen for symlinks in user directories, but if it does:
```bash
# Check if the target exists and remove it first
rm -rf .claude/skills/tidb-cloud-e2e-validation
./scripts/setup-skill-link.sh add
```
