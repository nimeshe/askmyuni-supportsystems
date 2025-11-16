# askmyuni-supportsystems

Support subsystems for the **Ask My Uni Agentic System** project. This repository implements data import workflows for GitHub project and issue management.

## Architecture Overview

### Subsystem 1: CSV Import Pipeline

Enables bulk import of Epics and Issues from CSV files into GitHub Project (#2) and multiple repositories.

**Workflow**:
```
CSV Input
    ↓
[Read & Parse] → Validate format, detect errors
    ↓
[Enrich & Validate] → Check business rules, map to GitHub entities
    ↓
[Import to GitHub] → Create Epics in Project, Issues in repos
```

**Target Destinations**:
- **GitHub Project**: https://github.com/users/nimeshe/projects/2
- **Primary Repo**: https://github.com/nimeshe/askmyuni-supportsystems (this repo)
- **Secondary Repo**: https://github.com/nimeshe/askmyuni-main

## Key Features

- ✅ CSV validation against import template
- ✅ Error reporting with line numbers and field details
- ✅ GitHub API integration for Epics and Sub-Items
- ✅ Cross-repo issue linking
- ✅ Dry-run mode for preview before import
- ✅ Rollback support for failed imports

## Configuration Requirements

See `.github/copilot-instructions.md` for complete setup guide including:
- Environment variables and GitHub token setup
- CSV template specification
- API configuration
- Development patterns

## Quick Start

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env with your GitHub token

# 2. Prepare CSV file
# Use config/template.csv as reference
# Pleae note raw_data.csv which is in the folder as template.csv has raw data. Can you please validate this data, then update csv file, and/or template.csv. Ensure Epics and Child issues are created and relationship created. Ensure Repo is mapped accordingly and project is mapped accordingly
## Repo 1: https://github.com/nimeshe/askmyuni-main
## Reoi 2L https://github.com/nimeshe/askmyuni-supportsystems = Same as tgus repo
## ProjectL https://github.com/users/nimeshe/projects/2


# 3. Validate import
python src/cli.py validate --csv data/import.csv --dry-run

# 4. Execute import
python src/cli.py import --csv data/import.csv --confirm
```

## Project Structure

```
src/
  ├── csv_handler.py       # CSV reading and parsing
  ├── validators.py        # Business rule validation
  ├── github_client.py      # GitHub API integration
  ├── issue_mapper.py       # CSV to GitHub issue mapping
  └── cli.py              # Command-line interface

config/
  ├── mappings.yaml       # Field and repo mappings
  └── template.csv        # Sample import file - I have been given the data. Can you please look at the data, and create the data file. Update data file or template or both as required

tests/
  └── fixtures/           # Test data and mock responses
```

## Dependencies

- Python 3.8+
- `requests` - GitHub API calls
- `pyyaml` - Configuration files
- `pandas` - CSV parsing (optional, for advanced features)

## Contributing

See `.github/copilot-instructions.md` for AI agent guidelines and development patterns.

