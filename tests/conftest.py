from webapp.app import app, db
import pytest

@pytest.fixture()
def test_client():
    flask_app = app

    # there's some code in app.py that initializes the db
    # db.drop_all() #TODO uncomment
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


@pytest.fixture()
def init_database(test_client):
    # Create the database and the database table
    db.drop_all() #TODO delete
    db.init_app(app)
    db.create_all(app=app)
    yield
    # db.drop_all() #TODO uncomment

