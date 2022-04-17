import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    """
    Class that represents a user of the application
    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using werkzeug.security)
        * registered_on - date & time that the user registered
    REMEMBER: Never store the plaintext password in a database!
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    password_hashed = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime)
    mealplan = db.Column(db.String)
    exerciseplan = db.Column(db.String)

    def __init__(self, email: str, username: str, password_plaintext: str, mealplan = "", exerciseplan = ""):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.email = email
        self.username = username
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.mealplan = mealplan
        self.exerciseplan = exerciseplan

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f"<User: {self.email}>"

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)
    
    def add_mealplan(self, mealplan):
        self.mealplan = json.dumps(mealplan)

    def get_mealplan(self):
        if self.mealplan == "":
            return []
        return json.loads(self.mealplan)

    def add_exerciseplan(self, exerciseplan):
        self.exerciseplan = json.dumps(exerciseplan)
    
    def get_exerciseplan(self):
        if self.exerciseplan == "":
            return []
        return json.loads(self.exerciseplan)

class Recipes(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    directions = db.Column(db.String)
    ingredients = db.Column(db.String)
    calcium = db.Column(db.Float)
    calories = db.Column(db.Float)
    carbohydrate = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    fat = db.Column(db.Float)
    fiber = db.Column(db.Float)
    iron = db.Column(db.Float)
    monounsaturated_fat = db.Column(db.Float)
    polyunsaturated_fat = db.Column(db.Float)
    potassium = db.Column(db.Float)
    protein = db.Column(db.Float)
    saturated_fat = db.Column(db.Float)
    sodium = db.Column(db.Float)
    sugar = db.Column(db.Float)
    trans_fat = db.Column(db.Float)
    vitamin_a = db.Column(db.Float)
    vitamin_c = db.Column(db.Float)
    number_of_servings = db.Column(db.Integer)
    type = db.Column(db.String)

    def __init__(self, json_str):
        data_dict = json.loads(json_str)
        self.name = data_dict["name"]
        self.directions = json.dumps(data_dict["directions"])
        self.ingredients = json.dumps(data_dict["ingredients"])
        self.number_of_servings = data_dict["number_of_servings"]
        self.type = json.dumps(data_dict["type"])

        self.calories = data_dict["nutritional_values"]["calories"]
        self.carbohydrate = data_dict["nutritional_values"]["carbohydrate"]
        self.protein = data_dict["nutritional_values"]["protein"]
        self.cholesterol = data_dict["nutritional_values"]["cholesterol"]
        self.fat = data_dict["nutritional_values"]["fat"]
        self.fiber = data_dict["nutritional_values"]["fiber"]
        self.iron = data_dict["nutritional_values"]["iron"]
        self.monounsaturated_fat = data_dict["nutritional_values"][
            "monounsaturated_fat"]
        self.polyunsaturated_fat = data_dict["nutritional_values"][
            "polyunsaturated_fat"]
        self.potassium = data_dict["nutritional_values"]["potassium"]
        self.calcium = data_dict["nutritional_values"]["calcium"]
        self.saturated_fat = data_dict["nutritional_values"]["saturated_fat"]
        self.sodium = data_dict["nutritional_values"]["sodium"]
        self.sugar = data_dict["nutritional_values"]["sugar"]
        self.trans_fat = data_dict["nutritional_values"]["trans_fat"]
        self.vitamin_a = data_dict["nutritional_values"]["vitamin_a"]
        self.vitamin_c = data_dict["nutritional_values"]["vitamin_c"]

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)

class Exercise(db.Model):
    __tablename__ = "exercise"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    targetmusclegroups = db.Column(db.String)
    level = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)

    def __init__(self, name="", targetmusclegroups=[], level = 0, sets = 0, reps = 0, json_str = ""):
        if json_str != "":
            data_dict = json.loads(json_str)
            self.name = data_dict["name"]
            self.targetmusclegroups = json.dumps(data_dict["targetmusclegroups"])
            self.level = data_dict["level"]
            self.sets = data_dict["sets"]
            self.reps = data_dict["reps"]
        else:
            self.name = name
            self.targetmusclegroups = json.dumps(targetmusclegroups)
            self.level = level
            self.sets = sets
            self.reps = reps

    def get_id(self):
        """Return the exercise ID as a unicode string (`str`)."""
        return str(self.id)