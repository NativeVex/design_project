from webapp.exerciseplan import add_exercise_to_db
from webapp.models import Exercise, db


def test_load_exercise_db(init_database_load):
    exercise1 = db.session.query(Exercise).filter_by(level=3).first()
    assert exercise1.name == "Tricep Dips"
