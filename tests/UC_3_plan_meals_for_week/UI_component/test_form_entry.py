def test_generatemealplan(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mealplan' page is posted to (POST) when the user enters health requirements data

    """
    response = test_client.post(
        "/mealplan",
        data=dict(Calories="2000", Carbs="20", Proteins="6"),
        follow_redirects=True,
    )
    assert response.status_code == 200

def test_diet_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is requested
    THEN check that the response is valid
    """
    response = test_client.get("/diet/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Enter your Diet/Nutrition Preferences" in response.data

