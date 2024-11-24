import pytest
import os
from datetime import datetime
import json
from models import Team, Submission, File, Milestone, MilestoneStatus, User, Project

@pytest.fixture
def setup_test_data(session):
    """Setup test data for file submissions"""
    # Create test project
    project = Project(
        project_topic="Test Project",
        statement="Test Statement",
        document_url="http://example.com"
    )
    session.add(project)
    session.flush()

    # Create test team
    team = Team(
        team_name="Test Team",
        project_id=project.project_id
    )
    session.add(team)
    session.flush()

    # Create test milestone
    milestone = Milestone(
        milestone_name="Test Milestone",
        milestone_description="Test Description",
        end_date=datetime(2024, 12, 31),
        max_marks=100,
        start_date=datetime(2024, 1, 1),
        project_id=project.project_id
    )
    session.add(milestone)
    session.flush()

    # Create test submission
    submission = Submission(
        team_id=team.team_id,
        milestone_id=milestone.milestone_id,
        submission_timestamp=datetime(2024, 1, 1)
    )
    session.add(submission)
    session.flush()

    # Create test file
    test_file = File(
        file_name="test_file.txt",
        submission_id=submission.submission_id
    )

    test_nonexistent_file = File(
        file_name="nonexistent_file.txt",
        submission_id=submission.submission_id
    )
    with open("../file_submissions/test_file.txt", "w") as f:
        f.write("Test content")
    session.add(test_file)
    session.add(test_nonexistent_file)
    session.commit()

    # Create test file on disk
    os.makedirs("file_submissions", exist_ok=True)
    with open(os.path.join("file_submissions", "test_file.txt"), "w") as f:
        f.write("Test content")

    return {
        "team": team,
        "milestone": milestone,
        "submission": submission,
        "file": test_file
    }

def test_get_team_files(client, auth_headers, setup_test_data):
    """Test getting files for a specific team"""
    team = setup_test_data["team"]
    response = client.get(f"/api/files/{team.team_id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["documents"]) == 2
    assert data["documents"][0]["team"] == "Test Team"
    assert data["documents"][0]["name"] == "test_file.txt"

def test_get_team_files_nonexistent_team(client, auth_headers):
    """Test getting files for a non-existent team"""
    response = client.get("/api/files/99999", headers=auth_headers)
    assert response.status_code == 404

def test_download_file(client, auth_headers, setup_test_data):
    """Test downloading a file"""
    file = setup_test_data["file"]
    response = client.get(f"/api/download/{file.file_id}", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == f'attachment; filename=test_file.txt'

def test_download_nonexistent_file(client, auth_headers):
    """Test downloading a non-existent file"""
    response = client.get("/api/download/99999", headers=auth_headers)
    assert response.status_code == 500

def test_create_milestone_review(client, auth_headers, setup_test_data):
    """Test creating a milestone review"""
    team = setup_test_data["team"]
    milestone = setup_test_data["milestone"]
    
    review_data = {
        "team_id": team.team_id,
        "milestone_id": milestone.milestone_id,
        "team_score": 85,
        "feedback": "Good work!",
        "max_milestone_score": 100
    }
    
    response = client.post(
        "/api/milestone-review",
        headers=auth_headers,
        json=review_data
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "Milestone review saved successfully."

def test_get_milestone_reviews(client, auth_headers, setup_test_data):
    """Test getting all milestone reviews"""
    response = client.get("/api/milestone-review", headers=auth_headers)
    assert response.status_code == 200

def test_update_milestone_review(client, auth_headers, setup_test_data):
    """Test updating a milestone review"""
    # First create a review
    team = setup_test_data["team"]
    milestone = setup_test_data["milestone"]
    
    milestone_status = MilestoneStatus(
        team_id=team.team_id,
        milestone_id=milestone.milestone_id,
        milestone_status="Evaluated",
        eval_score=80,
        eval_feedback="Initial feedback"
    )
    session = setup_test_data["team"].query.session
    session.add(milestone_status)
    session.commit()

    # Update the review
    update_data = {
        "team_score": 90,
        "feedback": "Updated feedback"
    }
    
    response = client.put(
        f"/api/milestone-review/{milestone_status.milestonestatus_id}",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Milestone review updated successfully."

def test_delete_milestone_review(client, auth_headers, setup_test_data):
    """Test deleting an existing milestone review"""
    team = setup_test_data["team"]
    milestone = setup_test_data["milestone"]
    
    # Create a milestone status to delete
    milestone_status = MilestoneStatus(
        team_id=team.team_id,
        milestone_id=milestone.milestone_id,
        milestone_status="Evaluated",
        eval_score=80,
        eval_feedback="Initial feedback"
    )
    session = setup_test_data["team"].query.session
    session.add(milestone_status)
    session.commit()

    response = client.delete(f"/api/milestone-review/{milestone_status.milestonestatus_id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Milestone review deleted successfully."

def test_delete_nonexistent_milestone_review(client, auth_headers):
    """Test deleting a non-existent milestone review"""
    response = client.delete("/api/milestone-review/99999", headers=auth_headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["errorCode"] == "not_found"
    assert data["message"] == "Milestone review not found."

def test_delete_milestone_review_invalid_id(client, auth_headers):
    """Test deleting a milestone review with an invalid ID"""
    response = client.delete("/api/milestone-review/invalid_id", headers=auth_headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["errorCode"] == "not_found"
    assert data["message"] == "Milestone review not found."

def teardown_module(module):
    """Clean up test files after tests"""
    if os.path.exists("file_submissions/test_file.txt"):
        os.remove("file_submissions/test_file.txt")
    if os.path.exists("file_submissions"):
        os.rmdir("file_submissions")