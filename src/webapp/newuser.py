import itertools
import json
import os
import random
import sys

from webapp import data_src
from webapp.data_src import DataStructures


def createnewuser(email, username, password):
    return {"email": email, "username": username, "password": password}
