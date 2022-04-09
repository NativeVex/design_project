from webapp.app import Recipes, app, db
from webapp.mealplan import get_recipes_from_db


def test_recipeQuery(test_client, init_database_recipes):
    """
    GIVEN a db with Adobo Chicken and Ice Cream Sandwich
    WHEN the query is called
    THEN test if query success
    """
    recipes = Recipes.query.filter(Recipes.Calories > 0,
                                   Recipes.Calories < 1000)
    assert recipes[1].Calories == 143.0
