# Contributing to askmyuni-supportsystems

## Development Setup

### Prerequisites
- Python 3.8+
- GitHub PAT (Personal Access Token) with `repo` and `project` scopes

### Quick Start

```bash
# Clone repository
git clone https://github.com/nimeshe/askmyuni-supportsystems.git
cd askmyuni-supportsystems

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your GitHub token and settings
```

## Development Workflow

### 1. Validate a CSV File (Dry Run)
```bash
python src/cli.py validate --csv data/import.csv --dry-run
```

This performs **Stage 1** validation:
- Reads CSV structure
- Validates required columns
- Reports format errors with line numbers
- Does NOT make any GitHub API calls

### 2. Preview Issues to Be Created
```bash
python src/cli.py preview --csv data/import.csv
```

Shows what will be created before importing.

### 3. Full Validation + Enrichment (No Import)
```bash
python src/cli.py validate --csv data/import.csv
```

This adds **Stage 2** validation:
- Validates assignees exist in GitHub
- Checks labels exist in target repos
- Reports warnings about missing metadata

### 4. Import to GitHub
```bash
python src/cli.py import --csv data/import.csv
# Review preview, then confirm when prompted

# Or skip confirmation
python src/cli.py import --csv data/import.csv --confirm
```

This executes **Stage 3**:
- Creates Epics in GitHub Project
- Creates Issues in both repos
- Links parent-child relationships
- Sets labels, assignees, milestones

## CSV Format

See `config/template.csv` for example. Required columns:

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| Title | string | Yes | Issue title |
| Description | string | Yes | Issue body/description |
| Type | string | Yes | `Epic` or `Task` |
| Labels | string | No | Semicolon-separated (e.g., `bug;enhancement`) |
| Assignee | string | No | GitHub username |
| Milestone | string | No | Milestone name |
| Repository | string | No | Target repo (defaults to askmyuni-supportsystems) |

## Configuration Files

- **`.env`** - Environment variables (GitHub token, org, repo names)
- **`config/mappings.yaml`** - Field mappings and validation rules
- **`config/template.csv`** - Example import file

## Code Structure

- **`src/csv_handler.py`** - CSV reading and parsing
- **`src/validators.py`** - Business rule validation
- **`src/github_client.py`** - GitHub REST API wrapper
- **`src/issue_mapper.py`** - CSV-to-GitHub mapping
- **`src/cli.py`** - Command-line interface

## Error Handling

All modules return structured error dicts:
```python
{
  "row": 5,           # Row number (0 for header errors)
  "field": "Type",    # Column name
  "message": "...",   # Human-readable error
  "severity": "warn"  # "error" or "warn"
}
```

## Testing

Run tests (when implemented):
```bash
pytest tests/
```

Test structure:
- `tests/test_csv_handler.py` - CSV parsing validation
- `tests/test_validators.py` - GitHub validation (mocked API)
- `tests/test_github_client.py` - API integration tests
- `tests/fixtures/` - Sample CSV files and mock responses

## Debugging

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python src/cli.py validate --csv data/import.csv
```

## Common Issues

### "GitHub token not found"
```bash
# Check .env file
cat .env
# Should contain: GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

### "User 'xxx' not found"
Verify username exists: `gh api users/username`

### "Rate limit exceeded"
GitHub API has rate limits. Wait before retry or use PAT for higher limits.

## Best Practices

1. **Always use `--dry-run` first** - Test CSV before importing
2. **Review preview** - Check what will be created
3. **Validate independently** - Use validation-only mode for safety
4. **Use meaningful labels** - Helps with filtering and searching
5. **Link to project** - Always include `ask-myuni` label

## Reporting Issues

Include:
- CSV file (if possible)
- Error output
- Environment info (`python --version`, `pip freeze`)
- GitHub org/repo names
