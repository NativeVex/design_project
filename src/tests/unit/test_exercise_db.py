from webapp.models import Exercise, db
from webapp.exerciseplan import add_exercise_to_db

def test_load_exercise_db(init_database_load):
    exercise1 = db.session.query(Exercise).filter_by(level=3).first()
    assert exercise1.name == "Tricep Dips"

def test_add_exercise_db(init_database_load):
    add_exercise_to_db("Sits Still", ["Brain", "Butt", "PP"], level=0, sets=69, reps=420)
    e = db.session.query(Exercise).filter_by(reps=420).first()
    assert e.name == "Sits Still"
    e2 = db.session.query(Exercise).filter_by(level=3).first()
    assert e2.name == "Tricep Dips"