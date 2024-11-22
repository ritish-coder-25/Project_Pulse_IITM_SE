import json
import pytest
from main import app, db, User, Milestone, MilestoneStatus, Project, Team, Member, Submission, File, Commit
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

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
def create_milestone(db):
    """Create n milestones for testing."""
    def _create_milestone(n):
        milestones = []
        for i in range(1, n + 1):
            milestone = Milestone.query.get(i)
            if not milestone:
                milestone = Milestone(milestone_name=i, milestone_description=f"Sample Milestone {i}", start_date=datetime(2024, 10, 15), end_date=datetime(2024,12,31), max_marks=100, project_id=1)
                db.session.add(milestone)
                milestones.append(milestone)
        db.session.commit()
        return milestones
    return _create_milestone

@pytest.fixture
def create_team(db, create_users):
    """Create n teams for testing."""
    def _create_team(n):
        teams = []
        for i in range(1, n + 1):
            team = Team.query.get(i)
            if not team:
                team = Team(team_id=i, team_name=f"Sample Team {i}")
                db.session.add(team)
                teams.append(team)
        db.session.commit()
        return teams
    return _create_team


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
def reset_db(db):
    """Reset the database for next test so Team names etc are setup fresh"""
    try:
        # Clear data from tables in the correct dependency order
        db.session.query(MilestoneStatus).delete()
        db.session.query(Commit).delete()
        db.session.query(Team).delete()
        db.session.query(Milestone).delete()
        db.session.query(Submission).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in case of any errors
        raise RuntimeError(f"Error resetting the database: {str(e)}")
    finally:
        db.session.close()  # Ensure session is always closed
    return

@pytest.fixture
def auth_headersStu(app):
    """Generate authentication headers for Student using JWT."""
    db.session.query(User).delete()
    db.session.commit()
    user_logging_in = User(
        first_name=f"StuFname1",
        last_name=f"StuLname1",
        password="password123",
        email=f"userStu@example.com",
        github_username=f"githubuserStu",
        discord_username=f"discorduserStu",
        user_type="Student",
        approval_status="Active"
    )
    db.session.add(user_logging_in)
    db.session.commit()
    with app.app_context():
        access_token = create_access_token(identity=1)
        return {
            'Authorization': f'Bearer {access_token}'
        }

@pytest.fixture
def auth_headersTA(app):
    """Generate authentication headers for TA using JWT."""
    db.session.query(User).delete()
    db.session.commit()
    user_logging_in = User(
        first_name=f"TAFname1",
        last_name=f"TALname1",
        password="password123",
        email=f"userTA@example.com",
        github_username=f"githubuserTA",
        discord_username=f"discorduserTA",
        user_type="TA",
        approval_status="Active"
    )
    db.session.add(user_logging_in)
    db.session.commit()
    with app.app_context():
        access_token = create_access_token(identity=1)
        return {
            'Authorization': f'Bearer {access_token}'
        }

# @pytest.fixture
# def create_commits(db):
#     """Create a sample project for testing."""
#     dt = datetime(2024, 11, 19)
#     commit = Commit(
#         user_id=1,
#         team_id=2,
#         commit_hash="testcommithash",
#         commit_timestamp=dt
#     )
#     db.session.add(commit)
#     db.session.commit()
#     print(commit)
#     return commit

## TESTS FOR TAHOMEPAGE API: /api/commits

def test_get_commit_not_loggedin(client, reset_db):
    """Test retrieving a commit without login."""
    dt = datetime(2024, 11, 19)
    reset_db
    commitdata = Commit(
        user_id=1,
        team_id=2,
        commit_hash="testcommithash",
        commit_timestamp=dt
    )
    db.session.add(commitdata)
    db.session.commit()
    response = client.get(
        "/api/commits",
    )
    assert response.status_code == 401


def test_get_commit_1commit(client, auth_headersTA, create_team, reset_db):
    """Test retrieving team with 1 commit in database."""
    dt = datetime.now() - timedelta(days=1)
    reset_db
    create_team(2)
    commitdata = Commit(
        user_id=1,
        team_id=2,
        commit_hash="testcommithash",
        commit_timestamp=dt
    )
    db.session.add(commitdata)
    db.session.commit()
    print(db.session.query(Commit.commit_timestamp).all())
    response = client.get(
        "/api/commits",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert data[0]['team'] == "Sample Team 2"
    assert len(data) == 1  

def test_get_commit_5commits_with2from1team(client, auth_headersTA, create_team, reset_db):
    """Test retrieving team with 5 commits in all, and 2 commits from 1 team."""
    reset_db
    create_team(2)
    dt1 = datetime.now() - timedelta(days=1)
    dt2 = datetime.now() - timedelta(days=2)
    dt3 = datetime.now() - timedelta(days=3)
    commits = [
        Commit(user_id=1, team_id=1, commit_hash="hash_team1_1", commit_timestamp=dt1),
        Commit(user_id=2, team_id=1, commit_hash="hash_team1_2", commit_timestamp=dt2),
        Commit(user_id=3, team_id=2, commit_hash="hash_team2_1", commit_timestamp=dt1),
        Commit(user_id=4, team_id=2, commit_hash="hash_team2_2", commit_timestamp=dt2),
        Commit(user_id=5, team_id=2, commit_hash="hash_team2_3", commit_timestamp=dt3)
    ]
    db.session.add_all(commits)
    db.session.commit()
    response = client.get(
        "/api/commits",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert len(data) == 5  
    team1_commits = [commit for commit in data if commit['team'] == "Sample Team 1"]
    team2_commits = [commit for commit in data if commit['team'] == "Sample Team 2"]
    assert len(team1_commits) == 2  
    assert len(team2_commits) == 3  



def test_get_commit_noCommits(client, auth_headersTA, reset_db):
    """Test retrieving a commit when there are no commits in last 7 days."""
    reset_db
    response = client.get(
        "/api/commits",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['team'] == 'No commits in the last 7 days' 



## TESTS FOR TAHOMEPAGE API: /api/project/milecomps

def test_get_milecomp_not_loggedin(client,create_team, create_milestone, reset_db):
    """Test retrieving milestone completions without login."""
    dt = datetime.now() - timedelta(days=1)
    reset_db
    create_team(1)
    create_milestone(1)
    milestonedata = MilestoneStatus(
        team_id=1,
        milestone_id=1,
        milestone_status='Completed',
        completed_date=dt
    )
    db.session.add(milestonedata)
    db.session.commit()
    response = client.get(
        "/api/project/milecomps",
    )
    assert response.status_code == 401


def test_get_milecomp_1milecomp(client, auth_headersTA, create_team, create_milestone, reset_db):
    """Test retrieving milestone completions with 1 completion in database."""
    # print(db.session.query(MilestoneStatus.completed_date).all())
    dt = datetime.now() - timedelta(days=1)
    reset_db
    create_team(1)
    create_milestone(1)
    milestonedata = MilestoneStatus(
        team_id=1,
        milestone_id=1,
        milestone_status='Completed',
        completed_date=dt
    )
    db.session.add(milestonedata)
    db.session.commit()
    print(db.session.query(MilestoneStatus.completed_date).all())
    response = client.get(
        "/api/project/milecomps",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert data[0]['team'] == "Sample Team 1"
    assert len(data) == 1


def test_get_milecomp_5milecomps_with2from1team(client, auth_headersTA, create_team, create_milestone, reset_db):
    """Test retrieving milestone completions with 5 completions in all, and 2 completions from 1 team."""
    dt1 = datetime.now() - timedelta(days=1)
    dt2 = datetime.now() - timedelta(days=2)
    dt3 = datetime.now() - timedelta(days=3)
    reset_db
    create_team(5)
    create_milestone(2)
    mstatus = [
        MilestoneStatus(team_id=1, milestone_id=1, milestone_status="Completed",completed_date=dt1),
        MilestoneStatus(team_id=1, milestone_id=2, milestone_status="Completed",completed_date=dt2),
        MilestoneStatus(team_id=2, milestone_id=1, milestone_status="Completed",completed_date=dt1),
        MilestoneStatus(team_id=3, milestone_id=1, milestone_status="Completed",completed_date=dt3),
        MilestoneStatus(team_id=4, milestone_id=2, milestone_status="Completed",completed_date=dt2)
    ]
    db.session.add_all(mstatus)
    db.session.commit()
    # print(db.session.query(MilestoneStatus.completed_date).all())
    response = client.get(
        "/api/project/milecomps",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert len(data) == 5  # Ensure all 5 milecomps are returned
    team1_milecomps = [milecomps for milecomps in data if milecomps['team'] == "Sample Team 1"]
    team2_milecomps = [milecomps for milecomps in data if milecomps['team'] == "Sample Team 2"]
    team3_milecomps = [milecomps for milecomps in data if milecomps['team'] == "Sample Team 3"]
    team4_milecomps = [milecomps for milecomps in data if milecomps['team'] == "Sample Team 4"]
    assert len(team1_milecomps) == 2
    assert len(team2_milecomps) == 1
    assert len(team3_milecomps) == 1
    assert len(team4_milecomps) == 1


def test_get_milecomps_noMilecomps(client, auth_headersTA, reset_db):
    """Test retrieving milestone completions when there are no completions in last 7 days."""
    reset_db
    response = client.get(
        "/api/project/milecomps",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['team'] == 'No milestone completions in the last 7 days' 

    
## TESTS FOR TAHOMEPAGE API: /api/submissions/uploads

def test_get_upload_not_loggedin(client,create_team, create_milestone, reset_db):
    """Test retrieving teams with uploads in last 7 days without login."""
    dt = datetime.now() - timedelta(days=1)
    reset_db
    create_team(1)
    create_milestone(1)
    uploaddata = Submission(
        team_id=1,
        milestone_id=1,
        submission_timestamp=dt
    )
    db.session.add(uploaddata)
    db.session.commit()
    response = client.get(
        "/api/submissions/uploads",
    )
    assert response.status_code == 401


def test_get_upload_1upload(client, auth_headersTA, create_team, create_milestone, reset_db):
    """Test retrieving uploads with 1 upload in database."""
    dt = datetime.now() - timedelta(days=1)
    reset_db
    create_team(1)
    create_milestone(1)
    uploaddata = Submission(
        team_id=1,
        milestone_id=1,
        submission_timestamp=dt
    )
    db.session.add(uploaddata)
    db.session.commit()
    response = client.get(
        "/api/submissions/uploads",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert data[0]['team'] == "Sample Team 1"
    assert len(data) == 1


def test_get_upload_5uploads_with2from1team(client, auth_headersTA, create_team, create_milestone, reset_db):
    """Test retrieving uploads with 5 uploads in all, and 2 uploads from 1 team."""
    dt1 = datetime.now() - timedelta(days=1)
    dt2 = datetime.now() - timedelta(days=2)
    dt3 = datetime.now() - timedelta(days=3)
    reset_db
    create_team(5)
    create_milestone(2)
    uploads = [
        Submission(team_id=1, milestone_id=1, submission_timestamp=dt1),
        Submission(team_id=1, milestone_id=2, submission_timestamp=dt3),
        Submission(team_id=2, milestone_id=1, submission_timestamp=dt2),
        Submission(team_id=3, milestone_id=1, submission_timestamp=dt1),
        Submission(team_id=4, milestone_id=2, submission_timestamp=dt1)
    ]
    db.session.add_all(uploads)
    db.session.commit()
    # print(db.session.query(MilestoneStatus.completed_date).all())
    response = client.get(
        "/api/submissions/uploads",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert len(data) == 5  
    team1_uploads = [uploads for uploads in data if uploads['team'] == "Sample Team 1"]
    team2_uploads = [uploads for uploads in data if uploads['team'] == "Sample Team 2"]
    team3_uploads = [uploads for uploads in data if uploads['team'] == "Sample Team 3"]
    team4_uploads = [uploads for uploads in data if uploads['team'] == "Sample Team 4"]
    assert len(team1_uploads) == 2
    assert len(team2_uploads) == 1
    assert len(team3_uploads) == 1
    assert len(team4_uploads) == 1


def test_get_uploads_noUploads(client, auth_headersTA, reset_db):
    """Test retrieving uploads when there are no uploads in last 7 days."""
    reset_db
    response = client.get(
        "/api/submissions/uploads",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['team'] == 'No uploads in the last 7 days' 


## TESTS FOR TAHOMEPAGE API: /api/users/pendusers

def test_get_pendusers_not_loggedin(client, reset_db):
    """Test retrieving users awaiting registration approval without a logging in."""
    reset_db
    user = User(
        first_name=f"Student1",
        last_name=f"Test1",
        password="password123",
        email=f"user@example.com",
        github_username=f"githubuser",
        discord_username=f"discorduser",
        user_type="Student",
        approval_status="Inactive"
    )
    db.session.add(user)
    db.session.commit()
    response = client.get(
        "/api/users/pendusers",
    )
    assert response.status_code == 401

def test_get_pendusers_0pending_user(client, auth_headersTA):
    """Test retrieving users with no users awaiting registration approval."""
    response = client.get(
        "/api/users/pendusers",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0


def test_get_pendusers_1pending_user(client, auth_headersTA):
    """Test retrieving users with 1 user awaiting registration approval."""
    user = User(
        first_name=f"Student1",
        last_name=f"Test1",
        password="password123",
        email=f"user@example.com",
        github_username=f"githubuserStu2",
        discord_username=f"discorduser",
        user_type="Student",
        approval_status="Inactive"
    )
    db.session.add(user)
    db.session.commit()
    response = client.get(
        "/api/users/pendusers",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['id'] == 2 
    assert len(data) == 1

def test_get_pendusers_2pending_users(client, auth_headersTA):
    """Test retrieving users with 2 users (TA and Student) awaiting registration approval."""
    userSt = User(
        first_name=f"Student1",
        last_name=f"Test1",
        password="password123",
        email=f"userSt@example.com",
        github_username=f"githubuserStu2",
        discord_username=f"discorduser",
        user_type="Student",
        approval_status="Inactive"
    )
    userTA = User(
        first_name=f"TA1",
        last_name=f"Test1",
        password="password123",
        email=f"userTA2@example.com",
        github_username=f"githubuserTA2",
        discord_username=f"discorduser",
        user_type="TA",
        approval_status="Inactive"
    )
    db.session.add_all([userSt, userTA])
    db.session.commit()
    response = client.get(
        "/api/users/pendusers",
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['id'] == 2 
    assert len(data) == 2

def test_post_approve_users_no_login(client, db):
    """Test approving a user without loggin in."""
    userSt = User(
        first_name=f"Studentx1",
        last_name=f"Testx1",
        password="password123",
        email=f"userStx@example.com",
        github_username=f"githubuserStux2",
        discord_username=f"discorduser",
        user_type="Student",
        approval_status="Inactive"
    )
    db.session.add(userSt)
    db.session.commit()
    payload = {
        "users": [
            {
                "user_id": 2,
                "approval_status": "Approved",
                "user_type": "Student"
            }
        ]}
    response = client.post(
        "/api/users/approve_users",
        data=json.dumps(payload)
    )
    assert response.status_code == 401

def test_post_approve_users_StuLogin(client, db, auth_headersStu):
    """Test approving a user with a student login."""
    userSt = User(
        first_name=f"Studentx1",
        last_name=f"Testx1",
        password="password123",
        email=f"userStx@example.com",
        github_username=f"githubuserStux2",
        discord_username=f"discorduser",
        user_type="Student",
        approval_status="Inactive"
    )
    db.session.add(userSt)
    db.session.commit()
    payload = {
        "users": [
            {
                "user_id": 2,
                "approval_status": "Approved",
                "user_type": "Student"
            }
        ]}
    response = client.post(
        "/api/users/approve_users",
        data=json.dumps(payload),
        headers={**auth_headersStu, "Content-Type": "application/json"}
    )
    assert response.status_code == 403

    

def test_post_approve_users_TAlogin(client, db, auth_headersTA):
    """Test approving a user with a TA login."""
    userSt = User(
        first_name=f"Studentx1",
        last_name=f"Testx1",
        password="password123",
        email=f"userStx@example.com",
        github_username=f"githubuserStux2",
        discord_username=f"discorduser",
        user_type="Student",
        approval_status="Inactive"
    )
    db.session.add(userSt)
    db.session.commit()
    payload = {
        "users": [
            {
                "user_id": 2,
                "approval_status": "Approved",
                "user_type": "Student"
            }
        ]}
    response = client.post(
        "/api/users/approve_users",
        data=json.dumps(payload),
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User approvals processed successfully"
    assert len(data["results"]) == 1
    assert data["results"][0]["user_id"] == userSt.user_id
    assert data["results"][0]["message"] == "User approval processed"
    updated_user = db.session.query(User).get(userSt.user_id)
    assert updated_user.approval_status == "Active"
    assert updated_user.user_type == "Student"

def test_post_approve_users_1TA1Stu(client, db, auth_headersTA):
    """Test approving 1TA and 1Student in a single request."""
    userSt = User(
        first_name=f"Studentx1",
        last_name=f"Testx1",
        password="password123",
        email=f"userStx@example.com",
        github_username=f"githubuserStux2",
        discord_username=f"discorduser",
        user_type="Student",
        approval_status="Inactive"
    )
    userTA = User(
        first_name=f"TAx1",
        last_name=f"TAx1",
        password="password123",
        email=f"userTAx@example.com",
        github_username=f"githubuserTAx2",
        discord_username=f"discorduser",
        user_type="Student",
        approval_status="Inactive"
    )
    db.session.add_all([userSt, userTA])
    db.session.commit()
    payload = {
        "users": [
            {
                "user_id": 2,
                "approval_status": "Approved",
                "user_type": "Student"
            },
            {
                "user_id": 3,
                "approval_status": "Approved",
                "user_type": "TA"
            }
        ]}
    response = client.post(
        "/api/users/approve_users",
        data=json.dumps(payload),
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User approvals processed successfully"
    assert len(data["results"]) == 2
    assert data["results"][0]["user_id"] == userSt.user_id
    assert data["results"][1]["user_id"] == userTA.user_id
    updated_user = db.session.query(User).get(userSt.user_id)
    assert updated_user.approval_status == "Active"
    assert updated_user.user_type == "Student"
    updated_user2 = db.session.query(User).get(userTA.user_id)
    assert updated_user2.approval_status == "Active"
    assert updated_user2.user_type == "TA"

def test_post_approve_users_invalid_JSON(client, db, auth_headersTA):
    """Test approving a user with a TA login."""
    userSt = User(
        first_name=f"Studentx1",
        last_name=f"Testx1",
        password="password123",
        email=f"userStx@example.com",
        github_username=f"githubuserStux2",
        discord_username=f"discorduser",
        user_type="Student",
        approval_status="Inactive"
    )
    db.session.add(userSt)
    db.session.commit()
    payload = [
            {
                "user_id": 2,
                "approval_status": "Approved",
                "user_type": "Student"
            }
        ]
    response = client.post(
        "/api/users/approve_users",
        data=json.dumps(payload),
        headers={**auth_headersTA, "Content-Type": "application/json"}
    )
    assert response.status_code == 422
