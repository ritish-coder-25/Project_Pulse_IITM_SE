import json
import pytest
from main import app, db, User, Team, Project
from flask_jwt_extended import create_access_token
from db_test_helpers import get_user_token_header

pytest.team_apis_team_id = 1
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
    team_id = pytest.team_apis_team_id
    team = Team.query.get(team_id)
    return team

# @pytest.fixture
# def create_project(db):
#     """Create a sample project for testing."""
#     project = Project(
#         project_topic="Test Project",
#         statement="This is a test project.",
#         document_url="https://example.com/project-docs"
#     )
#     db.session.add(project)
#     db.session.commit()
#     return project

def test_create_team(client, auth_headers, create_users):
    """Test creating a new team."""
    payload = {
        "team": "Beta Team",
        "github_repo_url": "https://github.com/example/beta",
        "emails": [user.email for user in create_users]  # List of 5 user emails
    }
    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Team created and members added successfully'
    assert 'team_id' in data
    pytest.team_apis_team_id = data['team_id']

    # Verify the team was created in the database
    team = Team.query.get(data['team_id'])
    assert team is not None
    assert team.team_name == "Beta Team"
    assert team.github_repo_url == "https://github.com/example/beta"
    #assert team.team_lead_id == create_user.id
    
    # Verify all members are added to the team
    for user in create_users:
        updated_user = User.query.get(user.user_id)
        assert updated_user.team_id == team.team_id

def test_create_team_with_insufficient_users(client, auth_headers, create_users):
    """Test creating a team with fewer than 5 users should fail."""
    # Create only 4 users instead of 5

    users_list = [user.email for user in create_users]
    users = users_list[:3]

    payload = {
        "team": "Gamma Team",
        "github_repo_url": "https://github.com/example/gamma",
        "emails": [user for user in users]  # Only 4 emails
    }

    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400  # Assuming the API returns 400 for insufficient members
    data = response.get_json()
    #print("data", data)
    assert data['message'] == "Cannot create team with less than 5 members"
    assert 'errorCode' in data
    assert data['errorCode'] == "create_team_and_members_less_than_5"


def test_create_team_with_invalid_users(client, auth_headers, create_users):
    """Test creating a team with invalid users should fail."""
    users_list = [user.email for user in create_users]
    users = users_list[:5]

    payload = {
        "team": "Gamma Team",
        "github_repo_url": "https://github.com/example/gamma",
        "emails": [user for user in users]  # Only 4 emails
    }
    payload["emails"].append("nouserwillexistforthis@text.com")

    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400  # Assuming the API returns 400 for insufficient members
    data = response.get_json()
    print("data", data)
    assert data['message'] == "One or more users do not exist"
    assert 'errorCode' in data
    assert data['errorCode'] == "create_team_and_members_user_not_found"

def test_get_team(client, auth_headers, create_team, create_users):
    """Test retrieving a team with team_id"""
    team = create_team
    response = client.get(
        "/api/teams/" + str(team.team_id),
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.get_json()
    assert 'team' in data
    assert data['team']['team_name'] == "Beta Team"
    assert data['team']['github_repo_url'] == "https://github.com/example/beta"
    #print("data", data['team']['members'])
    assert len(data['team']['members']) >= 5  # Ensure all members are listed


def test_curr_users_team(client, auth_headers, create_team, create_users):
    """Test retrieving the current users team."""
    response = client.get(
        "/api/teams",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.get_json()
    assert 'team' in data
    assert data['team']['team_name'] == "Beta Team"
    assert data['team']['github_repo_url'] == "https://github.com/example/beta"
    #print("data", data['team']['members'])
    assert len(data['team']['members']) >= 5  # Ensure all members are listed


def test_get_team_no_team_exists(client, auth_headers):
    """Test retrieving a team which does not exist."""
    response = client.get(
        "/api/teams/" + str(199),
        headers=auth_headers
    )

    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == "Team not found"
    assert 'errorCode' in data
    assert data['errorCode'] == "team_get_team_not_found"

def test_get_team_no_team(client, auth_headers, db):
    """Test retrieving a team when the user is not part of any team."""
    # Create a user without a team
    user = User(
            first_name=f"No1del",
            last_name=f"Team1del",
            password="password123",
            email=f"no.team@example1del.com",
            github_username=f"memberuserdelete1del",
            discord_username=f"memberuserdelete1del",
            user_type="Student",
            approval_status="Active",
    )
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.user_id)  # Replace with appropriate user ID
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.get(
        "/api/teams",
        headers=newHeaders
    )

    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == "User is not in team"
    assert data['errorCode'] == "team_get_curr_no_team"


def test_put_team(client, create_team, auth_headers, db):
    """Test adding users to a team after it has been created."""
    # Create a user without a team
    user = User(
            first_name=f"putl",
            last_name=f"put1l",
            password="password123",
            email=f"put.team@example1del.com",
            github_username=f"putteammember",
            discord_username=f"putteammember",
            user_type="Student",
            approval_status="Active",
    )
    db.session.add(user)
    db.session.commit()
    team = create_team
    payload = {
        "team_id": team.team_id,
        "emails": [user.email]
    }

    response = client.put(
        "/api/teams/" + str(team.team_id),
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 200
    data = response.get_json()
    foundEmail = False
    for member in data['team']['members']:
        if member['email'] == user.email:
            foundEmail = True
            break
    assert foundEmail
    assert data['team']['team_name'] == team.team_name

def test_put_team_not_found(client, auth_headers, db, create_team):
    payload = {
        "team_id": create_team.team_id,
        "emails": ["testemail"]
    }

    response = client.put(
        "/api/teams/" + str(456),
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['errorCode'] == "put_team_and_members_team_not_found"


def test_put_team_user_not_found(client, auth_headers, db, create_team):
    payload = {
        "team_id": create_team.team_id,
        "emails": ["testemail@noemailwillbefound.com"]
    }

    response = client.put(
        "/api/teams/" + str(create_team.team_id),
        data=json.dumps(payload),
        headers={**auth_headers, "Content-Type": "application/json"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['errorCode'] == "create_team_and_members_user_not_found"

def test_put_team_user_not_team_lead(client, auth_headers, db, create_team):
    payload = {
        "team_id": create_team.team_id,
        "emails": ["testemail@noemailwillbefound.com"]
    }
    access_token = create_access_token(identity=3)  # Replace with appropriate user ID
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.put(
        "/api/teams/" + str(create_team.team_id),
        data=json.dumps(payload),
        headers={**newHeaders, "Content-Type": "application/json"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data['errorCode'] == "put_team_and_members_only_team_lead_can_edit"


def test_delete_team_member(client, auth_headers, create_team, create_users):
    """Test removing a member from a team."""
    # Create a user to be removed
    member = User(
            first_name=f"Member1",
            last_name=f"User1",
            password="password123",
            email=f"member.user1@example.com",
            github_username=f"memberuserdelete1",
            discord_username=f"memberuserdelete1",
            user_type="Student",
            approval_status="Active",
            team_id=create_team.team_id
    )

    member2 = User(
            first_name=f"Member2",
            last_name=f"User2",
            password="password123",
            email=f"member.user2@example.com",
            github_username=f"memberuserdelete2",
            discord_username=f"memberuserdelete2",
            user_type="Student",
            approval_status="Active",
            team_id=create_team.team_id
    )
    db.session.add(member)
    db.session.add(member2)
    db.session.commit()

    response = client.delete(
        f"/api/teams/{create_team.team_id}/users/{member.user_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'User removed from team successfully'

    # Verify the member's team_id is now None
    updated_member = User.query.get(member.user_id)
    assert updated_member.team_id is None

def test_delete_team_member_not_found(client, auth_headers, create_team, create_users):
    """Test removing a member from a team."""
    # Create a user to be removed

    member = User(
            first_name=f"Member1_del_not_found",
            last_name=f"User1_del_not_found",
            password="password123",
            email=f"member.user1_del_not_found@example.com",
            github_username=f"memberuserdelete1_del_not_found",
            discord_username=f"memberuserdelete1_del_not_found",
            user_type="Student",
            approval_status="Active",
    )
    db.session.add(member)
    db.session.commit()

    response = client.delete(
        f"/api/teams/{create_team.team_id}/users/{member.user_id}",
        headers=auth_headers
    )

    assert response.status_code == 400
    data = response.get_json()
    data = response.get_json()
    assert data['errorCode'] == "delete_members_from_team_user_not_in_team"

def test_delete_team_member_team_lead_no_remove(client, auth_headers, create_team, create_users):
    """Test removing a member from a team."""
    # Create a user to be removed
    response = client.delete(
        f"/api/teams/{create_team.team_id}/users/{1}",
        headers=auth_headers
    )

    assert response.status_code == 400
    data = response.get_json()
    data = response.get_json()
    assert data['errorCode'] == "delete_members_from_team_no_del_team_lead"

def test_delete_team_member_team_lead_can_only_remove(client, auth_headers, create_team, create_users):
    """Test removing a member from a team."""
    # Create a user to be removed
    member = User(
            first_name=f"Member1_lead_can_only_remove",
            last_name=f"User1_lead_can_only_remove",
            password="password123",
            email=f"member.user1_lead_can_only_remove@example.com",
            github_username=f"memberuserdelete1_lead_can_only_remove",
            discord_username=f"memberuserdelete1_lead_can_only_remove",
            user_type="Student",
            approval_status="Active",
            team_id=create_team.team_id
    )
    db.session.add(member)
    db.session.commit()
    access_token = create_access_token(identity=3)  # Replace with appropriate user ID
    newHeaders = {
        'Authorization': f'Bearer {access_token}'
    }

    response = client.delete(
        f"/api/teams/{create_team.team_id}/users/{member.user_id}",
        headers=newHeaders
    )

    assert response.status_code == 400
    data = response.get_json()
    data = response.get_json()
    assert data['errorCode'] == "delete_members_from_team_only_team_lead_can_del"