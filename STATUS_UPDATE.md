# Project Status Update - November 16, 2025

## Overall Status

### Goal: Add Epics and Sub Tasks to GitHub
**Current State**: ❌ **Not Complete** — we have the infrastructure but haven't executed the import yet.

### What Exists Now

✅ **Documentation & Setup**
- `.github/copilot-instructions.md` — AI agent guide
- Full documentation suite (README, QUICKSTART, CONTRIBUTING, etc.)
- Configuration files (`.env.example`, `config/mappings.yaml`)

✅ **Python Import Pipeline** (5 modules in `src/`)
- `csv_handler.py` — CSV reading/parsing
- `validators.py` — Business rule validation  
- `github_client.py` — GitHub API wrapper
- `issue_mapper.py` — CSV-to-GitHub mapping
- `cli.py` — Command-line interface

✅ **Your Data**
- `config/rawdata.csv` — Your Epics (D1-D4) + 29 sub-tasks with Status/Labels/Parent columns

### What's Missing

❌ **The converter script** — We discussed creating `scripts/convert_raw_to_import.py` to transform `rawdata.csv` (columns: Title, Description, Status, Labels, Parent) into `data/import.csv` (columns: Title, Description, Type, Labels, Assignee, Milestone, Repository) but **never created it**.

❌ **The actual import** — Issues haven't been created in GitHub yet.

---

## Why the Code is Complex

The existing pipeline was designed for a different CSV format and includes:
- GitHub API validation (users, labels, milestones)
- Error handling with row-level reporting
- Dry-run/preview modes
- Rollback capability

**For your one-off task**, this is overkill. You just need to:
1. Convert `rawdata.csv` → `import.csv` (add Type/Repository columns)
2. Run the import

---

## What You Need to Do Next

### Option 1: Simplest Path (Recommended for One-Off)
Create a minimal Python script that directly reads `config/rawdata.csv` and creates issues via GitHub API:

```bash
# Install dependencies
pip install requests python-dotenv

# Set GitHub token in .env
echo "GITHUB_TOKEN=ghp_your_token_here" > .env
echo "GITHUB_ORG=nimeshe" >> .env

# Run the simple import script (I'll create this for you)
python scripts/simple_import.py
```

**Time: ~5 minutes** to create the script + run it.

### Option 2: Use Existing Pipeline (More Work)
1. Create converter: `scripts/convert_raw_to_import.py`
2. Run: `python scripts/convert_raw_to_import.py` → generates `data/import.csv`
3. Run: `python src/cli.py import --csv data/import.csv --confirm`

**Time: ~15 minutes** (more validation but overkill for this task).

---

## VS Code Popup Issue

**Cause**: GitHub authentication prompt from either:
- GitHub Copilot extension trying to authenticate
- GitHub Pull Requests extension
- `gh` CLI tool in the devcontainer

**Fix for Your Laptop**:

### Before You Switch Machines

1. **Check GitHub auth status**:
```bash
gh auth status
```

2. **If not authenticated**, auth with token (no browser):
```bash
# Use your GitHub PAT
export GITHUB_TOKEN="ghp_XXXXXXXXXXXXXXXX"
echo "$GITHUB_TOKEN" | gh auth login --with-token
```

3. **Disable browser prompts** (add to `.bashrc` or `.env`):
```bash
export BROWSER=echo  # Shows URLs instead of trying to open them
```

### On Your Laptop (Moving Workspace)

1. **Clone/sync the repo**:
```bash
git clone https://github.com/nimeshe/askmyuni-supportsystems.git
cd askmyuni-supportsystems
```

2. **Open in VS Code devcontainer** (if using):
   - VS Code will prompt to "Reopen in Container"
   - Or: `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

3. **Set up GitHub token**:
```bash
cp .env.example .env
nano .env  # Add your GITHUB_TOKEN
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Authenticate gh CLI** (prevents popup):
```bash
echo "$GITHUB_TOKEN" | gh auth login --with-token
```

---

## My Recommendation

**Let me create a simple `scripts/simple_import.py`** that:
- Reads `config/rawdata.csv`
- Creates Epics first (rows with Parent empty)
- Creates sub-tasks with parent references
- Uses your GitHub token from `.env`
- Adds everything to both repos + Project #2

This will be **~100 lines** instead of the 500+ line pipeline, and will finish your task in 5 minutes.

**Next Action**: Create `scripts/simple_import.py` and run it to complete the import.

---

## Target Destinations

- **GitHub Project**: https://github.com/users/nimeshe/projects/2
- **Primary Repo**: https://github.com/nimeshe/askmyuni-supportsystems (this repo)
- **Secondary Repo**: https://github.com/nimeshe/askmyuni-main

---

## Summary

- **Infrastructure**: ✅ Complete
- **Data Ready**: ✅ `config/rawdata.csv` has all Epics and tasks
- **Import Script**: ❌ Needs to be created
- **Execution**: ❌ Not run yet

**Estimated Time to Complete**: 5-10 minutes once the simple import script is created and GitHub token is configured.
