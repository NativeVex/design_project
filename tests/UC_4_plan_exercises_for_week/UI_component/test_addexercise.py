import pytest
@pytest.mark.xfail(reason="not yet implemented")
def test_add_exercise(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mealplan' page is posted to (POST) when the user enters health requirements data

    """
    response = test_client.post(
        "/addexercise",
        data=dict(
            name="newexercise",
            sets="9",
            reps="10",
            intensity="7",
            muscles=["quads", "abs", "hamstrings"],
        ),
        follow_redirects=True,
    )
    assert b"newexercise" in response.data
    assert response.status_code == 200

