import json

from webapp.models import Exercise, db


def populate_db(db):
    exercises = []
    with open("homeworkouts_org_exercises.json") as file:
        for line in file:
            new_exercise = Exercise(line)
            db.session.add(new_exercise)
    db.session.commit()
    return exercises
