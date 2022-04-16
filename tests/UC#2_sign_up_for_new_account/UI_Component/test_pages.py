def test_signup_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is requested
    THEN check that the response is valid
    """
    response = test_client.get("/signup/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign Up for a New Health/Diet Planner Account" in response.data
