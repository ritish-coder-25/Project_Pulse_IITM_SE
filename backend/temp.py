# from faker import Faker
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import db, User  # Replace `your_application` with your app's module
# from flask_bcrypt import Bcrypt


# bcrypt = Bcrypt()
# # Initialize Faker
# fake = Faker()

# # Path to your SQLite database file
# DATABASE_FILE = "app.db"  # Update with your SQLite file path

# # SQLite connection
# engine = create_engine(f"sqlite:///{DATABASE_FILE}")
# Session = sessionmaker(bind=engine)

# # Create 10 fake student users
# def create_fake_users(session, num_users=10):
#     for _ in range(num_users):
#         user = User(
#             first_name=fake.first_name(),
#             last_name=fake.last_name(),
#             email=fake.unique.email(),
#             password=bcrypt.generate_password_hash("12345678").decode(
#                     "utf-8"
#                 ),
#             github_username=fake.unique.user_name(),
#             discord_username=f"{fake.user_name()}#{fake.random_int(1000, 9999)}",
#             user_type='Student',
#             approval_status='Inactive',
#             team_id=None,  # Assuming team_id is optional
#         )
#         session.add(user)
#     session.commit()
#     print(f"Added {num_users} fake users to the database.")

# # Main execution block
# if __name__ == "__main__":
#     session = Session()

#     try:
#         create_fake_users(session)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         session.rollback()
#     finally:
#         session.close()


from datetime import datetime, timedelta
from faker import Faker
from models import db, Milestone, Project  # Replace `your_application` with your app's module

# Initialize Faker
fake = Faker()

# Function to generate 5 fake milestones
def create_fake_milestones(session, num_milestones=5):
    for _ in range(num_milestones):
        # Generate fake milestone data
        milestone = Milestone(
            milestone_name=fake.bs(),  # Fake business slogan for the name
            milestone_description=fake.text(max_nb_chars=200),  # Fake text for description
            start_date=fake.date_this_year(),  # Random start date this year
            end_date=fake.date_this_year(),  # Random end date this year
            max_marks=fake.random_number(digits=2),  # Random number for max_marks
            project_id=1  # Random project ID (Assuming project_id between 1 and 5)
        )
        
        # Ensure end date is after start date
        if milestone.end_date < milestone.start_date:
            milestone.end_date = milestone.start_date + timedelta(days=fake.random_int(min=1, max=30))
        
        session.add(milestone)
    
    session.commit()
    print(f"Added {num_milestones} fake milestones to the database.")

# Main execution block
if __name__ == "__main__":
    # Configure session
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    
    engine = create_engine("sqlite:///app.db")  # Replace with your actual SQLite database path
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        create_fake_milestones(session)
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
