from celery_config import make_celery
from utils.github_helpers import get_commits_with_changes_files
from models import Team, User, Commit, db
from datetime import datetime
import os
import json
from flask import Flask
from utils.summarizer_chain import summarize_code_changes

import logging

# Configure logging to write to a file
logging.basicConfig(filename='celery_worker.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

def log_json(json_obj):
    logging.debug(json.dumps(json_obj, indent=4))

app = Flask(__name__)
app.config.from_object('config.Config')

celery = make_celery(app)




@celery.task(bind=True)
def get_github_data(self, repo_url, start_time, end_time):

    print("Received data", repo_url)
    print("Received data", start_time)
    print("Received data", end_time)
    try:
        print("Received data", repo_url)
        print("Received data", start_time)
        print("Received data", end_time)
        # Fetch GitHub data
        output = get_commits_with_changes_files(
            since=start_time,#"2024-11-08T22:00:00Z",
            until=end_time,#"2024-11-10T22:00:00Z",
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
            print(f"Processing commits for user {user}")
            userobj = User.query.filter_by(github_username=user).first()
            if userobj is not None:
                print(f"User {user} found in the database. Saving commits to the database.")
                print("Here is the user object", userobj.to_dict())
                user_id = userobj.to_dict()['user_id']
                team = userobj.to_dict()['team_id']
                print("Usrr id", user_id)
                print("Team ", team)
            else:
                print(f"User {user} not found in the database. Skipping commits.")
                continue

            print(f"User {userobj} found in the database. Saving commits to the database.")
            print("This is the commit details", details)
                
            for commit_detail in details["commit_details"]:
                commit_changes = ""
                for file in commit_detail["file_changes"]:
                    commit_changes += f"Additions: {file['filename']} ({file['additions']} additions, {file['deletions']} deletions)\n\n File changes: {file['changes_str']} \n File changes details: {file['code_changes']}\n\n" 


                print("Starting to run GPT on commit changes")
                analysis_json = summarize_code_changes(commit_changes)
                
                last_occurrence = analysis_json.rfind("```")
                if last_occurrence != -1:
                    analysis_json = analysis_json[:last_occurrence]
                print(analysis_json)
                analysis_json = analysis_json.replace("```", "").replace("json", "")
                
                analysis_data = json.loads(analysis_json)
                code_clarity_score = analysis_data.get("Code Clarity", {}).get("score", 0)
                functionality_score = analysis_data.get("Functionality", {}).get("score", 0)
                efficiency_score = analysis_data.get("Efficiency", {}).get("score", 0)
                maintainability_score = analysis_data.get("Maintainability", {}).get("score", 0)
                documentation_score = analysis_data.get("Documentation", {}).get("score", 0)
                overall_score = (
                    code_clarity_score +
                    functionality_score +
                    efficiency_score +
                    maintainability_score +
                    documentation_score
                    ) / 5.0
                improvement_suggestions = analysis_data.get("overall_summary", {}).get("suggested_improvements", "")
                additional_observations = analysis_data.get("overall_summary", {}).get("weaknesses", "")
   
                commit = Commit(
                    user_id=user_id,  # Replace with actual user_id logic
                    team_id=team,  # Replace with actual team_id logic
                    commit_hash=commit_detail["commit_sha"],
                    commit_message=commit_detail["message"],
                    commit_timestamp=datetime.fromisoformat(commit_detail["date"].replace("Z", "+00:00")),
                    commit_changes =commit_changes,
                    commit_score=overall_score,
                    commit_clarity=code_clarity_score,
                    complexity_score=efficiency_score,
                    code_quality_score=functionality_score,
                    risk_assessment="Medium" if overall_score < 4 else "Low",  # Example logic
                    improvement_suggestions=improvement_suggestions,
                    analysis_timestamp=datetime.utcnow(),
                    additional_observations=additional_observations,
                )
                
                db.session.add(commit)
                print("Commit details:", commit)
                    # print("Commit details:", log_json(commit.to_dict()))

                db.session.commit()
        print(f"Commits from {repo_url} saved to the database.")

        
        return {
            "status": "success",
            "output_file": output_file,
            "commit_count": len(output)
        }
    except Exception as e:
        # db.session.rollback()
        # self.update_state(state='FAILURE', meta={'error': str(e)})
        print(f"Error occurred while processing GitHub data: {e}")
        raise e




