import base64
import itertools
import json
import random
import sys
from curses.ascii import SO

import pytest
import pathlib

from webapp.app import app
from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator
from webapp.models import Recipes, User, Exercise, db

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
def mpg_class(nv1):
    return MealplanGenerator(json.dumps(nv1), '{"calorie_split": [0.25, 0.25, 0.5], "protein_split": [0.25, 0.25, 0.5], "carbs_split": [0.25, 0.25, 0.5]}')


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
def init_database_load(test_client, request):
    # Create the database and the database table
    # and add two sample recipes
    file = pathlib.Path(request.node.fspath)
    data = file.with_name('r2.json')

    db.drop_all()
    db.init_app(app)
    db.create_all(app=app)
    
    with data.open() as r:
        for jsline in r:
            fixme = json.loads(jsline.strip())
            for i in fixme["nutritional_values"]:
                fixme["nutritional_values"][i] = float(
                    fixme["nutritional_values"][i])
            new_recipe = Recipes(json.dumps(fixme))
            db.session.add(new_recipe)

    data = file.with_name('homeworkouts_org_exercises.json')
    
    with data.open() as r:
        for jsline in r:
            new_exercise = Exercise(json_str=jsline)
            db.session.add(new_exercise)
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
def nv1(test_client):
    nutritionalvalues = DataStructures.nutritional_values()
    for i in nutritionalvalues:
        nutritionalvalues[i] = random.random() * 200
    return nutritionalvalues


@pytest.fixture
def nv2(test_client):
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
def sample_health_reqs(nv1):
    return nv1
