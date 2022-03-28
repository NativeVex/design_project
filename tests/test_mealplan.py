import json
import sys
from webapp import mealplan

def test_gen_meal_plan():
    #TODO: health reqs
    result_json = mealplan.gen_meal_plan("")
    assert(type(result_json) == str)
    result = json.loads(result_json)
    assert(type(result) == list)
    for i in result:
        assert(type(i) == dict)
