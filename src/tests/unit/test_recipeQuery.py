from webapp.app import app, db
from webapp.mealplan import get_recipes_from_db
from webapp.models import Recipes
import json


def test_recipeQuery(test_client, init_database_recipes):
    """
    GIVEN a db with Adobo Chicken and Ice Cream Sandwich
    WHEN the query is called
    THEN test if query success
    """
    recipes = Recipes.query.filter(Recipes.calories > 0,
                                   Recipes.calories < 1000)
    assert recipes[0].calories == 77
    assert json.loads(recipes[0].type)[0] == "Main Dish"