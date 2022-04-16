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
from webapp.exerciseplan import ExerciseplanGenerator

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
    return MealplanGenerator(json.dumps(nv1))


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

    adobo_chicken = Recipes(
        name="Adobo Chicken",
        Calories=107.0,
        Carbs=2.48,
        Proteins=11.88,
        fat=4.93,
        Sodium=392.0,
        Vitamina=9.0,
        Calcium=14.0,
        Iron=1.05,
        Potassium=147.0,
    )
    ice_cream_sandwich = Recipes(
        name="Ice Cream Sandwich",
        Calories=143.0,
        Carbs=21.75,
        Proteins=2.61,
        fat=5.6,
        Cholesterol=20.0,
        Sodium=37.0,
        Vitamina=53.0,
        Calcium=60.0,
        Iron=0.28,
        Potassium=122.0,
    )

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

@pytest.fixture
def e1():
    e1 = DataStructures.exercise()
    e1["name"] = "Test Exercise 1"
    e1["targetmusclegroups"] = ["biceps", "triceps", "abs", "glutes"]
    e1["level"] = 3
    e1["sets"] = 12
    e1["reps"] = 42
    return e1

@pytest.fixture
def e2():
    e2 = DataStructures.exercise()
    e2["name"] = "Test Exercise 2"
    e2["targetmusclegroups"] = ["biceps", "triceps", "quads", "glutes"]
    e2["level"] = 3
    e2["sets"] = 12
    e2["reps"] = 42
    return e2

@pytest.fixture
def e3():
    e3 = DataStructures.exercise()
    e3["name"] = "Test Exercise 3"
    e3["targetmusclegroups"] = ["traps", "hamstrings", "quads"]
    e3["level"] = 3
    e3["sets"] = 12
    e3["reps"] = 42
    return e3

@pytest.fixture
def er1():
    er = DataStructures.exercise_reqs()
    er["days"]["Monday"] = True
    er["days"]["Wednesday"] = True
    er["days"]["Friday"] = True
    er["level"] = 3
    er["targetmusclegroups"] = ["biceps", "triceps", "abs", "glutes"]
    return er

@pytest.fixture
def epg_class(er1):
    return ExerciseplanGenerator(json.dumps(er1))
