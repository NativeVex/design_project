from webapp.models import Recipes, db
from webapp.mealplan import add_exercise_to_db, add_recipe, get_recipes_from_db

def test_load_recipe_db(test_client, init_database_recipes):
    r1 = get_recipes_from_db()
    assert r1[0].potassium == 25

def test_add_recipe_db(test_client, init_database_recipes):
    add_recipe("iphone", ["swipe credit card", "get iphone"], ["assortment of metals", "transistors"], calories=0, carbohydrate=69, protein=420)
    iphone = Recipes.query.filter_by(name="iphone")
    assert iphone.protein == 420