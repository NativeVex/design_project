import json


class DataStructures:

    def nutritional_values():
        return json.loads(
            "{'calcium': 0.0,'calories': 0.0,'carbohydrate': 0.0,'cholesterol': 0.0,'fat': 0.0,'fiber': 0.0,'iron': 0.0,'monounsaturated_fat': 0.0,'polyunsaturated_fat': 0.0,'potassium': 0.0,'protein': 0.0,'saturated_fat': 0.0,'sodium': 0.0,'sugar': 0.0,'trans_fat': 0.0,'vitamin_a': 0.0,'vitamin_c': 0.0, 'type':""}"
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
