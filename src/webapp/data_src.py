import json


class DataStructures:

    def nutritional_values():
        return json.loads(
            '{"calcium": 0.0,"calories": 0.0,"carbohydrate": 0.0,"cholesterol": 0.0,"fat": 0.0,"fiber": 0.0,"iron": 0.0,"monounsaturated_fat": 0.0,"polyunsaturated_fat": 0.0,"potassium": 0.0,"protein": 0.0,"saturated_fat": 0.0,"sodium": 0.0,"sugar": 0.0,"trans_fat": 0.0,"vitamin_a": 0.0,"vitamin_c": 0.0}'
        )

    def recipe_data():
        skeleton = json.loads(
                '{"name":"n/a","ingredients":[],"directions":[],"nutritional_values":"","number_of_servings":0,"type":""}')
        skeleton["nutritional_values"] = DataStructures.nutritional_values()
        return skeleton

    def meal_plan(meals = 3):
        return [ DataStructures.recipe_data() for i in range(meals)]
