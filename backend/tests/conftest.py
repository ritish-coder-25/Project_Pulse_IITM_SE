import pytest
from flask_jwt_extended import create_access_token
import sys
import os
from datetime import datetime
# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from main import app as flask_app
from main import db as _db
from models import Project, User

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an in-memory database for testing
        "JWT_SECRET_KEY": "test-secret-key",  # Set a test JWT secret key
        "PROPAGATE_EXCEPTIONS": True,  # Propagate exceptions for better error messages
    })

    with flask_app.app_context():
        _db.create_all()
                # Optionally, create a default project if your Team model requires it
        project = Project(
            project_topic="Test Project",
            statement="This is a test project.",
            document_url="https://example.com/project-docs"
        )
        _db.session.add(project)
        _db.session.commit()

        yield flask_app
        _db.drop_all()

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
def create_student_user(db, approval_status="Active"):
    """Create multiple sample users for testing."""
    curr_d_time = datetime.now()
    password = "password123"
    user = User(
            first_name=f"User-student{curr_d_time}",
            last_name=f"Test{curr_d_time}",
            password=password,
            email=f"user{curr_d_time}@example.com",
            github_username=f"githubuser{curr_d_time}",
            discord_username=f"discorduser{curr_d_time}",
            user_type="Student",
            approval_status=approval_status
        )
    db.session.add(user)
    db.session.commit()
    return user, password

@pytest.fixture
def create_ta_user(db, approval_status="Active"):
    """Create multiple sample users for testing."""
    curr_d_time = datetime.now()
    password = "password123"
    user = User(
            first_name=f"User-ta{curr_d_time}",
            last_name=f"Test{curr_d_time}",
            password=password,
            email=f"user-ta{curr_d_time}@example.com",
            github_username=f"githubuser-ta{curr_d_time}",
            discord_username=f"discorduser-ta{curr_d_time}",
            user_type="TA",
            approval_status=approval_status
        )
    db.session.add(user)
    db.session.commit()
    return user, password

def get_user_token_header(user_id): 
    access_token = create_access_token(identity=user_id)  # Replace with appropriate user ID
    return {
        'Authorization': f'Bearer {access_token}'
    }
