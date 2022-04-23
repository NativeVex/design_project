from webapp.models import User
from webapp.app import db

def test_UC2_E2E_1(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is posted to (POST) when the user enters signup information

    """

    assert db.session.query(User).filter(User.email == "anyperson@gmail.com").count() == 0
    response = test_client.post(
        "/signup/",
        data=dict(email="anyperson@gmail.com",
                  username="foods", password="some"),
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert db.session.query(User).filter(User.email == "anyperson@gmail.com").count() == 1
