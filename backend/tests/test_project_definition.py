import json
import pytest
from main import app, db, User, Project
from flask_jwt_extended import create_access_token
import warnings

# Ignore all warnings (including deprecation warnings)
warnings.filterwarnings("ignore")



@pytest.fixture
def create_users(db):
    """Create sample users for testing project creation."""
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


def test_create_project(client, create_users):
    """Test creating a new project."""
    user = create_users[0]
    user.user_type = "TA"
    db.session.commit()

    token = create_access_token(identity=user.user_id)

    newHeaders = {
        'Authorization': f'Bearer {token}'
    }

    print(f"User: {user.first_name} {user.last_name}, User Type: {user.user_type}")

    payload = {
        "name": "New Test Project",
        "statement": "This is the project statement for the new test project.",
        "document_url": "https://example.com/new-project-docs"
    }
    
    response = client.post(
        "/api/projects",
        data=json.dumps(payload),
        headers={**newHeaders, "Content-Type": "application/json"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Project created successfully'
    assert 'project' in data
    assert data['project']['name'] == "New Test Project"
    assert data['project']['statement'] == "This is the project statement for the new test project."


def test_create_project_missing_field(client, auth_headers):
    """Test creating a project with a missing required field."""
    payload = {
        "name": "Test Project Without Statement",
        # Missing "statement" field
        "document_url": "https://example.com/project-docs"
    }
    
    response = client.post(
        "/api/projects",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == "Validation error: {'statement': ['Missing data for required field.']}"


def test_create_project_invalid_url(client, auth_headers):
    """Test creating a project with an invalid URL."""
    payload = {
        "name": "Test Project Invalid URL",
        "statement": "This is a project with an invalid document URL.",
        "document_url": "invalid-url"  # Invalid URL format
    }

    response = client.post(
        "/api/projects",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == "Validation error: {'document_url': ['Not a valid URL.']}"


def test_create_project_unauthorized(client, create_users):
    """Test creating a project when the user is not authorized."""
    # Create a regular user with a non-admin role (e.g., "Student")
    user = create_users[0]
    user.user_type = "Student"  # Ensure user has no permission
    db.session.commit()
    
    access_token = create_access_token(identity=user.user_id)
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "name": "Unauthorized Project",
        "statement": "This project creation attempt should fail due to user permissions.",
        "document_url": "https://example.com/unauthorized-project"
    }

    response = client.post(
        "/api/projects",
        data=json.dumps(payload),
        headers={**newHeaders, "Content-Type": "application/json"}
    )

    assert response.status_code == 403
    data = response.get_json()
    assert data['message'] == "You do not have permission to create a project"


def test_create_project_with_invalid_role(client, create_users):
    """Test creating a project with a user who has invalid roles."""
    # Create a user with a role that is not allowed to create projects (e.g., "Student")
    user = create_users[0]
    user.user_type = "Student"  # Set to an invalid role for project creation
    db.session.commit()

    access_token = create_access_token(identity=user.user_id)
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "name": "Invalid Role Project",
        "statement": "This project creation attempt should fail due to user role.",
        "document_url": "https://example.com/invalid-role-project"
    }

    response = client.post(
        "/api/projects",
        data=json.dumps(payload),
        headers={**newHeaders, "Content-Type": "application/json"}
    )

    assert response.status_code == 403
    data = response.get_json()
    assert data['message'] == "You do not have permission to create a project"


def test_create_project_missing_name(client, auth_headers):
    """Test creating a project with missing name field."""
    payload = {
        "statement": "This project is missing a name.",
        "document_url": "https://example.com/missing-name-project"
    }

    response = client.post(
        "/api/projects",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == "Validation error: {'name': ['Missing data for required field.']}"


def test_create_project_with_empty_name(client, auth_headers):
    """Test creating a project with an empty name."""
    payload = {
        "name": "",  # Empty string for name
        "statement": "This project has an empty name.",
        "document_url": "https://example.com/empty-name-project"
    }

    response = client.post(
        "/api/projects",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == "Validation error: {'name': ['Shorter than minimum length 1.']}"

'''
def test_create_project_invalid_user(client, auth_headers):
    """Test creating a project with an invalid user in the JWT token."""
    # Use a malformed JWT token
    invalid_access_token = "invalid_token_string"  # Malformed token (not a valid JWT)
    
    # Creating headers with the invalid token
    newHeaders = {
        'Authorization': f'Bearer {invalid_access_token}'
    }

    payload = {
        "name": "Test Project with Invalid User",
        "statement": "This project should fail due to an invalid user.", 
        "document_url": "https://example.com/invalid-user-project"       
    }

    response = client.post(
        "/api/projects",
        data=json.dumps(payload),
        headers={**newHeaders, "Content-Type": "application/json"}       
    )

    # Assert that the response code is 401 Unauthorized due to the invalid token
    assert response.status_code == 401
    data = response.get_json()
    assert data['message'] == "Invalid token"

'''