
from utils.github_helpers import get_commits_with_changes_files
from models import Team, User, Commit, db
from datetime import datetime
import os
import json
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')


from celery_config import celery

@celery.task
def get_github_data(repo_url):
    try:
        with app.app_context():
        # Fetch GitHub data
            output = get_commits_with_changes_files(
                since="2024-11-08T22:00:00Z",
                until="2024-11-10T22:00:00Z",
                repo_owner=None,
                repo_name=None,
                repo_url=repo_url
            )
    
            # Save output to a JSON file
            timestamp = datetime.now().strftime('%Y-%m-%d_%H')
            output_file = f"reports/{timestamp}_output.json"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w") as file:
                file.write(json.dumps(output, indent=4))
    
            print(f"Output saved to {output_file}")
    
            # Parse and save commits to the database
            for user, details in output.items():
                for commit_detail in details["commit_details"]:
                    commit = Commit(
                        user_id=1,  # Replace with actual user_id logic
                        team_id=1,  # Replace with actual team_id logic
                        commit_hash=commit_detail["commit_sha"],
                        commit_message=commit_detail["message"],
                        commit_timestamp=datetime.fromisoformat(commit_detail["date"].replace("Z", "+00:00")),
                    )
                    db.session.add(commit)
    
            db.session.commit()
            print(f"Commits from {repo_url} saved to the database.")

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while processing GitHub data: {e}")