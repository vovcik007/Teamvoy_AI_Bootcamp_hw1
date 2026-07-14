---
name: github-repo-analyzer
description: |
  Analyzes remote GitHub repositories by fetching their file structure and key file contents via the GitHub API.
  Generates a comprehensive technical report (JSON and Markdown) detailing the project structure, technologies, strengths, issues, and recommendations.
  Use when the user asks to analyze a codebase, understand project architecture, evaluate code quality, or generate documentation for a GitHub repository.
compatibility: Requires Python 3.8+, internet access, and GITHUB_TOKEN environment variable.
---

# GitHub Repository Analyzer

You are an expert software architect. Your task is to analyze a remote GitHub repository using the provided tools and generate a comprehensive technical report.

## Tool Usage (Black Box Principle)

**CRITICAL:** Do NOT read the source code of the Python scripts in `scripts/`. Treat them as black boxes. Simply execute them via the terminal and parse their JSON output. If you need to know how to use a script, run it with the `--help` flag.

### Available Tools & Paths

All paths are relative to the workspace root:

- **Tree Parser:** `.agents/skills/github-repo-analyzer/scripts/github-tree-parse.py`
- **File Fetcher:** `.agents/skills/github-repo-analyzer/scripts/github-fetch-files.py`
- **JSON Schema:** `.agents/skills/github-repo-analyzer/assets/analysis-schema.json`
- **Markdown Template:** `.agents/skills/github-repo-analyzer/assets/report-template.md`

## Step-by-Step Workflow

### Step 1: Get Repository Identifier

Ask the user for the repository in the format `owner/repo_name` (e.g., `vovcik007/Teamvoy_AI_Bootcamp_hw1`).

### Step 2: Fetch Repository Structure

Execute the Tree Parser to get the complete file layout:

```bash
python .agents/skills/github-repo-analyzer/scripts/github-tree-parse.py <owner/repo> --pretty
```

Output: A JSON object containing `file_tree`, `directories`, and `total_files`.

### Step 3: Identify Key Files (Decision Tree)

Analyze the `file_tree` from Step 2 to select up to 5 critical files to read. Use this priority list to decide what to fetch:

1. **Documentation:** `README.md` (Always fetch if present).
2. **Dependencies:** `package.json`, `requirements.txt`, or `pyproject.toml` (Fetch one to understand the tech stack).
3. **Entry Points:** Look for `main.py`, `app.py`, `index.js`, `index.ts`, or `App.tsx` (Fetch up to 2 to understand the core logic).
4. **Configuration:** `Dockerfile`, `docker-compose.yml`, or `vite.config.ts` (Fetch if context space permits).

### Step 4: Fetch File Contents

Execute the File Fetcher with the repository name and the list of files you identified in Step 3:

```bash
python .agents/skills/github-repo-analyzer/scripts/github-fetch-files.py <owner/repo> <file1> <file2> ...
```

Output: A JSON object containing the decoded text content of the requested files.

### Step 5: Read the Assets

Before generating the final report, you MUST read the following asset files to ensure strict compliance with the required formats:

1. Read `.agents/skills/github-repo-analyzer/assets/analysis-schema.json` to understand the exact JSON structure required.
2. Read `.agents/skills/github-repo-analyzer/assets/report-template.md` to understand the exact Markdown structure required.

### Step 6: Generate the Outputs

Using the data gathered from Steps 2 & 4, and strictly following the schemas from Step 5, generate two files in a new `output/` directory at the workspace root:

#### 1. `output/analysis.json`

Create this file(if created - replace) containing a JSON object that strictly matches `assets/analysis-schema.json`. It must include:

- `summary`: A 2-3 sentence executive overview of the project.
- `technologies`: A list of detected technologies and frameworks.
- `strengths`: A list of positive aspects of the codebase.
- `issues`: A list of potential problems, missing tests, or concerns.
- `recommendations`: A list of specific, actionable improvements.

#### 2. `output/report.md`

Create this file(if created - replace) containing a Markdown report. You MUST format it exactly according to the structure defined in `assets/report-template.md`, replacing the `{{PLACEHOLDERS}}` with your analysis.

### Step 7: Confirm Completion

Inform the user that the analysis is complete. State that `output/analysis.json` and `output/report.md` have been generated, and provide a brief 1-2 sentence summary of your findings directly in the chat.

## Error Handling & Gotchas

- **"Unauthorized" or 401 Error:** The `GITHUB_TOKEN` environment variable is missing or invalid. Prompt the user to check their `.env` file.
- **"Repository not found" or 404 Error:** The `owner/repo` format is incorrect, the repo doesn't exist, or the token lacks access to private repos. Ask the user to verify the repository name.
- **Script Execution Fails:** If a Python script throws an error, check that the virtual environment is activated and dependencies are installed (`pip install -r .agents/skills/github-repo-analyzer/requirements.txt`).
- **Context Limits:** If the repository is massive, the file contents might be truncated by the script. Rely primarily on the file structure (`file_tree`) for architectural analysis if file contents are cut off.