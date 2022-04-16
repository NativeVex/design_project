import json

from webapp.app import  app, db
#from webapp.models import Recipes
from webapp.mealplan import get_recipes_from_db


def test_getRecipes(test_client, init_database_recipes):
    """
    GIVEN a db with Adobo Chicken and Ice Cream Sandwich
    WHEN the get_recipes_from_db is called, Query the request to Json

    """
    recipes = get_recipes_from_db()
    for i in range(len(recipes)):
        recipes[i] = json.loads(recipes[i])
    assert type(recipes[0]) == type({"": str, "": [], "": {}})
    assert recipes[0]["nutritional_values"]["calories"] == 107.0
    assert recipes[1]["nutritional_values"]["calories"] == 143.0

    recipes = get_recipes_from_db(Proteins_max=5)
    for i in range(len(recipes)):
        recipes[i] = json.loads(recipes[i])
    assert recipes[0]["nutritional_values"]["sodium"] == 37.0
