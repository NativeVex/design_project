import base64
import itertools
import json
import random
import sys

import pytest

from webapp.app import app, db
from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator
from webapp.models import User

# Functions to test that a given datastructure is valid
# Written to be used in other test code
random.seed(0)

# Put db.init_app(app) and db.create_all(app=app) in here.
# Drop all tables as a fixure and then create database.


@pytest.fixture()
def new_user():
    user = User("tomliuhyyd@gmail.com", "klg", "qwerty123")
    return user


@pytest.fixture()
def test_client():
    flask_app = app

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


@pytest.fixture()
def init_database(test_client):
    # Create the database and the database table
    db.init_app(app)
    db.create_all(app=app)
    yield
    db.drop_all()


@pytest.fixture()
def login_default_user(test_client):
    test_client.post(
        "/login",
        data=dict(email="tomliuhyyd@gmail.com", password="qwerty123"),
        follow_redirects=True,
    )
    yield
    test_client.get("/logout", follow_redirects=True)


@pytest.fixture
def nv1():
    nutritionalvalues = DataStructures.nutritional_values()
    for i in nutritionalvalues:
        nutritionalvalues[i] = random.random() * 200
    return nutritionalvalues


@pytest.fixture
def nv2():
    nutritionalvalues = DataStructures.nutritional_values()
    for i in nutritionalvalues:
        nutritionalvalues[i] = random.random() * 200
    return nutritionalvalues


@pytest.fixture
def rd1(nv1):
    recipe = DataStructures.recipe_data()
    recipe["name"] = str(base64.b64encode(random.randbytes(20)))
    for i in range(random.randint(3, 20)):
        recipe["ingredients"].append(
            str(base64.b64encode(random.randbytes(20))))
    recipe["nutritional value"] = nv1
    return recipe


@pytest.fixture
def rd2(nv1):
    recipe = DataStructures.recipe_data()
    recipe["name"] = str(base64.b64encode(random.randbytes(20)))
    for i in range(random.randint(3, 20)):
        recipe["ingredients"].append(
            str(base64.b64encode(random.randbytes(20))))
    recipe["nutritional value"] = nv1
    return recipe


@pytest.fixture
def rd3(nv1):
    recipe = DataStructures.recipe_data()
    recipe["name"] = str(base64.b64encode(random.randbytes(20)))
    for i in range(random.randint(3, 20)):
        recipe["ingredients"].append(
            str(base64.b64encode(random.randbytes(20))))
    recipe["nutritional value"] = nv1
    return recipe


@pytest.fixture
def mp(rd1, rd2, rd3):
    meal_plan = DataStructures.meal_plan()
    meal_plan[0] = rd1
    meal_plan[1] = rd2
    meal_plan[2] = rd3
    return meal_plan


@pytest.fixture
def sample_health_reqs(nv1):
    return nv1


def test_nutritional_values(nv1):
    template_nv = DataStructures.nutritional_values()
    for i in template_nv:
        assert i in nv1
        assert type(nv1[i]) == type(template_nv[i])
    return


def test_recipe_data(rd1):
    template_rd = DataStructures.recipe_data()
    for i in template_rd:
        assert i in rd1
    assert "name" in rd1
    assert type(rd1["name"]) == type(template_rd["name"])
    assert "ingredients" in rd1
    assert type(rd1["ingredients"]) == type(template_rd["ingredients"])
    for i in rd1["ingredients"]:
        assert type(i) == str
    test_nutritional_values(rd1["nutritional value"])
    return


def test_meal_plan(mp):
    for i in mp:
        test_recipe_data(i)
    return


@pytest.mark.xfail(reason="testing bad nutritional values")
class TestBadNVs:

    def test_good_nutritional_values(self, nv1):
        test_nutritional_values(nv1)

    def test_bad_calories(self, nv2):
        nv2["calories"] = "yabba dabba doo"
        test_nutritional_values(nv2)
        return

    def test_missing_something(self, nv2):
        idx = random.choice(nv2)
        nv2.pop(idx)
        test_nutritional_values(nv2)

    def test_bad_something(self, nv2):
        idx = random.choice(nv2)
        nv2[idx] = "yabba dabba doo"
        test_nutritional_values(nv2)

    def test_missing_item(self, nv2):
        nv2.pop("vitaminA")
        test_nutritional_values(nv2)
        return

    def test_good_nutritional_values(self, nv2):
        test_nutritional_values(nv2)


@pytest.mark.xfail(reason="testing bad recipe data")
class TestBadRDs:

    def test_good_recipe(self, rd1):
        test_recipe_data(rd1)

    def test_bad_ingredient(self, rd1):
        rd1["ingredients"].append(True)
        test_recipe_data(rd1)

    def test_bad_name(self, rd1):
        rd1["name"] = None
        test_recipe_data(rd1)

    def test_bad_nv(self, rd1):
        rd["nutritional value"].pop("vitaminA")
        test_recipe_data(rd)

    def test_missing_something(self, rd1):
        idx = random.choice(rd)
        rd.pop(idx)

    def test_empty_recipe(self):
        rd = dict()
        test_recipe_data(rd)

    def test_good_recipe(rd1, self):
        test_recipe_data(rd1)


@pytest.mark.xfail(reason="testing bad meal plan")
class TestBadMPs:

    def test_good_meal_plan(self, mp):
        test_meal_plan(mp)

    def test_bad_recipe_ingredient(self, mp):
        mp[0]["ingredients"].append(0.24)
        test_meal_plan(mp)

    def test_empty_mp(self):
        mp = []
        test_meal_plan(mp)

    def test_good_meal_plan(self, mp):
        test_meal_plan(mp)


class TestGoodData:

    def test_all(self, mp):
        test_meal_plan(mp)
        for i in mp:
            test_recipe_data(i)
            test_nutritional_values(i["nutritional value"])
