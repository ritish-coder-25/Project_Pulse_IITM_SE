import json
import pytest
from main import app
from models import db, User, Team, Project, Milestone, MilestoneStatus, Commit
from flask_jwt_extended import create_access_token

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


def test_stu_dashboard_success(client, auth_headers, create_users, create_team):
    """Test fetching student dashboard with valid data."""
    # Use a user who is part of the team
    user = create_users[0]  # Assuming the first user is valid
    user.team_id = create_team.team_id  # Assign the user to the team
    db.session.commit()

    response = client.get(
        f"/api/stu_home/{user.user_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.get_json()

    # Assertions for the structure of the response
    assert 'user_name' in data
    assert 'team_name' in data
    assert 'team_score' in data
    assert 'members' in data
    assert 'milestones' in data

    # Additional checks for correctness
    assert data['user_name'] == f"{user.first_name} {user.last_name}"
    assert data['team_name'] == create_team.team_name
    assert isinstance(data['team_score'], int)
    assert len(data['members']) > 0
    assert len(data['milestones']) >= 0


def test_stu_dashboard_no_team(client, auth_headers, create_users):
    """Test fetching student dashboard when the user is not part of a team."""
    # Use a user who is not part of any team
    user = create_users[0]
    user.team_id = None  # Ensure the user is not in a team
    db.session.commit()

    response = client.get(
        f"/api/stu_home/{user.user_id}",
        headers=auth_headers
    )

    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == "User is not in a team"
    assert data['errorCode'] == "team_get_curr_no_team"


def test_stu_dashboard_user_not_found(client, auth_headers):
    """Test fetching student dashboard for a non-existent user."""
    non_existent_user_id = 99999  # Use a user ID that doesn't exist

    response = client.get(
        f"/api/stu_home/{non_existent_user_id}",
        headers=auth_headers
    )

    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == "User not found"
    assert 'errorCode' in data


def test_stu_dashboard_invalid_token(client):
    """Test fetching student dashboard with an invalid or missing token."""
    user_id = 1  # Assuming a valid user ID

    response = client.get(
        f"/api/stu_home/{user_id}",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
    data = response.get_json()
    assert data['msg'] == "Token has expired" or data['msg'] == "Invalid token"


def test_stu_dashboard_partial_team_data(client, auth_headers, create_users, create_team):
    """Test fetching student dashboard with partial team data (e.g., no milestones)."""
    # Use a user who is part of the team
    user = create_users[0]
    user.team_id = create_team.team_id  # Assign the user to the team
    db.session.commit()

    # Ensure no milestones exist for the team
    db.session.query(Milestone).filter_by(team_id=create_team.team_id).delete()
    db.session.commit()

    response = client.get(
        f"/api/stu_home/{user.user_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.get_json()

    # Assertions for the structure of the response
    assert 'user_name' in data
    assert 'team_name' in data
    assert 'team_score' in data
    assert 'members' in data
    assert 'milestones' in data

    # Check that milestones are empty
    assert len(data['milestones']) == 0
