import json


class DataStructures:
    def nutritional_values():
        return json.loads(
            '{"calcium": 0.0,"calories": 0.0,"carbohydrate": 0.0,"cholesterol": 0.0,"fat": 0.0,"fiber": 0.0,"iron": 0.0,"monounsaturated_fat": 0.0,"polyunsaturated_fat": 0.0,"potassium": 0.0,"protein": 0.0,"saturated_fat": 0.0,"sodium": 0.0,"sugar": 0.0,"trans_fat": 0.0,"vitamin_a": 0.0,"vitamin_c": 0.0}'
        )

    def default_nutritional_values():
        return json.loads(
            '{"calcium": 1300.0, "calories": 2000.0, "carbohydrate": 275.0, "cholesterol": 300.0, "fat": 78.0, "fiber": 28.0, "iron": 18.0, "monounsaturated_fat": 29.0, "polyunsaturated_fat": 29.0, "potassium": 4700.0, "protein": 50.0, "saturated_fat": 20.0, "sodium": 2300.0, "sugar": 0.0, "trans_fat": 0.0, "vitamin_a": 900.0, "vitamin_c": 90.0}'
        )

    def recipe_data():
        skeleton = json.loads(
            '{"name":"n/a","ingredients":[],"directions":[],"nutritional_values":"","number_of_servings":0,"type":[]}'
        )
        skeleton["nutritional_values"] = DataStructures.nutritional_values()
        return skeleton

    def meal_plan(meals=3):
        return [DataStructures.recipe_data() for i in range(meals)]

    def meal_plan_split():
        return json.loads(
            '{"calorie_split": [0.25, 0.25, 0.5], "protein_split": [0.25, 0.25, 0.5], "carbs_split": [0.25, 0.25, 0.5]}'
        )
