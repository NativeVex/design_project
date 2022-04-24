import pytest

@pytest.mark.xfail(reason="not yet implemented")
def test_generate_exercise_plan(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mealplan' page is posted to (POST) when the user enters health requirements data

    """
    response = test_client.post(
        "/exerciseplan",
        data=dict(sunday=True, friday=True,
                  intensity="8", glutes=True, chest=True),
        follow_redirects=True,
    )
    assert b"Personal Exercise Plan Recommendations" in response.data
    assert response.status_code == 200

