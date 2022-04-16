import base64
import itertools
import json
import random
import sys

import pytest

from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator
from webapp.exerciseplan import ExerciseplanGenerator

@pytest.mark.parametrize(
        "exercise",
           [(pytest.lazy_fixture('e1')),
            (pytest.lazy_fixture('e2')),
            (pytest.lazy_fixture('e3')
            )])
def test_overlap(exercise, er1, epg_class):
    overlap_given_val = egp_class._overlap(er1["targetmusclegroups"], exercise)
    is_overlap = False
    for i in er1["targetmusclegroups"]:
        if i in exercise["targetmusclegroups"]:
            assert overlap_given_val == True
            is_overlap = True
    assert overlap_given_val == is_overlap

def test_gen_exercises_for_day(epg_class):
    genned_exercises = epg_class._gen_exercises_for_day()
    level_sum = 0
    overlapped = False
    for i in genned_exercises:
        level_sum += i["level"]
        test_exercise(i)
    assert level_sum <= 3 * epg_class.user_requirements["level"]

def test_gen_exercises(epg_class):
    genned_ep = epg_class.gen_exercise_plan()
    for i in genned_ep:
        for j in genned_ep[i]:
            test_exercise(j)
