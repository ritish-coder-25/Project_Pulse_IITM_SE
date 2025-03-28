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
from models import Project, User, Milestone
from db_test_helpers import db_create_student_user, db_create_ta_user, get_user_token_header, db_create_users_for_team, db_create_team_with_users, db_create_milestones

@pytest.fixture(scope='session')
def app():
    # Create a temporary directory for uploads
    upload_dir = tempfile.mkdtemp()
    """Create and configure a new app instance for each test session."""
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an in-memory database for testing
        "JWT_SECRET_KEY": "test-secret-key",  # Set a test JWT secret key
        "PROPAGATE_EXCEPTIONS": True,  # Propagate exceptions for better error messages
        "UPLOAD_FOLDER": upload_dir # Temp folder for uploads
    })

    with flask_app.app_context():
        _db.create_all()
        # Create a default project if your Team model requires it
        project = Project(
            project_topic="Test Project",
            statement="This is a test project.",
            document_url="https://example.com/project-docs"
        )
        _db.session.add(project)
        _db.session.commit()
        db_create_student_user(_db)
        create_milestones(_db, project)
        yield flask_app
        _db.drop_all()


def create_milestones(_db, project):
    db_create_milestones(_db, project)

@pytest.fixture(scope='session')
def db(app):
    """Provide a database fixture."""
    return _db

@pytest.fixture(scope='function', autouse=True)
def session(db):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = {
        'bind': connection,
        'binds': {}
    }
    #session = db.create_scoped_session(options=options)
    db.session.bind = connection
    db.session.begin_nested()

    #db.session = session

    yield db.session

    db.session.rollback()
    connection.close()
    db.session.remove()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def auth_headers(app):
    """Generate authentication headers using JWT."""
    with app.app_context():
        access_token = create_access_token(identity=1)  # Replace with appropriate user ID
        return {
            'Authorization': f'Bearer {access_token}'
        }

# @pytest.fixture
# def admin_auth_headers(app, db):
#     """Generate authentication headers for an admin user."""
#     admin_user = User(
#         first_name="Admin",
#         last_name="User",
#         student_email="admin.user@example.com",
#         user_type="admin",
#         marker="marker_admin"
#     )
#     db.session.add(admin_user)
#     db.session.commit()

#     access_token = create_access_token(identity=admin_user.id)
#     return {
#         'Authorization': f'Bearer {access_token}'
#     }

@pytest.fixture
def create_student_user(db, team_id = None, approval_status="Active"):
    """Create multiple sample users for testing."""
    user, password = db_create_student_user(db, team_id, approval_status)
    return user, password

@pytest.fixture
def create_ta_user(db, approval_status="Active"):
    """Create multiple sample users for testing."""
    user, password = db_create_ta_user(db, approval_status)
    return user, password


@pytest.fixture
def create_users_for_team(db,create_student_user, team_id = None,no_of_users=7):
    """Create multiple sample users for a team."""
    users = db_create_users_for_team(db, team_id, no_of_users)
    return users

@pytest.fixture
def create_team_with_users(db,create_users_for_team, project_id=1):
    """Create team with multiple users."""
    team, team_users, team_lead = db_create_team_with_users(db, project_id)

    return team, team_users, team_lead


@pytest.fixture
def sample_file():
    return (io.BytesIO(b"Sample file content"), 'test_project.zip')

@pytest.fixture
def sample_file_invalid():
    return (io.BytesIO(b"Sample file content"), 'test_project.invalid')