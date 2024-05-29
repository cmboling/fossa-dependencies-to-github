import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
FOSSA_API_KEY = os.getenv('FOSSA_API_KEY')
FOSSA_LOCATOR = os.getenv('FOSSA_LOCATOR')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
GITHUB_SHA = os.getenv('GITHUB_SHA', 'your_commit_sha')
GITHUB_RUN_ID = os.getenv('GITHUB_RUN_ID', 'your_run_id')
GITHUB_WORKFLOW = os.getenv('GITHUB_WORKFLOW', 'your_workflow')
GITHUB_ACTION = os.getenv('GITHUB_ACTION', 'your_action')

# If FOSSA_API_KEY is None or empty, it indicates that the environment variable is not set correctly
if not FOSSA_API_KEY:
    raise ValueError("FOSSA_API_KEY is not set or is empty")

# FOSSA API call
fossa_url = f'https://app.fossa.com/api/v2/revisions/{FOSSA_LOCATOR}/dependencies?page=1&count=50'
fossa_headers = {
    'Authorization': f'Bearer {FOSSA_API_KEY}',
    'Accept': 'application/json'
}
fossa_response = requests.get(fossa_url, headers=fossa_headers)
fossa_data = fossa_response.json()

# Convert FOSSA response to GitHub Dependency Submission payload
github_payload = {
    'version': 0,
    'job': {
        'id': GITHUB_RUN_ID,
        'correlator': f'{GITHUB_WORKFLOW}_{GITHUB_ACTION}',
        'html_url': f'https://github.com/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID}'
    },
    'sha': GITHUB_SHA,
    'ref': 'refs/heads/main',
    'detector': {
        'name': 'fossa-detector',
        'version': '0.1.0',
        'url': 'https://github.com/fossa/fossa-cli'
    },
    'metadata': {},
    'scanned': datetime.utcnow().isoformat() + 'Z',
    'manifests': {
        'Podfile': {
            'name': 'Podfile',
            'file': {
                'source_location': 'Podfile'
            },
            'resolved': {}
        }
    }
}

for dependency in fossa_data['dependencies']:
    name_version = dependency['locator'].split('+')[1]
    name, version = name_version.split('$')

    resolved_entry = {
        'package_url': f'pkg:cocoapods/{name}@{version}',
        'metadata': {
            'name': name,
            'version': version
        }
    }

    github_payload['manifests']['Podfile']['resolved'][dependency['title']] = resolved_entry

# Save the payload to a file (optional, for debugging purposes)
with open('github_payload.json', 'w') as outfile:
    json.dump(github_payload, outfile, indent=2)

# Submit dependencies to GitHub
github_api_url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/dependency-graph/snapshots'
github_headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'X-GitHub-Api-Version': '2022-11-28'
}
response = requests.post(github_api_url, headers=github_headers, json=github_payload)

# Print response for debugging purposes
print(response.status_code)
print(response.json())
