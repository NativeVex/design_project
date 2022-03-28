import json
import sys

from webapp import *


def test_signupfornewaccountintegration(test_client):
    """integration test for going to sign up page and then
    having user send form data for their email, username, and password"""
    response1 = test_client.get("/signup/",follow_redirects=True)
    assert response1.status_code == 200
    response = test_client.post(
        "/signup/",
        data=dict(email="any@gmail.com", username="newuser", password="some"),
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_signintoexistingaccountintegration(test_client):
    """integration test for going to sign in page and then
    having user send form data for their username, and password"""
    response1 = test_client.get("/",follow_redirects=True)
    assert response1.status_code == 200
    response = test_client.post(
        "/",
        data=dict(email="any@gmail.com", username="newuser", password="some"),
        follow_redirects=True,
    )
    assert response.status_code == 200

def test_generatemealplanintegration(test_client):
    """integration test for going to mealplanner page and then
    having user send form data for their diet health requirements of calories,carbs,proteins"""
    response1 = test_client.get("/mealplan",follow_redirects=True)
    assert response1.status_code == 200
    response = test_client.post('/mealplan',
                                data=dict(Calories='2000', Carbs='20',Proteins='6'),follow_redirects=True)
    assert response.status_code == 200    
