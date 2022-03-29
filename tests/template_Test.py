import json
import sys
from webapp import mealplan
from webapp import data_src

def test_gen_meal_plan():
    #TODO: health reqs
    sample_nutritional_values = data_src.nutritional_values()
    sample_nutritional_values["calories"] = 2000
    sample_nutritional_values["carbs"] = 120
    sample_nutritional_values["protein"] = 130
    sample_nutritional_values["fat"] = 25
    sample_nutritional_values["cholesterol"] = 10
    sample_nutritional_values["sodium"] = 120
    result_json = mealplan.gen_meal_plan(json.dumps(sample_nutritional_values))
    assert(type(result_json) == str)
    result = json.loads(result_json)
    assert(type(result) == list)
    for i in result:
        assert(type(i) == dict)
