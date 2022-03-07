import json
import sys
import random
import base64
import pytest
import itertools
from webapp import mealplan
from webapp import data_src
import test_data




#define what the variables are for this use case
@pytest.fixture
def health_reqs():
    return test_data.sample_health_reqs()

@pytest.fixture
def meal_plan_a():
    return test_data.sample_meal_plan()

@pytest.fixture
def meal_plan_b():
    return test_data.sample_meal_plan()

@pytest.fixture
def recipe_list():
    ls = []
    for i in range(12):
        ls.append(test_data.sample_recipe())
    return ls

@pytest.fixture
def json_recipe_list(recipe_list):
    ls = []
    for i in recipe_list:
        ls.append(json.dumps(i))
    return ls



#test functions

#we can run this test several times, each time with different inputs, using this.
@pytest.mark.parametrize("n1,n2",
        [
            (test_data.sample_nutritional_values(), test_data.sample_nutritional_values()),
            (test_data.sample_nutritional_values(), test_data.sample_nutritional_values()),
            (test_data.sample_nutritional_values(), test_data.sample_nutritional_values())
            ])
def test_sum_nutritional_values(n1, n2):
#   n1 = sample_nutritional_values()
#   n2 = sample_nutritional_values()
    result = mealplan.sum_nutritional_values(n1, n2)
    for i in result:
        assert(result[i] == n1[i] + n2[i])
    
    return

#we can mark a test as expected to fail like this:
@pytest.mark.xfail(reason="Showcasing pytest functionality")
def test_should_fail():
    n1 = test_data.sample_nutritional_values()
    n1["calories"] = "yabba dabba doo"
    n2 = test_data.sample_nutritional_values()
    result = mealplan.sum_nutritional_values(n1, n2)
    for i in result:
        assert(result[i] == n1[i] + n2[i])

@pytest.mark.xfail(reason="Showcasing pytest functionality")
def test_should_pass():
    n1 = test_data.sample_nutritional_values()
    n2 = test_data.sample_nutritional_values()
    result = mealplan.sum_nutritional_values(n1, n2)
    for i in result:
        assert(result[i] == n1[i] + n2[i])

#we can expect a specific type of error like this:
def test_zero():
    with pytest.raises(ZeroDivisionError):
        result = 1/0
        return result

def test_diff_nutritional_values():
    n1 = test_data.sample_nutritional_values()
    n2 = test_data.sample_nutritional_values()
    result = mealplan.diff_nutritional_values(n1, n2)
    for i in result:
        assert(result[i] == n1[i] - n2[i])
    
    return
def test_calculate_meal_plan_nutrition():
    meal_plan = test_data.sample_meal_plan()
    print(meal_plan)
    nutrition = mealplan.calculate_meal_plan_nutrition(meal_plan)
    for i in nutrition:
        assert(nutrition[i] == meal_plan[0]["nutritional value"][i] + meal_plan[1]["nutritional value"][i] + meal_plan[2]["nutritional value"][i])
    return
def test_meal_plan_RSS():
    healthreqs = test_data.sample_nutritional_values()
    meal_plan = test_data.sample_meal_plan()
    rss = mealplan.meal_plan_RSS(healthreqs, meal_plan)
    real_rss = 0
    for i in meal_plan:
        for j in healthreqs:
            real_rss += (healthreqs[j] - i["nutritional value"][j])**2
    assert(real_rss == rss)
    return

#Module integration test: makes sure this module works as expected
def test_full_module_integration(health_reqs, recipe_list, json_recipe_list):
    #make sure fixtures work as expected
    for i in range(len(recipe_list)):
        assert(recipe_list[i] == json.loads(json_recipe_list[i]))
    program_output = mealplan.gen_meal_plan(json.dumps(health_reqs), json_recipe_list)

    #make sure this is really the best
    best_meal_plan = json.loads(program_output)
    best_meal_plan_rss = mealplan.meal_plan_RSS(health_reqs, best_meal_plan)
    meals_per_meal_plan = 3
    possible_meal_plans_iterator = itertools.combinations(recipe_list, meals_per_meal_plan)
    for i in possible_meal_plans_iterator:
        #this will fail if there is a better meal plan found
        assert(mealplan.meal_plan_RSS(health_reqs, i) >= best_meal_plan_rss)
