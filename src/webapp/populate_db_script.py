import json
from webapp.models import Recipes, db
from flask import Flask
from webapp.populate_db import populate_db
app = Flask(__name__)
flask_app = app
with flask_app.test_client() as testing_client:
    with flask_app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
        db.init_app(app)
        db.create_all(app=app)
        populate_db(db)