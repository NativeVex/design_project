from webapp.app import app


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = app

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get("/")
        # assert response.status_code == 200
        assert b"Login to your Health/Diet Planner Account" in response.data


def test_logintoexistingaccount(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check the response is valid when users enter their username and password
    """
    response = test_client.post("/",
                                data=dict(username="newuser",
                                          password="anything"),
                                follow_redirects=True)
    assert response.status_code == 200


def test_signupforaccount(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is posted to (POST) when the user enters signup information

    """
    response = test_client.post(
        "/signup/",
        data=dict(email="any@gmail.com", username="newuser", password="some"),
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_generatemealplan(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mealplan' page is posted to (POST) when the user enters health requirements data

    """
    response = test_client.post("/mealplan",
                                data=dict(Calories="2000",
                                          Carbs="20",
                                          Proteins="6"),
        follow_redirects=True)
    assert response.status_code == 200


def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/",follow_redirects=True)
    assert response.status_code == 200
    assert b"Login to your Health/Diet Planner Account" in response.data


def test_points_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/points/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/points/")
    assert response.status_code == 200
    assert b"Points History Calendar" in response.data


def test_points_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application
    WHEN the '/points/' page is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post("/points/")
    assert response.status_code == 405
    assert b"Points History Calendar" not in response.data


def test_signup_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is requested
    THEN check that the response is valid
    """
    response = test_client.get("/signup/",follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign Up for a New Health/Diet Planner Account" in response.data


def test_diet_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is requested
    THEN check that the response is valid
    """
    response = test_client.get("/diet/",follow_redirects=True)
    assert response.status_code == 200
    assert b"Enter your Diet/Nutrition Preferences" in response.data
