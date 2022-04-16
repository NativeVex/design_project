import base64
import itertools
import json
import random
import sys

import pytest

from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator

# Functions to test that a given datastructure is valid
# Written to be used in other test code
random.seed(0)


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


