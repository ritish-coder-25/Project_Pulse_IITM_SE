import json
import pytest
from flask_jwt_extended import create_access_token
from main import app, db
from datetime import datetime
from models import User, Team, Milestone, MilestoneStatus, Commit, Project


@pytest.fixture
def ta_auth_headers(app, db):
    """Generate authentication headers for TA."""
    try:
        ta_user = User(
            first_name="TA",
            last_name="User",
            email="ta.user@example.com",
            password='ta',
            user_type="TA",
            approval_status="Active"
        )
        db.session.add(ta_user)
        db.session.commit()
    
    except:
        db.session.rollback()
        ta_user = User.query.filter_by(email='ta.user@example.com').first()

    if ta_user:
        access_token = create_access_token(identity=ta_user.user_id)
        return {
            'Authorization': f'Bearer {access_token}'
        }
    else:
        print("Error while accessing TA User")


@pytest.fixture
def inactive_ta_auth_headers(app, db):
    """Generate authentication headers for TA."""
    try:
        ta_user = User(
            first_name="TA",
            last_name="User",
            email="inactive.ta.user@example.com",
            password='ta',
            user_type="TA",
            approval_status="Inactive"
        )
        db.session.add(ta_user)
        db.session.commit()
    
    except:
        db.session.rollback()
        ta_user = User.query.filter_by(email='inactive.ta.user@example.com').first()

    if ta_user:
        access_token = create_access_token(identity=ta_user.user_id)
        return {
            'Authorization': f'Bearer {access_token}'
        }
    else:
        print("Error while accessing TA User")


@pytest.fixture
def student_auth_headers(app, db):
    """Generate authentication headers for Student."""

    try:
        student_user = User(
            first_name="Student",
            last_name="User",
            email="student.user@example.com",
            password='student',
            user_type="Student",
            approval_status="Active"
        )
        db.session.add(student_user)
        db.session.commit()
    except:
        db.session.rollback()
        student_user = User.query.filter_by(email='student.user@example.com').first()

    if student_user:
        access_token = create_access_token(identity=student_user.user_id)
        return {
            'Authorization': f'Bearer {access_token}'
        }
    else:
        print("Error while accessing Student user")


@pytest.fixture
def create_users(db):
    """Create multiple sample users for testing."""
    users = []
    for i in range(1, 7):  # Creating 5 users
        existing_user = User.query.get(i)
        if(existing_user):
            users.append(existing_user)
            continue
        user = User(
            first_name=f"User{i}",
            last_name=f"Test{i}",
            password="password123",
            email=f"user{i}@example.com",
            github_username=f"githubuser{i}",
            discord_username=f"discorduser{i}",
            user_type="Student",
            approval_status="Active"
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users

@pytest.fixture
def create_team(db, create_users):
    """Create a sample team for testing."""
    team = Team.query.get(1)
    if not team:
        team = Team(
            team_name="Sample Team",
            github_repo_url="https://github.com/sample-repo",
        )
        db.session.add(team)
        db.session.commit()
    for user in create_users:
        if user.team_id is None:  
            user.team_id = team.team_id

    if not team.team_lead_id:
        team.team_lead_id = create_users[0].user_id  
    db.session.commit()
    return team

@pytest.fixture
def create_projects(db, create_team):
    """Create sample projects for testing."""
    project = Project.query.get(1)
    if (not project):
        project = Project(
            project_topic=f"Project Topic_1",
            statement=f"Project Statement_1",
            document_url=f"http://example.com/doc_1.pdf"
            )
        db.session.add(project)
        db.session.commit() 
    team = create_team
    if team:
        team.project_id = project.project_id
        db.session.commit()
    return project


@pytest.fixture
def create_milestones(db, create_projects):
    """Create sample milestones for testing."""
    milestones = []
    project = create_projects
    for i in range(1, 7):
        milestone = Milestone.query.get(i)
        if milestone:
            milestones.append(milestone)
            continue
        milestone = Milestone(
            milestone_name=f"Milestone {i}",
            milestone_description=f"Description for milestone {i}",
            start_date=datetime(2024, 1, i),
            end_date=datetime(2024, 1, i + 10),
            max_marks=20.0,
            project_id=project.project_id
        )
        db.session.add(milestone)
        milestones.append(milestone)
    db.session.commit()
    return milestones


@pytest.fixture
def create_milestone_statuses(db, create_team, create_milestones):
    """Create sample milestone statuses for testing."""
    statuses = []
    team = create_team
    for milestone in create_milestones:
        status = MilestoneStatus.query.filter_by(
            team_id=team.team_id, milestone_id=milestone.milestone_id
        ).first()
        if status:
            statuses.append(status)
            continue
        status = MilestoneStatus(
            team_id=team.team_id,
            milestone_id=milestone.milestone_id,
            milestone_status="Pending",
            eval_date=None,
            completed_date=None,
            eval_score=0.0,
            eval_feedback=None
        )
        db.session.add(status)
        statuses.append(status)
    db.session.commit()
    return statuses


@pytest.fixture
def create_commits(db, create_team, create_users):
    """Create sample commits for testing."""
    commits = []
    team = create_team
    for i, user in enumerate(create_users[:7], start=1):
        commit = Commit.query.filter_by(user_id=user.user_id, team_id=team.team_id).first()
        if commit:
            commits.append(commit)
            continue
        commit = Commit(
            user_id=user.user_id,
            team_id=team.team_id,
            commit_hash=f"hash_{i}",
            commit_message=f"Commit message {i}",
            commit_score=95.0 - i,
            commit_url=f"http://example.com/commit/{i}",
            complexity_score=10.0 - i,
            code_quality_score=90.0 - i,
            risk_assessment="Low",
            improvement_suggestions=f"Suggestions for commit {i}",
            additional_observations=f"Observations for commit {i}"
        )
        db.session.add(commit)
        commits.append(commit)
    db.session.commit()
    return commits
    

# Define test cases for teams

def test_ta_teams_dashboard_ta_role(client, ta_auth_headers, create_commits):

    response = client.get(f"/api/ta-teams", headers=ta_auth_headers)

    assert response.status_code == 200

    data = response.get_json()

    assert "milestones" in data

    assert "teams" in data


def test_ta_teams_dashboard_unauthorized_role(client, student_auth_headers):

    response = client.get(f"/api/ta-teams", headers=student_auth_headers)

    assert response.status_code == 403


def test_ta_teams_dashboard_inactive_role(client, inactive_ta_auth_headers):

    response = client.get(f"/api/ta-teams", headers=inactive_ta_auth_headers)

    assert response.status_code == 403


def test_ta_teams_dashboard_unauthorized_access(client):

    response = client.get(f"/api/ta-teams")

    assert response.status_code == 401



# Define test cases for individual team

def test_ta_team_dashboard_ta_role(client, ta_auth_headers, create_commits):

    team = Team.query.first()

    response = client.get(f"/api/ta-teams/{team.team_id}", headers=ta_auth_headers)

    assert response.status_code == 200

    data = response.get_json()

    assert "team" in data

    assert "milestones" in data

    assert "members" in data


def test_ta_team_dashboard_unauthorized_role(client, student_auth_headers, create_commits):

    team = Team.query.first()

    response = client.get(f"/api/ta-teams/{team.team_id}", headers=student_auth_headers)

    assert response.status_code == 403


def test_ta_team_dashboard_inactive_role(client, inactive_ta_auth_headers, create_commits):

    team = Team.query.first()

    response = client.get(f"/api/ta-teams/{team.team_id}", headers=inactive_ta_auth_headers)

    assert response.status_code == 403


def test_ta_team_dashboard_invalid_team(client, ta_auth_headers, create_commits):

    response = client.get(f"/api/ta-teams/9999999", headers=ta_auth_headers)

    assert response.status_code == 404


def test_ta_team_dashboard_unauthorized_access(client, create_commits):

    team = Team.query.first()

    response = client.get(f"/api/ta-teams/{team.team_id}")

    assert response.status_code == 401


