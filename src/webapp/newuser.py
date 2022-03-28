import itertools
import json
import os
import random
import sys

from webapp import data_src
from webapp.data_src import DataStructures


def createnewuser(email,username,password):
    # Hard coded exercises for now
    jsonnewuser={}
    jsonnewuser["email"]=email
    jsonnewuser["username"]=username
    jsonnewuser["password"]=password

    return jsonnewuser


