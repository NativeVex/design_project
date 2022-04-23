import base64
import itertools
import json
import random
import sys
from curses.ascii import SO

import pytest

from webapp.app import app, db
from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator
from webapp.models import Recipes, User

# Functions to test that a given datastructure is valid
# Written to be used in other test code
random.seed(0)

# Put db.init_app(app) and db.create_all(app=app) in here.
# Drop all tables as a fixure and then create database.
# define what the variables are for this use case


@pytest.fixture
def health_reqs():
    return sample_health_reqs()


@pytest.fixture
def json_recipe_list(recipe_list):
    ls = []
    for i in recipe_list:
        ls.append(json.dumps(i))
    return ls


@pytest.fixture
def s1():
    return '{"calorie_split": [0.25, 0.25, 0.5], "protein_split": [0.25, 0.25, 0.5], "carbs_split": [0.25, 0.25, 0.5]}'


@pytest.fixture
def mpg_class(nv1, s1):
    return MealplanGenerator(json.dumps(nv1), s1)


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
    db.drop_all()
    db.init_app(app)
    db.create_all(app=app)
    yield


@pytest.fixture()
def init_database_recipes(test_client):
    # Create the database and the database table
    # and add two sample recipes
    db.drop_all()
    db.init_app(app)
    db.create_all(app=app)

    adobo_chicken_dict = DataStructures.recipe_data()
    adobo_chicken_dict["name"] = "Adobo Chicken"
    adobo_chicken_dict["ingredients"] = ["Chicken", "Adobo Sauce"]
    adobo_chicken_dict["directions"] = ["Mix chicken and adobo sauce"]
    adobo_chicken_dict["nutritional_values"]["calcium"] = 14.0
    adobo_chicken_dict["nutritional_values"]["calories"] = 107.0
    adobo_chicken_dict["nutritional_values"]["carbohydrate"] = 2.48
    adobo_chicken_dict["nutritional_values"]["fat"] = 4.93
    adobo_chicken_dict["nutritional_values"]["iron"] = 1.05
    adobo_chicken_dict["nutritional_values"]["potassium"] = 147.0
    adobo_chicken_dict["nutritional_values"]["protein"] = 11.88
    adobo_chicken_dict["nutritional_values"]["sodium"] = 392.0
    adobo_chicken_dict["nutritional_values"]["vitamin_a"] = 9.0
    adobo_chicken_dict["number_of_servings"] = 1
    adobo_chicken_dict["type"] = ["Lunch"]
    ice_cream_sandwich_dict = DataStructures.recipe_data()
    ice_cream_sandwich_dict["name"] = "Ice Cream Sandwich"
    ice_cream_sandwich_dict["ingredients"] = ["Ice Cream", "Sandwich"]
    ice_cream_sandwich_dict["directions"] = ["Open wrapper", "Eat"]
    ice_cream_sandwich_dict["nutritional_values"]["calcium"] = 60.0
    ice_cream_sandwich_dict["nutritional_values"]["calories"] = 143.0
    ice_cream_sandwich_dict["nutritional_values"]["carbohydrate"] = 21.75
    ice_cream_sandwich_dict["nutritional_values"]["fat"] = 5.60
    ice_cream_sandwich_dict["nutritional_values"]["iron"] = 0.28
    ice_cream_sandwich_dict["nutritional_values"]["potassium"] = 122.0
    ice_cream_sandwich_dict["nutritional_values"]["protein"] = 2.610
    ice_cream_sandwich_dict["nutritional_values"]["sodium"] = 37.00
    ice_cream_sandwich_dict["nutritional_values"]["vitamin_a"] = 53.0
    ice_cream_sandwich_dict["number_of_servings"] = 1
    ice_cream_sandwich_dict["type"] = ["Snack"]
    adobo_chicken = Recipes(json.dumps(adobo_chicken_dict))
    ice_cream_sandwich = Recipes(json.dumps(ice_cream_sandwich_dict))

    db.session.add(adobo_chicken)
    db.session.add(ice_cream_sandwich)
    db.session.commit()
    yield


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
def nv1(test_client, init_database_recipes):
    nutritionalvalues = DataStructures.nutritional_values()
    for i in nutritionalvalues:
        nutritionalvalues[i] = random.random() * 200
    return nutritionalvalues


@pytest.fixture
def nv2(test_client, init_database_recipes):
    nutritionalvalues = DataStructures.nutritional_values()
    for i in nutritionalvalues:
        nutritionalvalues[i] = random.random() * 200
    return nutritionalvalues


@pytest.fixture
def rd1(nv1):
    recipe = DataStructures.recipe_data()
    recipe["name"] = str(base64.b64encode(random.randbytes(20)))
    recipe["number_of_servings"] = 4
    recipe["type"] = ["Breakfast"]
    for i in range(random.randint(3, 20)):
        recipe["ingredients"].append(
            str(base64.b64encode(random.randbytes(20))))
        recipe["directions"].append(
            str(base64.b64encode(random.randbytes(20))))
    recipe["nutritional_values"] = nv1
    return recipe


@pytest.fixture
def rd2(nv1):
    recipe = DataStructures.recipe_data()
    recipe["name"] = str(base64.b64encode(random.randbytes(20)))
    recipe["number_of_servings"] = 33
    recipe["type"] = ["Lunch", "Main Dish"]
    for i in range(random.randint(3, 20)):
        recipe["ingredients"].append(
            str(base64.b64encode(random.randbytes(20))))
        recipe["directions"].append(
            str(base64.b64encode(random.randbytes(20))))
    recipe["nutritional_values"] = nv1
    return recipe


@pytest.fixture
def rd3(nv1):
    recipe = DataStructures.recipe_data()
    recipe["name"] = str(base64.b64encode(random.randbytes(20)))
    recipe["number_of_servings"] = 0.67
    recipe["type"] = ["Lunch", "Side Dish", "Snack"]
    for i in range(random.randint(3, 20)):
        recipe["ingredients"].append(
            str(base64.b64encode(random.randbytes(20))))
        recipe["directions"].append(
            str(base64.b64encode(random.randbytes(20))))
    recipe["nutritional_values"] = nv1
    return recipe


@pytest.fixture
def mp(rd1, rd2, rd3):
    meal_plan = DataStructures.meal_plan()
    meal_plan[0] = rd1
    meal_plan[1] = rd2
    meal_plan[2] = rd3
    return meal_plan


@pytest.fixture
def sample_health_reqs():
    return DataStructures.default_nutritional_values()


def sample_recipe_source():
    return [json.dumps(rd1()), json.dumps(rd2()), json.dumps(rd3())]


@pytest.fixture
def sample_recipe_source_fcn():
    return sample_recipe_source
