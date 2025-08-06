# Central Repository Management

This repository manages automated workflows for multiple GitHub repositories, including daily reports and stale PR management.

## Configuration

Edit `repos-config.json` to add/remove repositories and configure which services are enabled:

```json
{
  "repositories": [
    {
      "name": "organization/repository-name",
      "enabled": [
        "github-daily-report",
        "mark-and-close-stale-prs"
      ]
    }
  ]
}
```

### Available Services

- **`github-daily-report`**: Generates automated daily reports for repository activity
- **`mark-and-close-stale-prs`**: Automatically marks and closes stale pull requests

## Manual Execution

### Daily Reports Workflow
- **Run for repositories with daily reports enabled**: Use "Run workflow" button
- **Run for all repositories**: Use "Run workflow" with "force_all" = true

### Stale PR Management
The stale PR management runs automatically based on the configuration in `repos-config.json`. Only repositories with `"mark-and-close-stale-prs"` in their enabled services will be processed.

## Repository List Management

The `repo-list-management.yml` workflow provides utilities for managing and inspecting the repository configuration.

### Description

This workflow allows you to inspect and validate your repository configuration without modifying it. It provides three main actions:
- List repositories with daily reports enabled
- List all repositories with their enabled services
- Validate the configuration file format

### Usage

To use the Repository List Management workflow:

1. Go to the "Actions" tab in your GitHub repository
2. Select "Manage Repository List" workflow
3. Click "Run workflow"
4. Choose your desired action:
   - **list-enabled**: Shows repositories with daily reports enabled
   - **list-all**: Shows all repositories with their enabled services
   - **validate-config**: Validates the JSON format and shows statistics
5. Optionally, enter a specific repository name to check its status
6. Click "Run workflow" to execute

The workflow will output the results in the workflow log, making it easy to review your current configuration.

## Adding a New Repository

1. Add entry to `repos-config.json`
2. Specify which services to enable in the `enabled` array:
   - Add `"github-daily-report"` for daily reports
   - Add `"mark-and-close-stale-prs"` for stale PR management
3. Commit changes
4. Next scheduled run will include the new repository with enabled services

### Example Configuration

```json
{
  "name": "your-org/new-repository",
  "enabled": [
    "github-daily-report",
    "mark-and-close-stale-prs"
  ]
}
```

## Secrets Required

- `PSONO_API_KEY_ID`
- `PSONO_API_SECRET_KEY_HEX` 
- `PSONO_GITHUB_CLI_TOKEN`
- `PSONO_DAILY_REPORT_ACTION_ENV`

## Variables Required

- `PSONO_SERVER_URL`