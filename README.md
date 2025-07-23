# Central Daily Reports

This repository manages daily reports for multiple GitHub repositories.

## Configuration

Edit `repos-config.json` to add/remove repositories:

```json
{
  "repositories": [
    {
      "name": "organization/repository-name",
      "enabled": true
    }
  ]
}
```

## Manual Execution

- **Run for enabled repositories only**: Use "Run workflow" button
- **Run for all repositories**: Use "Run workflow" with "force_all" = true

## Repository List Management

The `repo-list-management.yml` workflow provides utilities for managing and inspecting the repository configuration.

### Description

This workflow allows you to inspect and validate your repository configuration without modifying it. It provides three main actions:
- List all enabled repositories
- List all repositories with their status
- Validate the configuration file format

### Usage

To use the Repository List Management workflow:

1. Go to the "Actions" tab in your GitHub repository
2. Select "Manage Repository List" workflow
3. Click "Run workflow"
4. Choose your desired action:
   - **list-enabled**: Shows only repositories that are currently enabled
   - **list-all**: Shows all repositories with their enabled/disabled status
   - **validate-config**: Validates the JSON format and shows statistics
5. Optionally, enter a specific repository name to check its status
6. Click "Run workflow" to execute

The workflow will output the results in the workflow log, making it easy to review your current configuration.

## Adding a New Repository

1. Add entry to `repos-config.json`
2. Set `enabled: true`
3. Commit changes
4. Next scheduled run will include the new repository

## Secrets Required

- `PSONO_API_KEY_ID`
- `PSONO_API_SECRET_KEY_HEX` 
- `PSONO_GITHUB_CLI_TOKEN`
- `PSONO_DAILY_REPORT_ACTION_ENV`

## Variables Required

- `PSONO_SERVER_URL`