# tasks.py
from celery_config import celery, ContextTask
from utils.github_helpers import get_commits_with_changes_files
from models import Team, User
from datetime import datetime
import json


celery.task = ContextTask

@celery.task
def add(x, y):
    return x + y

# ... existing code ...

@celery.task
def get_github_data(repo_url):
    # Fetch the team based on the provided team_id
  
    output = get_commits_with_changes_files(since="2024-11-08T22:00:00Z", until="2024-11-10T22:00:00Z", repo_owner=None, repo_name=None, repo_url=repo_url)
    with open(f"reports/{datetime.now().strftime('%Y-%m-%d_%H')}_output.json", "w") as file:
        file.write(json.dumps(output, indent=4))
        
        print(output)
   

