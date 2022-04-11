import json


class DataStructures:

    def nutritional_values():
        return json.loads(
            '{"calories":0.0,"carbs":0.0,"protein":0.0,"fat":0.0,"cholesterol":0.0,"sodium":0.0,"vitaminA":0.0,"vitaminB1":0.0,"vitaminB2":0.0,"vitaminB3":0.0,"vitaminB5":0.0,"vitaminB6":0.0,"vitaminB9":0.0,"vitaminB12":0.0,"vitaminC":0.0,"vitaminD":0.0,"vitaminE":0.0,"vitaminK":0.0,"calcium":0.0,"copper":0.0,"fluoride":0.0,"iodine":0.0,"iron":0.0,"magnesium":0.0,"manganese":0.0,"molybdenum":0.0,"phosphorus":0.0,"potassium":0.0,"selenium":0.0,"zinc":0.0}'
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
    def exercise():
        return json.loads('{"name":"N/A","targetmusclegroups":[],"level":0,"sets":0,"reps":0}')

    def exercise_plan():
        skeleton = json.loads(
                '{"Sunday":[],"Monday":[],"Tuesday":[],"Wednesday":[],"Thursday":[],"Friday":[],"Saturday":[]}'
                )
        return skeleton
        
    def get_exercises_from_db():
    # Hard coded exercises for now
        jsonstring = {
        "Sunday": [
            {
                "Name": "Exercise 1",
                "sets": 5,
                "reps": 10,
                "targetmusclegroup": "legs"
            },
            {
                "Name": "Exercise 2",
                "sets": 12,
                "reps": 16,
                "targetmusclegroup": "thighs",
            },
            {
                "Name": "Exercise 3",
                "sets": 26,
                "reps": 32,
                "targetmusclegroup": "quad"
            },
        ],
        "Monday": [
            {
                "Name": "Exercise 1",
                "sets": 5,
                "reps": 10,
                "targetmusclegroup": "legs"
            },
            {
                "Name": "Exercise 2",
                "sets": 12,
                "reps": 16,
                "targetmusclegroup": "thighs",
            },
            {
                "Name": "Exercise 3",
                "sets": 26,
                "reps": 32,
                "targetmusclegroup": "quad"
            },
        ],
        "Tuesday": [
            {
                "Name": "Exercise 1",
                "sets": 5,
                "reps": 10,
                "targetmusclegroup": "legs"
            },
            {
                "Name": "Exercise 2",
                "sets": 12,
                "reps": 16,
                "targetmusclegroup": "thighs",
            },
            {
                "Name": "Exercise 3",
                "sets": 26,
                "reps": 32,
                "targetmusclegroup": "quad"
            },
        ],
        "Wednesday": [
            {
                "Name": "Exercise 1",
                "sets": 5,
                "reps": 10,
                "targetmusclegroup": "legs"
            },
            {
                "Name": "Exercise 2",
                "sets": 12,
                "reps": 16,
                "targetmusclegroup": "thighs",
            },
            {
                "Name": "Exercise 3",
                "sets": 26,
                "reps": 32,
                "targetmusclegroup": "quad"
            },
        ],
        "Thursday": [
            {
                "Name": "Exercise 1",
                "sets": 5,
                "reps": 10,
                "targetmusclegroup": "legs"
            },
            {
                "Name": "Exercise 2",
                "sets": 12,
                "reps": 16,
                "targetmusclegroup": "thighs",
            },
            {
                "Name": "Exercise 3",
                "sets": 26,
                "reps": 32,
                "targetmusclegroup": "quad"
            },
        ],
        "Friday": [
            {
                "Name": "Exercise 1",
                "sets": 5,
                "reps": 10,
                "targetmusclegroup": "legs"
            },
            {
                "Name": "Exercise 2",
                "sets": 12,
                "reps": 16,
                "targetmusclegroup": "thighs",
            },
            {
                "Name": "Exercise 3",
                "sets": 26,
                "reps": 32,
                "targetmusclegroup": "quad"
            },
        ],
        "Saturday": [
            {
                "Name": "Exercise 1",
                "sets": 5,
                "reps": 10,
                "targetmusclegroup": "legs"
            },
            {
                "Name": "Exercise 2",
                "sets": 12,
                "reps": 16,
                "targetmusclegroup": "thighs",
            },
            {
                "Name": "Exercise 3",
                "sets": 26,
                "reps": 32,
                "targetmusclegroup": "quad"
            },
        ],
    }
        jsonstringnew = json.dumps(jsonstring)
        return jsonstringnew
