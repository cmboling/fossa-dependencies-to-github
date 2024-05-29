# FOSSA to GitHub Dependency Submission Script

This repository contains a Python script that fetches cocoapods dependencies from the FOSSA API and submits them to the GitHub Dependency Submission API. This is useful for keeping your project's dependency graph up to date on GitHub.

## Purpose

The purpose of this script is to automate the process of retrieving dependency information from FOSSA and submitting it to GitHub. This helps in maintaining an accurate dependency graph in GitHub, which can be used for security and maintenance purposes.

## Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.6+**: This script is written in Python and requires Python 3.6 or newer.
2. **FOSSA API Key**: You need an API key from FOSSA to access their API.
3. **GitHub Token**: A GitHub personal access token with appropriate permissions to submit dependencies to your repository.
4. **Python Packages**: The script requires `requests` and `python-dotenv` packages. You can install these using pip.
5. **FOSSA CLI**: Ensure you have the CLI installed as well.

## Setup

### 1. Clone the Repository

Clone this repository to your local machine:

```sh
git clone https://github.com/cmboling/fossa-dependencies-to-github.git
cd fossa-dependencies-to-github
```

### 2. Create a .env File
Create a .env file in the root directory of the repository with the following content:

```
FOSSA_API_KEY=your_fossa_api_key
GITHUB_TOKEN=your_github_token
GITHUB_REPOSITORY=your_github_repository
GITHUB_SHA=your_commit_sha
GITHUB_RUN_ID=your_run_id
GITHUB_WORKFLOW=your_workflow
GITHUB_ACTION=your_action
```

Replace the placeholders with your actual values:

- FOSSA_API_KEY: Your FOSSA API key.
- GITHUB_TOKEN: Your GitHub personal access token.
- GITHUB_REPOSITORY: The GitHub repository in the format owner/repo.
- GITHUB_SHA: The commit SHA for which you are submitting dependencies.
- GITHUB_RUN_ID: The ID of the GitHub Actions run.
- GITHUB_WORKFLOW: The name of the GitHub workflow.
- GITHUB_ACTION: The name of the GitHub action.

### 3. Install Required Python Packages
Install the required Python packages using pip:

```
pip install requests python-dotenv
```

#### Usage

Run FOSSA analysis on the Podfile
```sh
fossa analyze --fossa-api-key <your access token>
fossa test --fossa-api-key <your access token>
```

Run the script using Python:

```sh
python3 submit_dependencies.py
```

This script will:
- Load environment variables from the .env file.
- Fetch dependencies from the FOSSA API.
- Construct the payload for the GitHub Dependency Submission API.
- Submit the dependency information to GitHub.

### Troubleshooting
If you encounter any issues, ensure the following:

- The environment variables in the .env file are correctly set.
- You have installed the required Python packages.
- You are using Python 3.6 or newer.
