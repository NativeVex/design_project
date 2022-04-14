from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator, get_mealplan, save_mealplan
from webapp.models import User, db
import json

def test_save_mealplan(new_user, test_client, init_database_recipes):
    db.session.add(new_user)
    db.session.commit()

    jsoninfo=DataStructures.nutritional_values()
    jsoninfo["calories"]=float(200)
    jsoninfo["carbohydrate"]=float(69)
    jsoninfo["protein"]=float(420)
    json_splits = '{"calorie_split": [0.25, 0.25, 0.5], "protein_split": [0.25, 0.25, 0.5], "carbs_split": [0.25, 0.25, 0.5]}'

    mpg = MealplanGenerator(json_health_requirements=json.dumps(jsoninfo), json_splits=json_splits)
    mealplan = mpg.gen_meal_plan()

    assert mealplan != ""

    save_mealplan(new_user.email, mealplan)
    queried_user = User.query.filter_by(email=new_user.email).first()
    
    retrieved_mealplan = get_mealplan(new_user.email)
    print(retrieved_mealplan)
    assert retrieved_mealplan == mealplan