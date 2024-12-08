# tasks.py
from celery_config import celery
from utils.github_helpers import get_commits_with_changes_files



@celery.task
def add(x, y):
    return x + y

# ... existing code ...

@celery.task
def get_github_data(team_id):
    # Fetch the team based on the provided team_id
    team = Team.query.get(team_id)
    if team:
        repo_url = team.github_repo_url
        output = get_commits_with_changes_files(since="2024-11-08T22:00:00Z", until="2024-11-10T22:00:00Z", repo_owner=None, repo_name=None, repo_url=repo_url)
        with open(f"reports/{team_id}_{datetime.now().strftime('%Y-%m-%d_%H')}_output.json", "w") as file:
            file.write(json.dumps(output, indent=4))
        
        print(output)
    else:
        # Handle the case where the team is not found
        print(f"Team with ID {team_id} not found.")

