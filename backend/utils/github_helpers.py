# FILE: github_utils.py
import requests,os
from dotenv import load_dotenv
import json
from datetime import datetime
load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def github_user_exists(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    return response.status_code == 200


# Define the base URL and headers for API requests


def check_collaborator_status(repo_owner, repo_name, username):
    """
    Checks if the authenticated user is a collaborator on the given repository.
    """

    
    HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    BASE_URL = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    url = f"{BASE_URL}/collaborators/{username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 204:
        print("You are already a collaborator on this repository.")
        return True
    elif response.status_code == 404:
        print("You are not a collaborator on this repository.")
        return False
    else:
        print(f"Error checking collaborator status: {response.json()}")
        return None

def create_invite_request_issue(repo_owner, repo_name):
    """
    Creates an issue on the repository to request collaborator access.
    """

    
    HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    BASE_URL = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    url = f"{BASE_URL}/issues"
    issue_data = {
        "title": "Request for Collaborator Access",
        "body": f"Hello {repo_owner},\n\nI would like to request collaborator access to this repository. "
                "Please let me know if there's any additional information needed.\n\nThanks,\n PK"
    }
    response = requests.post(url, headers=HEADERS, json=issue_data)

    if response.status_code == 201:
        print("Invite request issue created successfully.")
        return response.json()
    else:
        print(f"Error creating issue: {response.json()}")
        return None



def get_commits_with_changes(since, until, repo_owner, repo_name):
    """
    Fetches commits within a specific date range and prints details of file changes.
    :param since: The start date (ISO 8601 format, e.g., "2023-01-01T00:00:00Z")
    :param until: The end date (ISO 8601 format, e.g., "2023-01-31T23:59:59Z")
    """

    HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    BASE_URL = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    # Step 1: Fetch all commits within the date range
    commits_url = f"{BASE_URL}/commits"
    params = {"since": since, "until": until}
    commits_response = requests.get(commits_url, headers=HEADERS, params=params)

    if commits_response.status_code == 200:
        commits = commits_response.json()
        print(f"\nCommits with File Changes from {since} to {until}:")

        # Step 2: For each commit, fetch the detailed changes
        for commit in commits:
            commit_sha = commit['sha']
            commit_detail_url = f"{BASE_URL}/commits/{commit_sha}"
            detail_response = requests.get(commit_detail_url, headers=HEADERS)

            if detail_response.status_code == 200:
                commit_data = detail_response.json()
                commit_message = commit_data['commit']['message']
                author = commit_data['commit']['author']['name']
                date = commit_data['commit']['author']['date']

                print(f"\nCommit by {author} on {date}: {commit_message}")
                print(f"Commit SHA: {commit_sha}")
                print("File Changes:")

                # Print file changes for each file modified in the commit
                for file in commit_data['files']:
                    filename = file['filename']
                    status = file['status']  # added, modified, or removed
                    additions = file['additions']
                    deletions = file['deletions']
                    changes = file['changes']

                    print(f"  - {filename} [{status}]")
                    print(f"    Additions: {additions}, Deletions: {deletions}, Total Changes: {changes}")
            else:
                print(f"Error fetching commit details for {commit_sha}: {detail_response.json()}")
    else:
        print(f"Error fetching commits: {commits_response.json()}")
        return None
    

import requests

def get_commits_with_changes_files(since, until, repo_owner, repo_name):
    """
    Fetches commits within a specific date range and stores details of file changes in a dictionary for each author.
    :param since: The start date (ISO 8601 format, e.g., "2023-01-01T00:00:00Z")
    :param until: The end date (ISO 8601 format, e.g., "2023-01-31T23:59:59Z")
    :param repo_owner: The GitHub username or organization name of the repository owner.
    :param repo_name: The name of the repository.
    :return: A dictionary with authors as keys, and their associated changes as values.
    """

    HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    BASE_URL = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    # Dictionary to store changes by user
    user_changes = {}

    # Step 1: Fetch all commits within the date range
    commits_url = f"{BASE_URL}/commits"
    params = {"since": since, "until": until}
    commits_response = requests.get(commits_url, headers=HEADERS, params=params)

    if commits_response.status_code == 200:
        commits = commits_response.json()

        # Step 2: For each commit, fetch the detailed changes
        for commit in commits:
            commit_sha = commit['sha']
            commit_detail_url = f"{BASE_URL}/commits/{commit_sha}"
            detail_response = requests.get(commit_detail_url, headers=HEADERS)

            if detail_response.status_code == 200:
                commit_data = detail_response.json()
                commit_message = commit_data['commit']['message']
                author = commit_data['commit']['author']['name']
                date = commit_data['commit']['author']['date']

                # Prepare the commit metadata
                commit_info = {
                    "commit_sha": commit_sha,
                    "message": commit_message,
                    "date": date,
                    "file_changes": []
                }

                # Step 3: Process each file in the commit and store the file changes
                for file in commit_data['files']:
                    filename = file['filename']
                    status = file['status']  # added, modified, or removed
                    additions = file['additions']
                    deletions = file['deletions']
                    changes = file['changes']
                    patch = file.get('patch', '')  # Get the actual code changes (diff) as a string

                    # Generate a string summarizing the file changes
                    changes_str = (
                        f"File: {filename}, Status: {status}, "
                        f"Additions: {additions}, Deletions: {deletions}, Total Changes: {changes}"
                    )

                    file_change_info = {
                        "filename": filename,
                        "status": status,
                        "additions": additions,
                        "deletions": deletions,
                        "total_changes": changes,
                        "changes_str": changes_str,  # Summary of the changes
                        "code_changes": patch  # Actual code changes (diff)
                    }

                    commit_info["file_changes"].append(file_change_info)

                # Step 4: Add or update the user's changes in the dictionary
                if author not in user_changes:
                    user_changes[author] = {
                        "total_commits": 0,
                        "commit_details": []
                    }

                # Increment the user's total commits and add the current commit details
                user_changes[author]["total_commits"] += 1
                user_changes[author]["commit_details"].append(commit_info)

            else:
                print(f"Error fetching commit details for {commit_sha}: {detail_response.json()}")

    else:
        print(f"Error fetching commits: {commits_response.json()}")
        return None

    return user_changes

# Run the check and create an issue if not already a collaborator
if __name__ == "__main__":
    #if not check_collaborator_status(repo_owner='ritish-coder-25', repo_name='Project_Pulse_IITM_SE', username='joycejemimas'):
        #create_invite_request_issue(repo_owner='joycejemimas', repo_name='california-agents')
       # print("You are not a collaborator on this repository.")
    #create_invite_request_issue(repo_owner='ritish-coder-25', repo_name='Project_Pulse_IITM_SE')

    # get_commits_with_changes(since="2023-01-01T00:00:00Z", until="2024-11-10T22:00:00Z",repo_owner= 'ritish-coder-25', repo_name='Project_Pulse_IITM_SE')
    output = get_commits_with_changes_files(since="2024-11-08T22:00:00Z", until="2024-11-10T22:00:00Z",repo_owner= 'ritish-coder-25', repo_name='Project_Pulse_IITM_SE')

    team_id = "Project_Pulse_IITM_SE"

    with open(f"reports/{team_id}_{datetime.now().strftime('%Y-%m-%d_%H')}_output.json", "w") as file:
        file.write(json.dumps(output, indent=4))
    print(output)

