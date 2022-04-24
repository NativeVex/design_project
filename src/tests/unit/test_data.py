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

# def test_nutritional_values(nv1):
#     template_nv = DataStructures.nutritional_values()
#     for i in template_nv:
#         assert i in nv1
#         assert type(nv1[i]) == type(template_nv[i])

# def test_recipe_data(rd1):
#     template_rd = DataStructures.recipe_data()
#     for i in template_rd:
#         assert i in rd1
#     assert "name" in rd1
#     assert type(rd1["name"]) == type(template_rd["name"])
#     assert "ingredients" in rd1
#     assert type(rd1["ingredients"]) == type(template_rd["ingredients"])
#     for i in rd1["ingredients"]:
#         assert type(i) == str
#     test_nutritional_values(rd1["nutritional_values"])

# def test_meal_plan(mp):
#     for i in mp:
#         test_recipe_data(i)

# @pytest.mark.xfail(reason="testing bad nutritional values")
# class TestBadNVs:

#     def test_good_nutritional_values(self, nv1):
#         test_nutritional_values(nv1)

#     def test_bad_calories(self, nv2):
#         nv2["calories"] = "yabba dabba doo"
#         test_nutritional_values(nv2)

#     def test_missing_something(self, nv2):
#         idx = random.choice(nv2)
#         nv2.pop(idx)
#         test_nutritional_values(nv2)

#     def test_bad_something(self, nv2):
#         idx = random.choice(nv2)
#         nv2[idx] = "yabba dabba doo"
#         test_nutritional_values(nv2)

#     def test_missing_item(self, nv2):
#         nv2.pop("vitaminA")
#         test_nutritional_values(nv2)

#     def test_good_nutritional_values_2(self, nv2):
#         assert "vitaminA" in nv2
#         test_nutritional_values(nv2)

# def test_delim1():
#     pass

# @pytest.mark.xfail(reason="testing bad recipe data")
# class TestBadRDs:

#     def test_good_recipe(self, rd1):
#         test_recipe_data(rd1)

#     def test_bad_ingredient(self, rd1):
#         rd1["ingredients"].append(True)
#         test_recipe_data(rd1)

#     def test_bad_name(self, rd1):
#         rd1["name"] = None
#         test_recipe_data(rd1)

#     def test_bad_nv(self, rd1):
#         rd["nutritional value"].pop("vitaminA")
#         test_recipe_data(rd)

#     def test_missing_something(self, rd1):
#         idx = random.choice(rd)
#         rd.pop(idx)

#     def test_empty_recipe(self):
#         rd = dict()
#         test_recipe_data(rd)

#     def test_good_recipe(rd1, self):
#         test_recipe_data(rd1)

# def test_delim2():
#     pass

# @pytest.mark.xfail(reason="testing bad meal plan")
# class TestBadMPs:

#     def test_good_meal_plan(self, mp):
#         test_meal_plan(mp)

#     def test_bad_recipe_ingredient(self, mp):
#         mp[0]["ingredients"].append(0.24)
#         test_meal_plan(mp)

#     def test_empty_mp(self):
#         mp = []
#         test_meal_plan(mp)

#     def test_good_meal_plan(self, mp):
#         test_meal_plan(mp)

# def test_delim3():
#     pass

# class TestGoodData:

#     def test_all(self, mp):
#         test_meal_plan(mp)
#         for i in mp:
#             test_recipe_data(i)
#             test_nutritional_values(i["nutritional value"])
