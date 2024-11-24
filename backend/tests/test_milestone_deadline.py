import pytest
from main import app, db, User, Team, Project, Milestone
from flask_jwt_extended import create_access_token
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch

@pytest.fixture
def create_users(db):
    """Create multiple sample users for testing."""
    users = []
    for i in range(1, 7):  # Creating 6 users
        existing_user = User.query.get(i)
        if existing_user:
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
def create_team(db):
    """Create a sample team for testing."""
    team = Team.query.get(1)
    if not team:
        team = Team(
            team_name="Team Sample",
            github_repo_url="https://github.com/sample-repo",
        )
        db.session.add(team)
        db.session.commit()
    return team

@pytest.fixture
def create_projects(db, create_team):
    """Create sample projects for testing."""
    project = Project.query.get(1)
    if not project:
        project = Project(
            project_topic="Project Topic 1",
            statement="Project Statement 1",
            document_url="http://example.com/doc_1.pdf"
        )
        db.session.add(project)
        db.session.commit()
    # Link team to project
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

@pytest.fixture(autouse=True)
def clear_database(db):
    """Ensure a clean slate before each test."""
    db.session.query(Milestone).delete()
    db.session.query(Project).delete()
    db.session.query(User).delete()
    db.session.commit()

def test_get_milestones_success(client, create_users, create_team, create_milestones):
    """Test that the endpoint returns the correct milestones data."""
    user = create_users[0]
    user.team_id = create_team.team_id
    db.session.commit()
    token = create_access_token(identity={"id": user.user_id, "role": "student"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get('/api/milestones/deadlines', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert len(data) == 6  # Since we created 6 milestones
    assert data[1]["milestone_name"] == "Milestone 2"
    assert data[1]["milestone_description"] == "Description for milestone 2"
    assert "end_date" in data[1]

def test_get_milestones_unauthenticated(client):
    """Test that the endpoint returns 401 if the user is unauthenticated."""
    response = client.get('/api/milestones/deadlines')
    assert response.status_code == 401
    assert "Missing Authorization Header" in response.get_json()["msg"]

def test_get_milestones_empty(client, create_users, create_team):
    """Test that the endpoint returns an empty list when no milestones are present."""
    user = create_users[0]
    user.team_id = create_team.team_id
    db.session.commit()
    token = create_access_token(identity={"id": user.user_id, "role": "student"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get('/api/milestones/deadlines', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert data == []

def test_get_milestones_server_error(client, mocker):
    """Test that the endpoint handles server errors gracefully."""
    # Mock the database query to raise an exception
    with mocker.patch('main.Milestone.query.all', side_effect=SQLAlchemyError("Database query failed")):
        token = create_access_token(identity={"id": 2, "role": "student"})
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get('/api/milestones/deadlines', headers=headers)
        data = response.get_json()
        print(data)
        assert response.status_code == 200
        assert data == [] 