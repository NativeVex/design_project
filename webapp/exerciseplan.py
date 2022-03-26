import itertools
import json
import os
import random
import sys

from webapp import data_src
from webapp.data_src import DataStructures


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
