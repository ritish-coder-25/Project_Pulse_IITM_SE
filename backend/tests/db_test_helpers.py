
import pytest
from flask_jwt_extended import create_access_token
import sys
import os
from datetime import datetime, timedelta
import tempfile
import io
# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from main import app as flask_app
from main import db as _db
from models import Project, User, Milestone, Team


def db_create_milestones(_db, project):
    num_milestones = 5
    #yesterday = datetime.now().date() - timedelta(days=1)
    today = datetime.now().date()
    #tomorrow = datetime.now().date() + timedelta(days=1)
    for i in range(num_milestones):
        expected_start = today + timedelta(days=(i*2))
        expected_end = expected_start + timedelta(days=1)
        milestone = Milestone(
            milestone_name=f"Milestone {i}",
            project_id=project.project_id,
            milestone_description=f"This is milestone {i}",
            start_date=expected_start,
            end_date=expected_end,
            max_marks=10.0
        )
        _db.session.add(milestone)
    _db.session.commit()

def db_create_milestone(_db, project_id):
    today = datetime.now().date()
    expected_start = today + timedelta(days=(2))
    expected_end = expected_start + timedelta(days=1)
    milestone = Milestone(
        milestone_name=f"Milestone {today}",
        project_id=project_id,
        milestone_description=f"This is milestone {today}",
        start_date=expected_start,
        end_date=expected_end,
        max_marks=10.0
    )
    _db.session.add(milestone)
    _db.session.commit()
    return milestone


def db_create_user(db, user_p_fix='student', user_type="Student", team_id = None, approval_status="Active"):
    """Create multiple sample users for testing."""
    curr_d_time = datetime.now()
    password = "password123"
    user = User(
            first_name=f"User-{user_p_fix}-{curr_d_time}",
            last_name=f"Test{curr_d_time}",
            password=password,
            email=f"user{user_p_fix}{curr_d_time}@example.com",
            github_username=f"githubuser{user_p_fix}{curr_d_time}",
            discord_username=f"discorduser{user_p_fix}{curr_d_time}",
            user_type=user_type,
            approval_status=approval_status,
            team_id=team_id
        )
    db.session.add(user)
    db.session.commit()
    return user, password

def db_create_student_user(db, team_id = None, approval_status="Active"):
    """Create multiple sample users for testing."""
    user, password = db_create_user(db, team_id=team_id, approval_status=approval_status)
    return user, password


def db_create_ta_user(db, approval_status="Active"):
    """Create multiple sample users for testing."""
    user, password = db_create_user(db, user_p_fix='ta', user_type="TA", approval_status=approval_status)
    return user, password

def get_user_token_header(user_id): 
    access_token = create_access_token(identity=user_id)  # Replace with appropriate user ID
    return {
        'Authorization': f'Bearer {access_token}'
    }



def db_create_users_for_team(db, team_id = None,no_of_users=7):
    """Create multiple sample users for a team."""
    users = []
    for i in range(1, no_of_users):
        user, password = db_create_student_user(db, team_id)
        users.append({
            'user': user,
            'password': password
        })
    return users


def db_create_team_with_users(db, project_id=1):
    """Create team with multiple users."""
    team = Team(
        team_name="Beta Team",
        github_repo_url="https://github.com/example/beta",
        project_id=project_id)

    db.session.add(team)
    db.session.commit()
    team_users = db_create_users_for_team(db, team_id=team.team_id)
    team_lead = team_users[0]['user']
    team.team_lead_id = team_lead.user_id
    db.session.add(team)
    db.session.commit()
    return team, team_users, team_lead