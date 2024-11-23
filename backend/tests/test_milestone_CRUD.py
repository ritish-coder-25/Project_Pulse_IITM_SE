import json
import pytest
from main import app, db, User, Milestone, Project
from flask_jwt_extended import create_access_token
import warnings
from datetime import datetime

# Ignore all warnings (including deprecation warnings)
warnings.filterwarnings("ignore")


@pytest.fixture
def create_users(db):
    """Create sample users for testing milestone creation."""
    users = []
    for i in range(1, 6):  # Creating 5 users
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
            user_type="TA",  # Admin, TA, Instructor, Developer, etc.
            approval_status="Active"
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users


@pytest.fixture
def create_project(db):
    """Create a sample project for testing."""
    project = Project(
        project_topic="Test Project",
        statement="This is a test project.",
        document_url="https://example.com/project-docs"
    )
    db.session.add(project)
    db.session.commit()
    return project


@pytest.fixture
def create_milestone(db, create_project):
    """Create a sample milestone for testing."""
    project = create_project
    milestone = Milestone(
        milestone_name="Test Milestone",
        milestone_description="This is a test milestone.",
        start_date=datetime.strptime("2024-11-01", "%Y-%m-%d"),
        end_date=datetime.strptime("2024-11-30", "%Y-%m-%d"),
        max_marks=100.0,
        project_id=project.project_id
    )
    db.session.add(milestone)
    db.session.commit()
    return milestone


@pytest.fixture
def auth_headers(create_users):
    """Generate authorization headers for a test user."""
    user = create_users[0]  # Choose the first user
    access_token = create_access_token(identity=user.user_id)
    return {
        'Authorization': f'Bearer {access_token}'
    }


def test_create_milestone(client, auth_headers, create_milestone):
    """Test creating a new milestone."""
    payload = {
        "milestone_name": "New Test Milestone",
        "milestone_description": "This is the description for the new test milestone.",
        "start_date": "2024-12-01",
        "end_date": "2024-12-31",
        "max_marks": 120.0,
        "project_id": create_milestone.project_id
    }
    
    response = client.post(
        "/api/milestones",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Milestone created successfully'
    assert data['milestone_id'] == 2


def test_create_milestone_missing_field(client, auth_headers):
    """Test creating a milestone with a missing required field."""
    payload = {
        "milestone_name": "Test Milestone Without Description",
        "start_date": "2024-11-01",
        "end_date": "2024-11-30",
        "max_marks": 100.0,
        "project_id": 1
    }
    
    response = client.post(
        "/api/milestones",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == "Validation error: {'milestone_description': ['Missing data for required field.']}"


def test_create_milestone_invalid_date(client, auth_headers):
    """Test creating a milestone with invalid start or end date."""
    payload = {
        "milestone_name": "Test Milestone with Invalid Date",
        "milestone_description": "This milestone has invalid dates.",
        "start_date": "invalid-date",  # Invalid date format
        "end_date": "2024-12-31",
        "max_marks": 100.0,
        "project_id": 1
    }

    response = client.post(
        "/api/milestones",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == "Validation error: {'start_date': ['Start date must be in the format YYYY-MM-DD']}"


def test_create_milestone_wrong_role(client, create_users):
    """Test creating a milestone when the user is not authorized."""
    # Create a regular user with a non-admin role (e.g., "Student")
    user = create_users[0]
    user.user_type = "Student"  # Ensure user has no permission
    db.session.commit()
    
    access_token = create_access_token(identity=user.user_id)
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "milestone_name": "Wrong Role Milestone",
        "milestone_description": "This milestone creation attempt should fail due to user permissions.",
        "start_date": "2024-12-01",
        "end_date": "2024-12-31",
        "max_marks": 100.0,
        "project_id": 1
    }

    response = client.post(
        "/api/milestones",
        data=json.dumps(payload),
        headers={**newHeaders, "Content-Type": "application/json"}
    )

    assert response.status_code == 403
    data = response.get_json()
    assert data['message'] == "You do not have permission to create a milestone"

def test_create_milestones_unauthorized(client):
    """Test unauthorized access to creating milestones"""
    payload = {
        "milestone_name": "Unauthorized Milestone",
        "milestone_description": "This milestone creation attempt should fail due to user permissions.",
        "start_date": "2024-12-01",
        "end_date": "2024-12-31",
        "max_marks": 100.0,
        "project_id": 1
    }

    response = client.post(
        "/api/milestones",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 401 #Unauthorized status
    data = response.get_json()
    assert data['msg'] == "Missing Authorization Header"


def test_get_milestones(client, auth_headers, create_milestone):
    """Test retrieving all milestones."""
    response = client.get(
        "/api/milestones",
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data['milestones'], list)  # Check that the response is a list of milestones
    assert len(data['milestones']) > 0  # Check that there is at least one milestone

def test_get_milestones_unauthorized(client):
    """Test unauthorized access to get milestones."""
    response = client.get(
        "/api/milestones",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 401  # Unauthorized status
    data = response.get_json()
    assert data['msg'] == "Missing Authorization Header"


def test_update_milestone(client, auth_headers, create_milestone, create_users):
    """Test updating a milestone."""
    user = create_users[0]
    user.user_type = "TA"  # Ensure user has no permission
    db.session.commit()
    
    access_token = create_access_token(identity=user.user_id)
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }
    payload = {
        "milestone_name": "Updated Milestone Name",
        "milestone_description": "Updated milestone description.",
        "start_date": "2025-01-01",
        "end_date": "2025-02-24",
        "max_marks": 60.0,
    }

    response = client.put(
        f"/api/milestones/{create_milestone.milestone_id}",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Milestone updated successfully'

def test_update_milestone_unauthorized(client, create_milestone):
    """Test unauthorized user trying to update a milestone."""
    payload = {
        "milestone_name": "Unauthorized Updated Milestone Name",
        "milestone_description": "Unauthorized Updated milestone description.",
        "start_date": "2025-01-01",
        "end_date": "2025-02-24",
        "max_marks": 60.0,
    }
    response = client.put(
        f"/api/milestones/{create_milestone.milestone_id}",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 401  # Unauthorized status
    data = response.get_json()
    assert data['msg'] == "Missing Authorization Header"

def test_update_milestone_wrong_role(client, create_users, create_milestone):
    """Test creating a milestone when the user is not authorized."""
    # Create a regular user with a non-admin role (e.g., "Student")
    user = create_users[0]
    user.user_type = "Student"  # Ensure user has no permission
    db.session.commit()
    
    access_token = create_access_token(identity=user.user_id)
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "milestone_name": "Wrong Role Updating Milestone",
        "milestone_description": "This milestone update attempt should fail due to user permissions.",
        "start_date": "2024-12-01",
        "end_date": "2024-12-31",
        "max_marks": 100.0,
    }

    response = client.put(
        f"/api/milestones/{create_milestone.milestone_id}",
        data=json.dumps(payload),
        headers={**newHeaders, "Content-Type": "application/json"}
    )

    assert response.status_code == 403
    data = response.get_json()
    assert data['message'] == "You do not have permission to update milestone"


def test_delete_milestone(client, create_milestone, create_users):
    """Test deleting a milestone."""
    user = create_users[0]
    user.user_type = "TA"
    db.session.commit()

    access_token = create_access_token(identity=user.user_id)
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }

    response = client.delete(
        f"/api/milestones/{create_milestone.milestone_id}",
        headers={**newHeaders, "Content-Type": "application/json"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Milestone deleted successfully'

def test_delete_milestone_unauthorized(client, create_milestone):
    """Test unauthorized user trying to delete a milestone."""
    response = client.delete(
        f"/api/milestones/{create_milestone.milestone_id}",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 401  # Unauthorized status
    data = response.get_json()
    assert data['msg'] == "Missing Authorization Header"

def test_delete_milestone_wrong_role(client, create_users, create_milestone):
    """Test wrong role trying to delete a milestone"""
    user = create_users[0]
    user.user_type = "Student"
    db.session.commit()

    access_token = create_access_token(identity=user.user_id)
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }

    response = client.delete(
        f"/api/milestones/{create_milestone.milestone_id}",
        headers={**newHeaders, "Content-Type": "application/json"}
    )

    assert response.status_code == 403
    data = response.get_json()
    assert data['message'] == "You do not have permission to delete milestones"


