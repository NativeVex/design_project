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

    def __init__(self, email: str, username: str, password_plaintext: str):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.email = email
        self.username = username

        self.password_hashed = self._generate_password_hash(password_plaintext)

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


class Recipes(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
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
    type = db.Column(db.String)

    def __init__(
        self,
        name: str,
        calories: float,
        carbohydrate: float,
        protein: float,
        cholesterol=0.0,
        fat=0.0,
        fiber=0.0,
        iron=0.0,
        monounsaturated_fat=0.0,
        polyunsaturated_fat=0.0,
        potassium=0.0,
        calcium = 0.0,
        saturated_fat=0.0,
        sodium=0.0,
        sugar=0.0,
        trans_fat=0.0,
        vitamin_a=0.0,
        vitamin_c=0.0,
        type = ""
    ):
        """Create a new Mealplan object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.name = name
        self.calories = calories
        self.carbohydrate = carbohydrate
        self.protein = protein
        self.cholesterol = cholesterol
        self.fat = fat
        self.fiber = fiber
        self.iron = iron
        self.monounsaturated_fat = monounsaturated_fat
        self.polyunsaturated_fat = polyunsaturated_fat
        self.potassium = potassium
        self.calcium = calcium
        self.saturated_fat = saturated_fat
        self.sodium = sodium
        self.sugar = sugar
        self.trans_fat = trans_fat
        self.vitamin_a = vitamin_a
        self.vitamin_c = vitamin_c
        self.type = type

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)
