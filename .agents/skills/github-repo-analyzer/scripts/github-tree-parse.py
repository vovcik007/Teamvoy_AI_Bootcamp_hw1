#!/usr/bin/env python3
"""
GitHub Repository Tree Parser

Fetches the complete file tree of a GitHub repository using the GitHub API.
Outputs clean JSON for AI agent consumption.
"""

import os
import sys
import argparse
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path.cwd() / ".env"
if not env_path.exists():
    # Fallback: look relative to the script's new location in .agents/skills/.../scripts/
    env_path = Path(__file__).parent.parent.parent.parent / ".env"

load_dotenv(dotenv_path=env_path, override=True)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
API_BASE_URL = "https://api.github.com/repos"


def get_repo_tree(owner: str, repo: str, branch: str = "main") -> dict:
    """
    Fetches the complete file tree of a GitHub repository.
    
    Returns a structured dict with repository info and file list.
    """
    if not GITHUB_TOKEN:
        return {"error": "GITHUB_TOKEN not found in environment"}

    url = f"{API_BASE_URL}/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Separate files from directories
        files = [item['path'] for item in data.get('tree', []) if item['type'] == 'blob']
        dirs = [item['path'] for item in data.get('tree', []) if item['type'] == 'tree']
        
        return {
            "repository": f"{owner}/{repo}",
            "branch": branch,
            "total_files": len(files),
            "total_directories": len(dirs),
            "file_tree": files,
            "directories": dirs
        }

    except requests.exceptions.HTTPError as err:
        if response.status_code == 401:
            return {"error": "Unauthorized. Check your GITHUB_TOKEN."}
        elif response.status_code == 404:
            return {"error": f"Repository '{owner}/{repo}' not found or inaccessible."}
        else:
            return {"error": f"HTTP Error: {str(err)}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Connection Error: {str(err)}"}


def main():
    parser = argparse.ArgumentParser(
        description="Fetch GitHub repository structure via API"
    )
    parser.add_argument(
        "repo_path",
        help="Repository in format 'owner/repo_name' (e.g., octocat/Hello-World)"
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch name (default: main)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Print formatted JSON output"
    )
    
    args = parser.parse_args()
    
    if "/" not in args.repo_path:
        print(json.dumps({"error": "Use format 'owner/repo_name'"}))
        sys.exit(1)
        
    owner, repo = args.repo_path.split("/", 1)
    
    result = get_repo_tree(owner, repo, args.branch)
    
    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))
    
    # Exit with error code if there was an error
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()