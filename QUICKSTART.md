# Quick Setup Guide

This page helps you quickly set up and start using the CSV Import Pipeline.

## 1. Prerequisites

- **Python 3.8+**
- **GitHub Account** with access to:
  - `nimeshe/askmyuni-supportsystems` repo
  - `nimeshe/askmyuni-main` repo
  - Project #2 (https://github.com/users/nimeshe/projects/2)

## 2. Create GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `askmyuni-import`
4. Scopes: Select `repo` and `project`
5. Copy the token (keep it secret!)

## 3. Environment Setup

```bash
# Clone this repo
git clone https://github.com/nimeshe/askmyuni-supportsystems.git
cd askmyuni-supportsystems

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your token
nano .env
# Replace ghp_xxxxxxxxxxxx with your actual token
```

## 4. Prepare CSV Data

Create your CSV file with the required columns:

```csv
Title,Description,Type,Labels,Assignee,Milestone,Repository
User Authentication,Enable secure login,Epic,security;ask-myuni,username,v1.0,askmyuni-supportsystems
```

**Column Requirements**:
- `Title` (required): Issue title
- `Description` (required): Issue description
- `Type` (required): `Epic` or `Task`
- `Labels` (optional): Semicolon-separated labels
- `Assignee` (optional): GitHub username
- `Milestone` (optional): Milestone name
- `Repository` (optional): `askmyuni-supportsystems` or `askmyuni-main`

See `config/template.csv` for a complete example.

## 5. Validate CSV Before Importing

```bash
# Validate format only (no GitHub API calls)
python src/cli.py validate --csv data/import.csv --dry-run

# Output will show errors if any
```

## 6. Preview What Will Be Created

```bash
# See all issues that will be created
python src/cli.py preview --csv data/import.csv
```

## 7. Import to GitHub

```bash
# Import with confirmation prompt
python src/cli.py import --csv data/import.csv

# Or skip confirmation (use with caution!)
python src/cli.py import --csv data/import.csv --confirm
```

## 8. Verify in GitHub

1. Check Project: https://github.com/users/nimeshe/projects/2
2. Check Repos:
   - https://github.com/nimeshe/askmyuni-supportsystems/issues
   - https://github.com/nimeshe/askmyuni-main/issues

## Troubleshooting

### "GitHub token not found" Error
```bash
# Check .env file exists and has GITHUB_TOKEN
cat .env

# Make sure you've set it:
# GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### "User 'xxx' not found" Error
- Verify the GitHub username is correct
- Check the user exists: https://github.com/xxx

### "Label not found" Warning
- Labels will be automatically created in the repository
- Or create them manually first in the repo settings

### CSV Parsing Error
- Check CSV format matches `config/template.csv`
- Ensure no extra commas or missing quotes
- Verify column headers are exact matches

## Next Steps

See `CONTRIBUTING.md` for detailed development information.

## Need Help?

Check the main documentation:
- **Overview**: `README.md`
- **AI Agent Instructions**: `.github/copilot-instructions.md`
- **Configuration Details**: See inline comments in `config/mappings.yaml`
- **Example CSV**: `config/template.csv`
