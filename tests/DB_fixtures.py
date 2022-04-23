# --- DB FIXTURES
import pytest
from flask import Flask

from webapp.app import create_app, db
from webapp.models import User


@pytest.fixture()
def test_client():
    """
    In the future, if we copy paste, can we link our sources? It makes
    debugging a little more sane.
    https://testdriven.io/blog/flask-pytest/
    """

    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client
            db.session.remove()
            db.drop_all()


@pytest.fixture()
def register_sample_account(
    test_client, username="ANYTHING", email="anything@gmail.com", password="some"
):
    sample = User(email=email, username=username, password_plaintext=password)
    db.session.add(sample)
    db.session.commit()


# deleted init_database here b.c. there was functionality being duplicated from
# setup function


@pytest.fixture()
def login_default_user(test_client):
    test_client.post(
        "/login",
        data=dict(email="anything@gmail.com", password="some"),
        follow_redirects=True,
    )
    yield
    test_client.get("/logout", follow_redirects=True)
