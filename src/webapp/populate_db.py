import json
from webapp.models import Recipes, db

def populate_db(db):
    with open("r2.json") as r:
        for jsline in r:
            fixme = json.loads(jsline.strip())
            for i in fixme["nutritional_values"]:
                fixme["nutritional_values"][i] = float(
                    fixme["nutritional_values"][i])
            new_recipe = Recipes(json.dumps(fixme))
            db.session.add(new_recipe)
    db.session.commit()