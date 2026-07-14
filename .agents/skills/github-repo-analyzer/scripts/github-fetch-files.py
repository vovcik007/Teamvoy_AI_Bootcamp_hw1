#!/usr/bin/env python3
"""
Fetches contents of specific files from a GitHub repository.
"""

import os
import sys
import argparse
import json
import base64
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


def get_file_content(owner: str, repo: str, file_path: str, branch: str = "main") -> dict:
    """Fetches content of a single file from GitHub."""
    if not GITHUB_TOKEN:
        return {"error": "GITHUB_TOKEN not found"}

    url = f"{API_BASE_URL}/{owner}/{repo}/contents/{file_path}?ref={branch}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # GitHub returns file content as base64 encoded
        if "content" in data:
            content = base64.b64decode(data["content"]).decode('utf-8', errors='ignore')
            return {
                "path": file_path,
                "content": content,
                "size": data.get("size", 0)
            }
        else:
            return {"error": f"Could not fetch {file_path}"}

    except requests.exceptions.RequestException as err:
        return {"error": f"Failed to fetch {file_path}: {str(err)}"}


def main():
    parser = argparse.ArgumentParser(description="Fetch file contents from GitHub")
    parser.add_argument("repo_path", help="Repository in format 'owner/repo'")
    parser.add_argument("files", nargs="+", help="List of file paths to fetch")
    parser.add_argument("--branch", default="main", help="Branch name")
    
    args = parser.parse_args()
    
    if "/" not in args.repo_path:
        print(json.dumps({"error": "Use format 'owner/repo'"}))
        sys.exit(1)
    
    owner, repo = args.repo_path.split("/", 1)
    
    files_data = []
    for file_path in args.files:
        result = get_file_content(owner, repo, file_path, args.branch)
        files_data.append(result)
    
    output = {
        "repository": f"{owner}/{repo}",
        "files": files_data
    }
    
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()