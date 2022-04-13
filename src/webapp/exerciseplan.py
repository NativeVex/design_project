import itertools
import json
import os
import random
import sys
import copy

from webapp import data_src
from webapp.data_src import DataStructures


def get_exercises_from_db():
    exercises = []
    with open("homeworkouts_org_exercises.json") as file:
        for line in file:
            exercises.append(line)
    return exercises



class ExerciseplanGenerator(data_src.DataStructures):
    user_requirements = None
    exercise_list = [] 
    def __init__(self, json_str):
        self.user_requirements = json.loads(json_str)
        json_exercises = get_exercises_from_db()
        for i in json_exercises:
            self.exercise_list.append(json.loads(i))
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
        user_exercises = []
        exercise_sum = 0
        needed_groups = copy.deepcopy(self.user_requirements["targetmusclegroups"])
        exercise_list = copy.deepcopy(self.exercise_list)
        random.shuffle(exercise_list)
        while exercise_sum != (3 * self.user_requirements["level"]):
            ex_size = len(user_exercises)
            for i in exercise_list:
                if exercise_sum == 3 * self.user_requirements["level"]:
                    break
                if i["level"] > self.user_requirements["level"] or i["level"] > ((3 * self.user_requirements["level"]) - exercise_sum):
                    continue
                if needed_groups == []:
                    if self._overlap(self.user_requirements["targetmusclegroups"], i):
                        user_exercises.append(i)
                        exercise_sum += i["level"]
                        exercise_list.remove(i)
                else:
                    if self._overlap(needed_groups, i):
                        user_exercises.append(i)
                        exercise_sum += i["level"]
                        for j in i["targetmusclegroups"]:
                            if j in needed_groups:
                                needed_groups.remove(j)
                        exercise_list.remove(i)
            if ex_size == len(user_exercises): #no exercises added this entire loop
                break
        return user_exercises

    def gen_exercise_plan(self):
        to_return = DataStructures.exercise_plan()
        for i in self.user_requirements["days"]:
            if self.user_requirements["days"][i]:
                to_return[i] = self._gen_exercises_for_day()
        return to_return
