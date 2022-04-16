from webapp.models import Exercise

def test_load_exercise_db(test_client, init_database_exercises):
    exercise1 = Exercise.query.filter_by(level=3).first()
    assert exercise1.name == "Tricep Dips"