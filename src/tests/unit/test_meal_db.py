import json

from webapp.mealplan import add_recipe, get_recipes_from_db
from webapp.models import Recipes, db


def test_load_recipe_db(init_database_load):
    recipes = get_recipes_from_db()
    for i in range(len(recipes)):
        recipes[i] = json.loads(recipes[i])
    assert type(recipes[0]) == type({"": str, "": [], "": {}})
    assert recipes[0]["nutritional_values"]["calories"] == 77
    assert recipes[1]["nutritional_values"]["calories"] == 214

    recipes = get_recipes_from_db()
    for i in range(len(recipes)):
        recipes[i] = json.loads(recipes[i])
    assert recipes[0]["nutritional_values"]["fat"] == 1.69
