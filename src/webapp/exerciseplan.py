import itertools
import json
import os
import random
import sys
import copy

from webapp import data_src
from webapp.data_src import DataStructures
from webapp.models import Exercise, db


def get_exercises_from_db():
    exercises = []
    queried_exercises = Exercise.query()
    for exercise in queried_exercises:
        skeleton = DataStructures.exercise()
        skeleton["name"] = exercise.name
        skeleton["targetmusclegroups"] = json.loads(exercise.targetmusclegroups)
        skeleton["level"] = exercise.level
        skeleton["sets"] = exercise.sets
        skeleton["reps"] = exercise.reps
    return exercises

def add_exercise_to_db(name: str, targetmusclegroups: list, level=0, sets=0, reps=0):
    db.session.add(Exercise(name, targetmusclegroups, level, sets, reps))
    db.session.commit()
    return

class ExerciseplanGenerator(data_src.DataStructures):
    user_requirements = None
    exercise_list = [] 
    def __init__(self, json_str):
        """
        Init function
        in: JSON string formatted according to DataStructures.exercise_reqs
        out: n/a
        """
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
        Check whether an exercise overlaps with the target muscle groups
        Returns True if needed_groups and exercise["targetmusclegroups"] have an overlapping member
        Returns False otherwise.
        """
        for i in needed_groups:
            if i in exercise["targetmusclegroups"]:
                return True
        return False

    def _gen_exercises_for_day(self):
        """
        Returns a list of exercises for one day that satisfy the user's requirements

        in: N/A
        out: List of exercises that satisfy user requirements

        Basic algorithm:
            Shuffle exercise list
            Find exercises that
                overlap with at least one of the user's target muscle groups and
                have a level no higher than the user's level
            Add the exercise level to a running counter
            Once the counter hits 3x the user's level the plan is returned.

            It is also programmed to try to find a plan that satisfies *all* of the user's requirements and to avoid repeats.
            Tweaks can be done to allow repeats or non-overlapping exercises if there are no more good exercises,
            or the entire generator could be rebuilt to rank each exercise and pick the top N. But I think this returns
            reasonable exercise plans given the user's requirements.
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
        """
        Returns a weekly exercise plan populated with exercises for every day that the user wants to work out.

        in: N/A
        out: Weekly exercise plan in JSON format
        """
        to_return = DataStructures.exercise_plan()
        for i in self.user_requirements["days"]:
            if self.user_requirements["days"][i]:
                to_return[i] = self._gen_exercises_for_day()
        return json.dumps(to_return)
