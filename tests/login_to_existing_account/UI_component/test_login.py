def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login to your Health/Diet Planner Account" in response.data

