import json
import sys
import random
import base64
import pytest
import itertools
from webapp import mealplan
from webapp import data_src


#Functions to test that a given datastructure is valid
#Written to be used in other test code 
def sample_nutritional_values():
    nutritionalvalues = data_src.nutritional_values()
    for i in nutritionalvalues:
        nutritionalvalues[i] = int(random.random() * 200)
    return nutritionalvalues

def sample_recipe():
    recipe = data_src.recipe_data()
    recipe["name"] = str(base64.b64encode(random.randbytes(20)))
    for i in range(random.randint(3, 20)):
        recipe["ingredients"].append(str(base64.b64encode(random.randbytes(20))))
    recipe["nutritional value"] = sample_nutritional_values()
    return recipe

def sample_meal_plan():
    meal_plan = data_src.meal_plan()
    meal_plan[0] = sample_recipe()
    meal_plan[1] = sample_recipe()
    meal_plan[2] = sample_recipe()
    return meal_plan

def sample_health_reqs():
    return sample_nutritional_values()

@pytest.mark.parametrize("nv", [(sample_nutritional_values())])
def test_nutritional_values(nv):
    template_nv = data_src.nutritional_values()
    for i in template_nv:
        assert(i in nv)
        assert(type(nv[i]) == type(template_nv[i]))
    return

@pytest.mark.parametrize("rd", [(sample_recipe())])
def test_recipe_data(rd):
    template_rd = data_src.recipe_data()
    for i in template_rd:
        assert(i in rd)
    assert("name" in rd)
    assert(type(rd["name"]) == type(template_rd["name"]))
    assert("ingredients" in rd)
    assert(type(rd["ingredients"]) == type(template_rd["ingredients"]))
    for i in rd["ingredients"]:
        assert(type(i) == str)
    test_nutritional_values(rd["nutritional value"])
    return

@pytest.mark.parametrize("mp", [(sample_meal_plan())])
def test_meal_plan(mp):
    for i in mp:
        test_recipe_data(i)
    return

@pytest.mark.xfail(reason="testing bad nutritional values")
class TestBadNVs:
    def test_good_nutritional_values(self):
        nv = sample_nutritional_values()
        test_nutritional_values(nv)
    def test_bad_calories(self):
        nv = sample_nutritional_values()
        nv["calories"] = "yabba dabba doo"
        test_nutritional_values(nv)
        return
    def test_missing_something(self):
        nv = sample_nutritional_values()
        idx = random.choice(nv)
        nv.pop(idx)
        test_nutritional_values(nv)
    def test_bad_something(self):
        nv = sample_nutritional_values()
        idx = random.choice(nv)
        nv[idx] = "yabba dabba doo"
        test_nutritional_values(nv)
    def test_missing_item(self):
        nv = sample_nutritional_values()
        nv.pop("vitaminA")
        test_nutritional_values(nv)
        return

@pytest.mark.xfail(reason="testing bad recipe data")
class TestBadRDs:
    def test_good_recipe(self):
        rd = sample_recipe()
        test_recipe_data(rd)
    def test_bad_ingredient(self):
        rd = sample_recipe()
        rd["ingredients"].append(True)
        test_recipe_data(rd)
    def test_bad_name(self):
        rd = sample_recipe()
        rd["name"] = None
        test_recipe_data(rd)
    def test_bad_nv(self):
        rd = sample_recipe()
        rd["nutritional value"].pop("vitaminA")
        test_recipe_data(rd)
    def test_empty_recipe(self):
        rd = dict()
        test_recipe_data(rd)

@pytest.mark.xfail(reason="testing bad meal plan")
class TestBadMPs:
    def test_good_meal_plan(self):
        mp = sample_meal_plan()
        test_meal_plan(mp)
    def test_bad_recipe_ingredient(self):
        mp = sample_meal_plan()
        mp[0]["ingredients"].append(0.24)
        test_meal_plan(mp)
    def test_empty_mp(self):
        mp = []
        test_meal_plan(mp)


class TestGoodData:
    def test_all(self):
        mp = sample_meal_plan()
        test_meal_plan(mp)
        for i in mp:
            test_recipe_data(i)
            test_nutritional_values(i["nutritional value"])
