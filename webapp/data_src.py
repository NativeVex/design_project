import json


class DataStructures:

    def nutritional_values():
        return json.loads(
            '{"calories":0,"carbs":0,"protein":0,"fat":0,"cholesterol":0,"sodium":0,"vitaminA":0,"vitaminB1":0,"vitaminB2":0,"vitaminB3":0,"vitaminB5":0,"vitaminB6":0,"vitaminB9":0,"vitaminB12":0,"vitaminC":0,"vitaminD":0,"vitaminE":0,"vitaminK":0,"calcium":0,"copper":0,"fluoride":0,"iodine":0,"iron":0,"magnesium":0,"manganese":0,"molybdenum":0,"phosphorus":0,"potassium":0,"selenium":0,"zinc":0}'
        )

    def recipe_data():
        skeleton = json.loads(
            '{"name":"n/a","ingredients":[],"nutritional value":""}')
        skeleton["nutritional value"] = DataStructures.nutritional_values()
        return skeleton

    def meal_plan():
        return [
            DataStructures.recipe_data(),
            DataStructures.recipe_data(),
            DataStructures.recipe_data(),
        ]