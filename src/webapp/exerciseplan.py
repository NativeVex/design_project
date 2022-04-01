import itertools
import json
import os
import random
import sys

from webapp import data_src
from webapp.data_src import DataStructures


def get_exercises_from_db():
    exercises = []
    pull_up = DataStructures.exercise()
    pull_up["name"] = "Pull Ups"
    pull_up["targetmusclegroups"] = ["back", "shoulders", "arms", "core", "chest"]
    pull_up["level"] = 4
    pull_up["sets"] = 3
    pull_up["reps"] = 8
    exercises.append(json.dumps(pull_up))
    squats = DataStructures.exercise()
    squats["name"] = "Squats"
    squats["targetmusclegroups"] = ["thighs", "hamstrings", "glutes"]
    squats["level"] = 1
    squats["sets"] = 3
    squats["reps"] = 30
    exercises.append(json.dumps(squats))
    crunches = DataStructures.exercise()
    crunches["name"] = "Crunches"
    crunches["targetmusclegroups"] = ["core"]
    crunches["level"] = 1
    crunches["sets"] = 3
    crunches["reps"] = 30
    exercises.append(json.dumps(crunches))
    push_up["name"] = "Push Ups"
    push_up["targetmusclegroups"] = ["core", "arms", "chest", "shoulders"]
    push_up["level"] = 2
    push_up["sets"] = 3
    push_up["reps"] = 15



#class ExerciseplanGenerator(data_src.DataStructures):
