import base64
import itertools
import json
import random
import sys

import pytest

from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator

from .DB_fixtures import *
from .Mealplan_fixtures import *

# Functions to test that a given datastructure is valid
# Written to be used in other test code
random.seed(0)
