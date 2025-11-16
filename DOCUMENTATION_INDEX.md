# Documentation Index

Quick navigation guide for askmyuni-supportsystems project documentation.

## Start Here

**New to this project?** Start with these in order:

1. **[README.md](README.md)** - Project overview and quick start
2. **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step setup (5 min read)
3. **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Pre-import verification checklist

## For Different Roles

### For AI Coding Agents

→ **[.github/copilot-instructions.md](.github/copilot-instructions.md)**

Comprehensive architecture guide including:
- Three-stage pipeline architecture
- Code organization patterns
- Error handling patterns
- API integration details
- Testing requirements
- Critical commands

### For First-Time Users

1. [QUICKSTART.md](QUICKSTART.md) - 5-step setup guide
2. [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Verification checklist
3. [config/template.csv](config/template.csv) - Example CSV format

### For Developers

1. [CONTRIBUTING.md](CONTRIBUTING.md) - Development workflow and commands
2. [.github/copilot-instructions.md](.github/copilot-instructions.md) - Architecture
3. [config/mappings.yaml](config/mappings.yaml) - Configuration reference
4. Source code: `src/*.py` - Implementation files

### For Operators / DevOps

1. [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Pre-flight checklist
2. [QUICKSTART.md](QUICKSTART.md) - Quick start commands
3. [.env.example](.env.example) - Environment configuration

## File Structure

```
askmyuni-supportsystems/
├── Documentation
│   ├── README.md                      ← Project overview
│   ├── QUICKSTART.md                  ← 5-step setup guide
│   ├── CONTRIBUTING.md                ← Development workflow
│   ├── SETUP_CHECKLIST.md             ← Pre-import checklist
│   ├── SETUP_SUMMARY.txt              ← This session's summary
│   ├── DOCUMENTATION_INDEX.md          ← You are here
│   └── .github/copilot-instructions.md ← AI Agent guide (PRIMARY)
│
├── Configuration
│   ├── .env.example                   ← Environment template
│   ├── config/
│   │   ├── template.csv               ← Example import file
│   │   └── mappings.yaml              ← Field mappings & rules
│   └── requirements.txt               ← Python dependencies
│
├── Source Code (Python)
│   └── src/
│       ├── cli.py                     ← Command-line interface
│       ├── csv_handler.py             ← CSV reading & parsing
│       ├── validators.py              ← Business rule validation
│       ├── github_client.py           ← GitHub API wrapper
│       └── issue_mapper.py            ← CSV → GitHub mapping
│
└── Test & Data
    ├── tests/                         ← Test suite (to implement)
    ├── data/                          ← Input CSV files (user-created)
    └── setup.sh                       ← Setup automation script
```

## Key Commands

### Validation Only (No Import)
```bash
# Format check only
python src/cli.py validate --csv data/import.csv --dry-run

# Full validation with GitHub checks
python src/cli.py validate --csv data/import.csv
```

### Preview Before Import
```bash
python src/cli.py preview --csv data/import.csv
```

### Import to GitHub
```bash
# With confirmation prompt
python src/cli.py import --csv data/import.csv

# Skip confirmation
python src/cli.py import --csv data/import.csv --confirm
```

## CSV Format Reference

Required columns (in any order):
| Column | Type | Required | Default |
|--------|------|----------|---------|
| Title | string | Yes | — |
| Description | string | Yes | — |
| Type | Epic\|Task | Yes | — |
| Labels | string (;-separated) | No | — |
| Assignee | GitHub username | No | — |
| Milestone | string | No | — |
| Repository | repo name | No | primary repo |

See [config/template.csv](config/template.csv) for example.

## Important Links

### GitHub Targets
- **Project #2**: https://github.com/users/nimeshe/projects/2
- **Primary Repo**: https://github.com/nimeshe/askmyuni-supportsystems
- **Secondary Repo**: https://github.com/nimeshe/askmyuni-main

### Configuration
- **GitHub Token**: https://github.com/settings/tokens
- **Project Settings**: https://github.com/users/nimeshe/projects/2/settings
- **Repo Labels**: Settings → Labels in each repository
- **Repo Milestones**: Settings → Milestones in each repository

## Architecture at a Glance

```
CSV Input
   ↓
[Stage 1: Read & Validate]
   - Parse CSV structure
   - Validate headers
   - Report format errors
   ↓
[Stage 2: Enrich & Validate]
   - Check GitHub users
   - Verify labels/milestones
   - Validate relationships
   ↓
[Stage 3: Import to GitHub]
   - Create Epics in Project
   - Create Issues in repos
   - Set metadata (labels, assignees)
   - Link cross-repo references
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "GitHub token not found" | Check `.env` file has `GITHUB_TOKEN=ghp_...` |
| "User not found" | Verify GitHub username is correct |
| "Label not found" | Labels auto-create or pre-create in repo settings |
| "CSV parsing error" | Check format matches `config/template.csv` |
| Rate limit exceeded | Wait before retry (PAT allows 5000/hour) |

See [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) for detailed troubleshooting.

## Common Tasks

**How do I...?**

- **Set up the environment?** → [QUICKSTART.md](QUICKSTART.md)
- **Create a CSV file?** → [config/template.csv](config/template.csv)
- **Validate before importing?** → See "Key Commands" section above
- **Understand the architecture?** → [.github/copilot-instructions.md](.github/copilot-instructions.md)
- **Develop new features?** → [CONTRIBUTING.md](CONTRIBUTING.md)
- **Check if I'm ready to import?** → [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)

## What Was Created

This session created:
- ✅ AI Agent instructions (`.github/copilot-instructions.md`)
- ✅ 5 documentation files (README, QUICKSTART, CONTRIBUTING, CHECKLIST, INDEX)
- ✅ 5 Python source modules (CSV handler, validators, GitHub client, mapper, CLI)
- ✅ Configuration templates (env, YAML, CSV)
- ✅ Directory structure and requirements file

Everything is ready for development and import!

## Next Steps

1. Read [QUICKSTART.md](QUICKSTART.md) for 5-step setup
2. Complete [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
3. Prepare your CSV file using [config/template.csv](config/template.csv)
4. Run validation: `python src/cli.py validate --csv data/import.csv --dry-run`
5. Execute import: `python src/cli.py import --csv data/import.csv`

---

**Questions?** Check the relevant documentation above or see troubleshooting section.
