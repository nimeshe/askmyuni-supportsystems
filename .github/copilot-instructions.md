# Ask My Uni Support Systems - AI Agent Instructions

## Project Overview

**Purpose**: Support subsystem for the Ask My Uni Agentic System project. This repo implements data import workflows that read CSV files, validate them, and import Epics/Issues into GitHub Project and multiple repositories.

**Target Repositories**:
- Primary: `nimeshe/askmyuni-supportsystems` (this repo)
- Secondary: `nimeshe/askmyuni-main`

**GitHub Project**: https://github.com/users/nimeshe/projects/2

## Subsystem 1: CSV Import Pipeline

### Architecture Overview

The primary subsystem performs a three-stage workflow:

```
CSV Input → Validation → GitHub Import
     ↓
  - Read CSV
  - Validate format
  - Report errors
  
     ↓
  - Validate against import template
  - Enrich with repo/project info
  - Check constraints
  
     ↓
  - Create Epics (parent issues) in Project
  - Create Sub-Items in both repos
  - Link issues cross-repo
```

### Stage 1: CSV Reading & Validation

**Objective**: Read CSV, validate structure, detect format errors early.

**Requirements**:
- Accept CSV input with columns: `Title`, `Description`, `Type` (Epic/Task), `Labels`, `Assignee`, `Milestone`
- Validate column headers match import template
- Report parsing errors with line numbers and field names
- Handle missing required fields gracefully

**Implementation Notes**:
- Prefer Python (`csv` module or `pandas`) for flexible validation
- Use structured error reporting (list errors, don't fail on first one)
- Support CSV preview before full import

### Stage 2: Enrichment & Validation

**Objective**: Validate data against business rules, enrich with GitHub metadata.

**Requirements**:
- Validate Epics exist or can be created in Project
- Map assignees to GitHub user logins
- Verify labels exist in target repos or create them
- Check for duplicate issues
- Validate parent-child relationships (Epic → Sub-Items)

**Key Constraints**:
- Epic items must exist in GitHub Project first
- Sub-Items can be distributed across both repos
- Cross-repo linking via issue references (#owner/repo#issue)
- All issues require a valid assignee (or validate as optional per config)

### Stage 3: GitHub Import

**Objective**: Create issues in GitHub Project and repos with proper relationships.

**Requirements**:
- Use GitHub REST API v3 (or GraphQL for batch operations)
- Create Epics in Project with proper field mapping
- Create Issues in repos with parent Epic links
- Set labels, assignees, milestones atomically
- Handle API rate limits (60 req/min unauthenticated, 5000 req/hour authenticated)

**API Integration**:
```python
# Required: GitHub token (PAT) with 'repo', 'project' scopes
# Environment: GH_TOKEN or .env GITHUB_TOKEN
# Endpoints:
# - POST /repos/{owner}/{repo}/issues
# - PATCH /repos/{owner}/{repo}/issues/{issue_number}
# - POST /projects/{project_id}/columns/{column_id}/cards
```

## Configuration Requirements

### Required Files

1. **Environment Configuration** (`.env` or `config.py`):
   ```
   GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   GITHUB_ORG=nimeshe
   PRIMARY_REPO=askmyuni-supportsystems
   SECONDARY_REPO=askmyuni-main
   PROJECT_ID=2
   ```

2. **CSV Import Template** (`data/import-template.csv` or schema):
   - Document expected columns and types
   - Provide example CSV with valid entries
   - List validation rules for each field

3. **Mapping Configuration** (`config/mappings.yaml`):
   - Epic label mappings
   - Repo assignment rules (which issues go to which repo)
   - Field aliases for different CSV sources

### GitHub Prerequisites

- Both repos (`askmyuni-supportsystems`, `askmyuni-main`) must exist
- Project ID `2` must exist and be accessible
- Create project columns if using custom workflow states
- Pre-populate common labels in both repos

## Development Patterns

### Code Organization (Python Preferred)

```
src/
  ├── csv_handler.py       # Read, parse, validate CSV
  ├── validators.py        # Business rule validation
  ├── github_client.py      # GitHub API wrapper
  ├── issue_mapper.py       # Map CSV rows → GitHub issues
  └── cli.py              # Command-line interface

config/
  ├── mappings.yaml       # Field mappings
  └── template.csv        # Example import file

tests/
  ├── test_csv_handler.py
  ├── test_validators.py
  └── test_github_client.py
```

### Error Handling Pattern

All validation stages should collect errors and return a summary:
```python
{
  "valid": False,
  "errors": [
    {"row": 5, "field": "Type", "message": "Invalid type 'Bug', must be 'Epic' or 'Task'"},
    {"row": 7, "field": "Assignee", "message": "User 'unknown' not found in GitHub"}
  ],
  "warnings": [
    {"row": 3, "message": "Milestone 'v1.0' doesn't exist, will create"}
  ]
}
```

### Testing Requirements

- Unit tests for CSV parsing (valid, malformed, missing columns)
- Validator tests with mock GitHub API responses
- Integration tests against GitHub (use test repos/project)
- Example CSV files in `tests/fixtures/`

## Critical Commands

### Run Validation Only (Dry Run)
```bash
python src/cli.py validate --csv data/import.csv --dry-run
```

### Import with Confirmation
```bash
python src/cli.py import --csv data/import.csv --confirm
```

### Preview Issues to Be Created
```bash
python src/cli.py preview --csv data/import.csv
```

### Rollback Last Import
```bash
python src/cli.py rollback --last-import-id <id>
```

## Key Files to Understand

- **README.md**: Project overview and subsystem documentation
- **config/template.csv**: Sample valid CSV for import
- **src/github_client.py**: All GitHub API interactions
- **.env.example**: Template for required environment variables

## Integration with Ask My Uni Main

When importing to Project #2:
- Epics should be created with `ask-myuni` label
- Issues in `askmyuni-main` should link back to this repo via cross-repo references
- Maintain consistent milestone naming across both repos

## Next Steps for Completion

1. **GitHub API Setup**: Create PAT token with `repo` + `project` scopes
2. **CSV Template**: Define exact columns and validation rules
3. **Dependency Installation**: `pip install requests pyyaml pandas`
4. **Testing**: Verify against test project before production import
5. **Documentation**: Add CONTRIBUTING.md with workflow examples
