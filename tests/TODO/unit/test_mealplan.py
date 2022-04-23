import base64
import fractions
import itertools
import json
import random
import sys

import pytest
import test_data

from webapp.app import app, db
from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator


# test functions
def test_sum_nutritional_values(nv1, nv2, mpg_class):
    """Tests _sum_nutritional_values utility function"""

    result = mpg_class._sum_nutritional_values(nv1, nv2)
    for i in result:
        assert result[i] == nv1[i] + nv2[i]


# we can mark a test as expected to fail like this:
@pytest.mark.xfail(reason="Showcasing pytest functionality", strict=True)
def test_sum_nutritional_values_fail(nv1, nv2, mpg_class):
    """Tests _sum_nutritional_values with string for one value; should fail"""
    nv1["calories"] = "yabba dabba doo"
    result = mpg_class._sum_nutritional_values(nv1, nv2)
    for i in result:
        assert result[i] == nv1[i] + nv2[i]


# we can expect a specific type of error like this:
def test_diff_nutritional_values(nv1, nv2, mpg_class):
    """Tests _diff_nutritional_values utility function"""
    result = mpg_class._diff_nutritional_values(nv1, nv2)
    for i in result:
        assert result[i] == nv1[i] - nv2[i]


def test_calculate_meal_plan_nutrition(mp, mpg_class):
    """Tests _calculate_meal_plan_nutrition utility function"""
    nutrition = mpg_class._calculate_meal_plan_nutrition(mp)

    for i in nutrition:
        assert (
            nutrition[i]
            == mp[0]["nutritional_values"][i]
            + mp[1]["nutritional_values"][i]
            + mp[2]["nutritional_values"][i]
        )


def test_nutritional_values_RSS(sample_health_reqs, nv1, mpg_class):
    rss = mpg_class._nutritional_values_RSS(sample_health_reqs, nv1)
    real_rss = 0
    for i in nv1:
        real_rss += (sample_health_reqs[i] - nv1[i]) ** 2
    real_rss /= len(nv1)
    assert rss == real_rss


def test_recipe_data_RSS(sample_health_reqs, rd1, mpg_class):
    rss = mpg_class._recipe_RSS(sample_health_reqs, rd1)
    real_rss = 0
    for i in sample_health_reqs:
        real_rss += (sample_health_reqs[i] - rd1["nutritional_values"][i]) ** 2
    real_rss /= len(sample_health_reqs)
    assert rss == real_rss


def test_meal_plan_RSS(sample_health_reqs, mp, mpg_class):
    """Tests _meal_plan_RSS function that gets the RSS of a mealplan"""
    rss = mpg_class._meal_plan_RSS(sample_health_reqs, mp)
    real_rss = 0
    for i in mp:
        for j in i["nutritional_values"]:
            real_rss += (i["nutritional_values"][j] -
                         sample_health_reqs[j]) ** 2
        real_rss /= len(i["nutritional_values"])
    real_rss /= len(mp)
    assert real_rss == rss


@pytest.mark.parametrize(
    "calorie_split,protein_split,carbs_split",
    [
        ([0.25, 0.25, 0.5], [0.25, 0.25, 0.5], [0.25, 0.25, 0.5]),
        ([0.1, 0.1, 0.9], [0.1, 0.9, 0.1], [0.9, 0.1, 0.1]),
        ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
        ([30.0, 30.0, 30.0], [29.9, 29.9, 29.9], [28.8, 28.8, 28.8]),
        ([1.1, 2.2, 3.3], [4.4, 5.5, 6.6], [7.7, 8.8, 9.9]),
    ],
)
def test_balance_health_requirements(
    calorie_split, protein_split, carbs_split, nv1, mpg_class
):
    health_requirements = nv1
    hr_breakfast, hr_lunch, hr_dinner = mpg_class._balance_health_requirements(
        calorie_split, protein_split, carbs_split, health_requirements
    )
    assert (
        hr_breakfast["calories"] == health_requirements["calories"] *
        calorie_split[0]
    )
    assert hr_breakfast["protein"] == health_requirements["protein"] * \
        protein_split[0]
    assert (
        hr_breakfast["carbohydrate"]
        == health_requirements["carbohydrate"] * carbs_split[0]
    )
    assert hr_lunch["calories"] == health_requirements["calories"] * \
        calorie_split[1]
    assert hr_lunch["protein"] == health_requirements["protein"] * \
        protein_split[1]
    assert (
        hr_lunch["carbohydrate"] == health_requirements["carbohydrate"] *
        carbs_split[1]
    )
    assert hr_dinner["calories"] == health_requirements["calories"] * \
        calorie_split[2]
    assert hr_dinner["protein"] == health_requirements["protein"] * \
        protein_split[2]
    assert (
        hr_dinner["carbohydrate"]
        == health_requirements["carbohydrate"] * carbs_split[2]
    )
    return


@pytest.mark.parametrize(
    "scale,scalable_num,sussy_ing",
    [
        (0, 1, "1/3 orange"),
        (1, 12.2, "2/4"),
        (1.44, 33, "a 1/3lb bag of flour"),
        (3 / 2, 2.2222, "3tsp Apple Cider"),
        (0.3, 0, "a metric ton of ice cream"),
    ],
)
def test_scale_recipe(scale, scalable_num, sussy_ing, rd1, mpg_class):
    rd1["ingredients"] = [
        "1/4 leg of lamb",
        "3 tsp tumeric",
        "4 lbs of peas",
        "Pound of salt",
        str(scalable_num) + " bubble teas",
        sussy_ing,
    ]
    old_servings = rd1["number_of_servings"]

    # _scale_recipe runs in place
    a = mpg_class._scale_recipe(rd1, scale)
    assert a == None
    assert rd1["number_of_servings"] == old_servings * scale

    # six asserstions, one for each ingredient
    assert fractions.Fraction(
        rd1["ingredients"][0].split(" ")[0]
    ) == fractions.Fraction(str(1 / 4 * scale))
    assert fractions.Fraction(
        rd1["ingredients"][1].split(" ")[0]
    ) == fractions.Fraction(str(3 * scale))
    assert fractions.Fraction(
        rd1["ingredients"][2].split(" ")[0]
    ) == fractions.Fraction(str(4 * scale))
    assert rd1["ingredients"][3].split(" ")[0] == "Pound"
    assert fractions.Fraction(
        rd1["ingredients"][4].split(" ")[0]
    ) == fractions.Fraction(str(scalable_num * scale))
    if sussy_ing.split(" ")[0].replace(".", "").replace("/", "").isdigit():
        assert (
            fractions.Fraction(rd1["ingredients"][5].split(" ")[0])
            == fractions.Fraction(sussy_ing.split(" ")[0]) * scale
        )
    else:
        assert rd1["ingredients"][5] == sussy_ing
    return


def test_module_integration(sample_health_reqs, mpg_class):
    """Tests full functionality of mealplan generator module"""
    out = json.loads(mpg_class.gen_meal_plan())
    test_data.test_meal_plan(out)


# Module integration test: makes sure this module works as expected
#   def test_full_module_integration(health_reqs, recipe_list, json_recipe_list):
#       #make sure fixtures work as expected
#       for i in range(len(recipe_list)):
#           assert(recipe_list[i] == json.loads(json_recipe_list[i]))
#       program_output = mealplan.gen_meal_plan(json.dumps(health_reqs), json_recipe_list)

#       #make sure this is really the best
#       best_meal_plan = json.loads(program_output)
#       best_meal_plan_rss = mealplan.meal_plan_RSS(health_reqs, best_meal_plan)
#       meals_per_meal_plan = 3
#       possible_meal_plans_iterator = itertools.combinations(recipe_list, meals_per_meal_plan)
#       for i in possible_meal_plans_iterator:
#           #this will fail if there is a better meal plan found
#           assert(mealplan.meal_plan_RSS(health_reqs, i) >= best_meal_plan_rss)


# IGNORE ME
def test_zero():
    with pytest.raises(ZeroDivisionError):
        result = 1 / 0
        return result
