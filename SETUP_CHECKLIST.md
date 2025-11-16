# Configuration Checklist

Complete this checklist before running the CSV import pipeline.

## GitHub Setup

- [ ] Create GitHub Personal Access Token (PAT)
  - Go to https://github.com/settings/tokens
  - Select scopes: `repo`, `project`
  - Copy token (you'll need it in the next step)

- [ ] Verify access to required repositories
  - [ ] Can access https://github.com/nimeshe/askmyuni-supportsystems
  - [ ] Can access https://github.com/nimeshe/askmyuni-main
  - [ ] Can access Project #2: https://github.com/users/nimeshe/projects/2

## Local Environment

- [ ] Python 3.8+ installed
  ```bash
  python3 --version
  ```

- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```

- [ ] `.env` file created and configured
  ```bash
  cp .env.example .env
  # Edit .env with your GitHub token
  nano .env
  ```

- [ ] Environment variables set
  - [ ] `GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
  - [ ] `GITHUB_ORG=nimeshe` (should be pre-filled)
  - [ ] `PRIMARY_REPO=askmyuni-supportsystems` (should be pre-filled)
  - [ ] `SECONDARY_REPO=askmyuni-main` (should be pre-filled)
  - [ ] `PROJECT_ID=2` (should be pre-filled)

## CSV Preparation

- [ ] CSV file created with required columns
  ```
  Title, Description, Type, Labels, Assignee, Milestone, Repository
  ```

- [ ] Example CSV file: `config/template.csv`
  - Review and use as reference

- [ ] Validate CSV structure
  ```bash
  python src/cli.py validate --csv data/import.csv --dry-run
  ```

## GitHub Repository Setup

- [ ] Common labels exist in both repos (optional)
  - Repository Settings → Labels
  - Create: `ask-myuni`, `bug`, `enhancement`, `documentation`, etc.

- [ ] Milestones exist (if using milestones in CSV)
  - Repository Settings → Milestones
  - Create all referenced milestones in both repos

- [ ] Users exist and are accessible
  - Verify all assignee usernames are valid GitHub users
  - Test: `gh api users/{username}`

## Testing & Validation

- [ ] Test import with dry-run on small CSV
  ```bash
  python src/cli.py validate --csv data/test-small.csv --dry-run
  ```

- [ ] Preview what will be created
  ```bash
  python src/cli.py preview --csv data/test-small.csv
  ```

- [ ] Full validation (includes GitHub API checks)
  ```bash
  python src/cli.py validate --csv data/test-small.csv
  ```

## Import Configuration

- [ ] Decide repo assignment strategy
  - Primary repo: `askmyuni-supportsystems`
  - Secondary repo: `askmyuni-main`
  - Edit CSV `Repository` column or update `config/mappings.yaml`

- [ ] Verify label handling
  - Labels will auto-create in repos if missing
  - Or pre-create in repo Settings → Labels

- [ ] Milestone strategy
  - Create milestones first, or let system create them
  - Configure in `config/mappings.yaml` → `error_handling.on_missing_milestone`

## Production Import

- [ ] Test import on test repository first (if possible)

- [ ] Create backup/reference
  - Keep original CSV file
  - Document any manual changes made

- [ ] Run import
  ```bash
  python src/cli.py import --csv data/import.csv
  ```
  Or with auto-confirm:
  ```bash
  python src/cli.py import --csv data/import.csv --confirm
  ```

- [ ] Verify in GitHub
  - Check Project: https://github.com/users/nimeshe/projects/2
  - Check Issues in both repos
  - Verify labels, assignees, and milestones are set correctly

## Troubleshooting

If you encounter errors, check:

1. **GitHub Token Issues**
   ```bash
   grep GITHUB_TOKEN .env
   # Should show: GITHUB_TOKEN=ghp_xxxxxxxxxxxx (not ghp_xxxxxxxxxxxx)
   ```

2. **CSV Format**
   ```bash
   # Validate CSV
   python src/cli.py validate --csv data/import.csv --dry-run
   ```

3. **User/Label/Milestone Validation**
   - Verify users exist: https://github.com/{username}
   - Check labels in repo Settings
   - Check milestones in repo Settings

4. **Rate Limiting**
   - GitHub API rate limits: 5000 req/hour with PAT
   - If rate limited, wait before retrying

## Support

- Documentation: See `.github/copilot-instructions.md`
- Quick start: See `QUICKSTART.md`
- Development: See `CONTRIBUTING.md`
