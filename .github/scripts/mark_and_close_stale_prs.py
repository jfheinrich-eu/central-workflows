import json
import os
import logging
from datetime import datetime, timezone
from typing import Any
from github import Github
from tabulate import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Konfiguration
CONFIG_PATH: str = "repos-config.json"
DAYS_BEFORE_STALE: int = int(os.environ.get("DAYS_BEFORE_STALE", "30"))
DAYS_BEFORE_CLOSE: int = int(os.environ.get("DAYS_BEFORE_CLOSE", "7"))

# Lade Token und Konfig
token: str = os.environ["GITHUB_TOKEN"]
g: Github = Github(token)

with open(CONFIG_PATH, encoding="utf-8") as f:
    config: dict[str, Any] = json.load(f)

results: list[list[str]] = []

for repo_entry in config["repositories"]:
    repo_name: str = repo_entry["name"]
    enabled: list[str] = repo_entry.get("enabled", [])
    pr_marked: list[str] = []
    pr_closed: list[str] = []
    if "mark-and-close-stale-prs" not in enabled:
        logger.info(f"Skipping {repo_name} - service not enabled")
        results.append([repo_name, "Skipped", "", ""])
        continue

    logger.info(f"Processing repository: {repo_name}")
    repo = g.get_repo(repo_name)
    pulls = repo.get_pulls(state="open", sort="updated")
    now: datetime = datetime.now(timezone.utc)
    for pr in pulls:
        updated = pr.updated_at
        if updated is None:
            # Skip PRs with no updated_at timestamp
            continue
        days_inactive: int = (now - updated).days
        comments = pr.get_issue_comments()
        stale_label: str = "stale"
        has_stale: bool = any(label.name == stale_label for label in pr.labels)

        if days_inactive >= DAYS_BEFORE_STALE and not has_stale:
            pr.add_to_labels(stale_label)
            pr.create_issue_comment(
                f"This PR is marked as stale after {DAYS_BEFORE_STALE} days of inactivity."
            )
            pr_marked.append(f"#{pr.number} {pr.title}")
            logger.info(f"Marked PR #{pr.number} as stale in {repo_name}")
        elif has_stale and days_inactive >= DAYS_BEFORE_STALE + DAYS_BEFORE_CLOSE:
            pr.create_issue_comment(
                f"Closed as stale after {DAYS_BEFORE_STALE + DAYS_BEFORE_CLOSE} days of inactivity."
            )
            pr.edit(state="closed")
            pr_closed.append(f"#{pr.number} {pr.title}")
            logger.info(f"Closed stale PR #{pr.number} in {repo_name}")

    results.append(
        [
            repo_name,
            "Checked",
            ", ".join(pr_marked) if pr_marked else "-",
            ", ".join(pr_closed) if pr_closed else "-",
        ]
    )
    logger.info(
        f"Completed processing {repo_name}: {len(pr_marked)} marked, {len(pr_closed)} closed"
    )

# Generate summary
logger.info("Generating summary report")
headers: list[str] = ["Repository", "Status", "PRs Marked Stale", "PRs Closed"]
table_md: str = tabulate(results, headers, tablefmt="github")

with open("summary.md", "w", encoding="utf-8") as f:
    f.write(f"## Mark and Close Stale PRs Report\n\n{table_md}\n")

logger.info("Summary report written to summary.md")
