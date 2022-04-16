from webapp.models import Recipes, db
from webapp.mealplan import add_recipe, get_recipes_from_db
import json

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

def test_add_recipe_db(init_database_load):
    add_recipe(name="iphone", directions=["swipe credit card", "get iphone"], ingredients=["assortment of metals", "transistors"], calories=0, carbohydrate=69, protein=420)
    add_recipe(name="iphoneX", directions=["swipe more credit card", "get iphone"], ingredients=["assortment of metals", "transistors"], calories=10, carbohydrate=6969, protein=42069)
    iphone = db.session.query(Recipes).filter_by(name="iphone").first()
    assert iphone.protein == 420
