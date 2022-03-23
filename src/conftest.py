import pytest

from webapp.app import app, db
from webapp.models import User


@pytest.fixture()
def new_user():
    user = User("tomliuhyyd@gmail.com", "klg", "qwerty123")
    return user


@pytest.fixture()
def test_client():
    flask_app = app

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


@pytest.fixture()
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email="tomliuhyyd@gmail.com", password_plaintext="qwerty123")
    user2 = User(email="tomliuhyyd1@gmail.com",
                 password_plaintext="qwerty1234")
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()
    yield
    db.drop_all()


@pytest.fixture()
def login_default_user(test_client):
    test_client.post(
        "/login",
        data=dict(email="tomliuhyyd@gmail.com", password="qwerty123"),
        follow_redirects=True,
    )
    yield
    test_client.get("/logout", follow_redirects=True)
