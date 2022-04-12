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
<<<<<<< HEAD
=======
    push_up = DataStructures.exercise()
>>>>>>> exerciseplan
    push_up["name"] = "Push Ups"
    push_up["targetmusclegroups"] = ["core", "arms", "chest", "shoulders"]
    push_up["level"] = 2
    push_up["sets"] = 3
    push_up["reps"] = 15
<<<<<<< HEAD



#class ExerciseplanGenerator(data_src.DataStructures):
=======
    exercises.append(json.dumps(push_up))
    return exercises



class ExerciseplanGenerator(data_src.DataStructures):
    user_requirements = None
    exercise_list = None
    def __init__(self, json_str):
        self.user_requirements = json.loads(json_str)
        self.exercise_list = get_exercises_from_db()
        return

    #For each day that the user wants to work out, give them exercises S.T.
    #every day they do exercises summing to ~3x their level
    #every day they do at least one exercise that targets every muscle group specified
    def _overlap(self, needed_groups, exercise):
        """
        Check whether an exercise overlaps with the user's target muscle groups
        """
        for i in needed_groups:
            if i in exercise["targetmusclegroups"]:
                return True
        return False

    def _gen_exercises_for_day(self):
        """
        Returns a list of exercises for one day that satisfy the user's requirements
        """
        exercises = []
        exercise_sum = 0
        needed_groups = self.user_requirements["targetmusclegroups"] #copy.deepcopy?
        random.shuffle(self.exercise_list) #does this work as intended?
        for i in self.exercise_list:
            if i["level"] > self.user_requirements["level"] or i["level"] > ((3 * self.user_requirements["level"]) - exercise_sum):
                continue
            if needed_groups == []:
                if self._overlap(self.user_requirements["targetmusclegroups"]):
                    exercises.append(i)
                    exercise_sum += i["level"]
            else:
                if self._overlap(needed_groups, i):
                    exercises.append(i)
                    exercise_sum += i["level"]
                    for j in i["targetmusclegroups"]:
                        if j in needed_groups:
                            needed_groups.remove(j)
        return exercises

    def gen_exercise_plan(self):
        to_return = DataStructures.exercise_plan()
        for i in self.user_requirements["days"]:
            if self.user_requirements["days"][i]:
                to_return[i] = self._gen_exercises_for_day()
        return to_return
>>>>>>> exerciseplan
