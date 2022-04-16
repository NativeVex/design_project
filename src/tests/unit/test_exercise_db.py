from webapp.models import Exercise, db
from webapp.exerciseplan import add_exercise_to_db

def test_load_exercise_db(test_client, init_database_exercises):
    exercise1 = Exercise.query.filter_by(level=3).first()
    assert exercise1.name == "Tricep Dips"

def test_add_exercise_db(test_client, init_database_exercises):
    add_exercise_to_db("Sits Still", ["Brain", "Butt", "PP"], level=0, sets=69, reps=420)
    e = Exercise.query.filter_by(reps=420).first()
    assert e.name == "Sits Still"