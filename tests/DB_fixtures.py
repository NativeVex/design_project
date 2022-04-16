# --- DB FIXTURES
import pytest
from webapp.app import app, db
from flask import Flask

@pytest.fixture()
def test_client():
    """ Universal setup """
    flask_app = app

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client




@pytest.fixture()
def init_database(test_client):
    # Create the database and the database table
    db.init_app(app)
    db.create_all(app=app)
    yield
    db.drop_all()


# @pytest.fixture
# def test_client():
#     app = Flask(__name__)
#     app.config.from_pyfile(config_filename)

#     from yourapplication.model import db
#     db.init_app(app)

#     from yourapplication.views.admin import admin
#     from yourapplication.views.frontend import frontend
#     app.register_blueprint(admin)
#     app.register_blueprint(frontend)

#     return app

@pytest.fixture()
def login_default_user(test_client):
    test_client.post(
        "/login",
        data=dict(email="tomliuhyyd@gmail.com", password="qwerty123"),
        follow_redirects=True,
    )
    yield
    test_client.get("/logout", follow_redirects=True)


