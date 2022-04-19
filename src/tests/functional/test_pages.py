from urllib import response

import pytest

from webapp.app import User, app, db


def test_signup(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is posted to (POST) when the user enters signup information

    """

    response = test_client.post(
        "/signup/",
        data=dict(email="anyperson@gmail.com",
                  username="foods",
                  password="some"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Login to your Health/Diet Planner Account" in response.data


def test_dupe_signup(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is posted to (POST) when the user enters signup information

    """
    test_client.post(
        "/signup/",
        data=dict(email="anything@gmail.com",
                  username="newuser",
                  password="some"),
        follow_redirects=True,
    )

    response = test_client.post(
        "/signup/",
        data=dict(email="anything@gmail.com",
                  username="newuser",
                  password="some"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Email address already exists" in response.data


def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login to your Health/Diet Planner Account" in response.data


def test_login_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check the response is valid when users enter their username and password
    """
    response = test_client.post(
        "/",
        data=dict(email="anything@gmail.com", password="some"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Enter your Diet/Nutrition Preferences" in response.data


def test_login_failed(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (POST)
    THEN check that the response is valid
    """
    response = test_client.post("/",
                                data=dict(email="any@gmail.com",
                                          password="notsome"),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Please check your login details and try again." in response.data


def test_generate_mealplan(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mealplan' page is posted to (POST) when the user enters health requirements data

    """
    response = test_client.post(
        "/mealplan",
        data=dict(
            Calories="129.7",
            Carbs="57.6",
            Proteins="68.5",
            fiber="75.9",
            caloriesbreakfastamount=".7",
            calorieslunchamount=".9",
            carbsbreakfastamount=".3",
            carbslunchamount=".6",
            proteinsbreakfastamount=".35",
            proteinslunchamount=".55",
        ),
        follow_redirects=True,
    )
    assert b"Personal Meal Plan Recommendations" in response.data
    assert response.status_code == 200


def test_generate_exercise_plan(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mealplan' page is posted to (POST) when the user enters health requirements data

    """
    response = test_client.post(
        "/exerciseplan",
        data=dict(tuesday=True,
                  friday=True,
                  intensity="8",
                  glutes=True,
                  cardio=True,
                  chest=True),
        follow_redirects=True,
    )
    assert b"Personal Exercise Plan Recommendations" in response.data
    assert response.status_code == 200


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
    assert b"Exercise added!" in response.data
    assert response.status_code == 200


def test_add_food_item(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/mealplan' page is posted to (POST) when the user enters health requirements data

    """
    response = test_client.post(
        "/addfood",
        data=dict(
            newrecipename="apples",
            newrecipeingredients="any some foods",
            foodtype="lunch",
            numberofservings="7",
            newrecipedirections="food directions",
            newrecipecalories="87.6",
            newrecipecarbs="6",
            protein="72",
        ),
        follow_redirects=True,
    )
    assert b"Food recipe added!" in response.data
    assert response.status_code == 200

def test_change_health_requirements(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/changehealthrequirementss' page is posted to (POST) when the user enters health requirements data

    """
    response = test_client.get(    #going to change health requirements page to see current health configuration 
        "/changehealthrequirements",
        follow_redirects=True,
    )
    assert response.status_code==200
    response1 = test_client.post(   #selecting old health requirements option to see old health configuration
        "/getoldhealthrequirements",
        follow_redirects=True,
    )
    assert response1.status_code==200
    response2 = test_client.post(         #updating and saving new health configuration
        "/savenewhealthrequirements",
        data=dict(Calories="78.6", Carbs="47.9",Proteins="68.7",monounsaturated_fat="59.8",vitamin_a="45"),
        follow_redirects=True,
    )
    assert b"59.8" in response2.data
    assert response2.status_code == 200
    

@pytest.mark.xfail(reason="not yet implemented")
def test_points_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/points/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/points/")
    assert response.status_code == 200
    assert b"Points History Calendar" in response.data


def test_points_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/points/' page is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post("/points/")
    assert response.status_code == 405
    assert b"Points History Calendar" not in response.data


def test_signup_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is requested
    THEN check that the response is valid
    """
    response = test_client.get("/signup/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign Up for a New Health/Diet Planner Account" in response.data


def test_diet_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup/' page is requested
    THEN check that the response is valid
    """
    response = test_client.get("/diet/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Enter your Diet/Nutrition Preferences" in response.data
