import pytest
from main import app, db
from flask_jwt_extended import create_access_token


# Fixtures
@pytest.fixture(scope="session")
def app_fixture():
    """Create a test app."""
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory DB for testing
            "JWT_SECRET_KEY": "test-secret-key",
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app_fixture):
    """Fixture to provide a test client."""
    with app_fixture.test_client() as client:
        yield client


@pytest.fixture
def auth_header(app_fixture):
    """Fixture to create an authorization header."""
    with app_fixture.app_context():
        token = create_access_token(identity="test_user")
        return {"Authorization": f"Bearer {token}"}


# Helper Function
def seed_sample_data():
    """Seed the database with sample data."""
    from models import User, Commit, Milestone, Document

    # Add sample user
    user = User(username="test_user", email="test@example.com", password="hashed_pw")
    db.session.add(user)

    # Add sample commit
    commit = Commit(
        message="Initial commit", author="test_user", timestamp="2024-01-01"
    )
    db.session.add(commit)

    # Add sample milestone
    milestone = Milestone(
        name="Initial milestone", completed=True, timestamp="2024-01-01"
    )
    db.session.add(milestone)

    # Add sample document
    document = Document(
        name="Test Document", url="http://example.com/doc", uploaded_by="test_user"
    )
    db.session.add(document)

    db.session.commit()


@pytest.fixture(autouse=True)
def setup_and_teardown(app_fixture):
    """Automatically seed and rollback data for every test."""
    seed_sample_data()
    yield
    db.session.rollback()


# Tests
class TestCommitsAPI:
    def test_tad_commits_retrieval(self, client, auth_header):
        """Test retrieving commits through TADcommits API."""
        response = client.get("/api/commits", headers=auth_header)
        assert response.status_code == 200
        assert isinstance(response.json, list)

    @pytest.mark.parametrize(
        "auth_header, expected_status",
        [(None, 401), ({"Authorization": "Bearer invalid_token"}, 401)],
    )
    def test_tad_commits_unauthorized(self, client, auth_header, expected_status):
        """Test unauthorized access to TADcommits API."""
        response = client.get("/api/commits", headers=auth_header)
        assert response.status_code == expected_status


class TestMilestonesAPI:
    def test_tad_milestones(self, client, auth_header):
        """Test retrieving milestones."""
        response = client.get("/api/project/milecomps", headers=auth_header)
        assert response.status_code == 200
        assert "milestones" in response.json

    def test_tad_milestones_unauthorized(self, client):
        """Test unauthorized access to milestones API."""
        response = client.get("/api/project/milecomps")
        assert response.status_code == 401


class TestDocumentUploadsAPI:
    def test_tad_docupload(self, client, auth_header):
        """Test retrieving document uploads."""
        response = client.get("/api/submissions/uploads", headers=auth_header)
        assert response.status_code == 200
        assert "uploads" in response.json


class TestUserApprovalAPI:
    def test_user_approval(self, client, auth_header):
        """Test approving a user."""
        payload = {"user_id": 1, "approve": True}
        response = client.post(
            "/api/users/approve_users", json=payload, headers=auth_header
        )
        assert response.status_code == 200
        assert response.json["status"] == "approved"

    def test_user_approval_invalid_user(self, client, auth_header):
        """Test approving a non-existent user."""
        payload = {"user_id": 999, "approve": True}
        response = client.post(
            "/api/users/approve_users", json=payload, headers=auth_header
        )
        assert response.status_code == 404
        assert response.json["message"] == "User not found"


class TestPendingUsersAPI:
    def test_pending_users(self, client, auth_header):
        """Test fetching pending users."""
        response = client.get("/api/users/pendusers", headers=auth_header)
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_pending_users_unauthorized(self, client):
        """Test unauthorized access to pending users API."""
        response = client.get("/api/users/pendusers")
        assert response.status_code == 401
