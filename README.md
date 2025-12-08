# Processing Tools - GitHub

Lightweight utilities for managing and monitoring GitHub repositories.

## Quick Start

### Prerequisites

1. Install GitHub CLI:
   ```bash
   brew install gh
   gh auth login
   ```

2. Install PyYAML:
   ```bash
   pip3 install PyYAML
   ```

### Run the Script

```bash
cd github-utils
python3 list_repos_prs.py
```

That's it! The script will generate `open-prs.csv` in the same directory.

## GitHub Utils

Located in `github-utils/`, these tools help manage pull requests and repository information.

### Scripts

#### `list_repos_prs.py`

Python script that generates a CSV report of open pull requests across configured repositories.

**Usage:**
```bash
# Run directly
cd github-utils
python3 list_repos_prs.py > open-prs.csv

# Or with virtual environment active
cd github-utils
python list_repos_prs.py > open-prs.csv
```

**Requirements:**
- Python 3.11+
- `gh` - GitHub CLI (must be authenticated)
- PyYAML (install via `requirements.txt`)

**Output:**
CSV file with the following columns:
- `repo` - Repository name
- `pr_id` - Pull request number
- `title` - PR title
- `date_created` - Creation timestamp
- `url` - PR URL
- `author` - PR author login
- `ci_status` - CI status (ok/failed)

### GitHub Actions

The workflow `.github/workflows/open-prs.yaml` automatically:
1. Runs daily at 4 AM UTC
2. Generates PR reports
3. Splits reports into Konflux PRs and Others
4. Commits and pushes the updated markdown reports

The workflow can also be triggered manually via `workflow_dispatch`.

## Configuration

Repository configuration is stored in `github-utils/repos.yaml`.

Simple YAML format with a list of repositories:
```yaml
github_repos:
  - owner/repo-name
  - another-owner/another-repo
```

Just add or remove repository paths (format: `owner/repository-name`) to update which repos are monitored.
