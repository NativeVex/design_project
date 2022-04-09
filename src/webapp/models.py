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
    Calories = db.Column(db.Float)
    Carbs = db.Column(db.Float)
    Proteins = db.Column(db.Float)
    fat = db.Column(db.Float)
    Cholesterol = db.Column(db.Float)
    Sodium = db.Column(db.Float)
    Vitamina = db.Column(db.Float)
    Calcium = db.Column(db.Float)
    Copper = db.Column(db.Float)
    Fluoride = db.Column(db.Float)
    Iodine = db.Column(db.Float)
    Iron = db.Column(db.Float)
    Magnesium = db.Column(db.Float)
    Manganese = db.Column(db.Float)
    Molybdenum = db.Column(db.Float)
    Phosphorus = db.Column(db.Float)
    Potassium = db.Column(db.Float)
    Selenium = db.Column(db.Float)
    Zinc = db.Column(db.Float)
    Vitaminc = db.Column(db.Float)

    def __init__(
        self,
        name: str,
        Calories: float,
        Carbs: float,
        Proteins: float,
        fat=0.0,
        Cholesterol=0.0,
        Sodium=0.0,
        Vitamina=0.0,
        Calcium=0.0,
        Copper=0.0,
        Fluoride=0.0,
        Iodine=0.0,
        Iron=0.0,
        Magnesium=0.0,
        Manganese=0.0,
        Molybdenum=0.0,
        Phosphorus=0.0,
        Potassium=0.0,
        Selenium=0.0,
        Zinc=0.0,
        Vitaminc=0.0,
    ):
        """Create a new Mealplan object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.name = name
        self.Calories = Calories
        self.Carbs = Carbs
        self.fat = fat
        self.Proteins = Proteins
        self.Cholesterol = Cholesterol
        self.Sodium = Sodium
        self.Vitamina = Vitamina
        self.Calcium = Calcium
        self.Copper = Copper
        self.Fluoride = Fluoride
        self.Iodine = Iodine
        self.Iron = Iron
        self.Magnesium = Magnesium
        self.Manganese = Manganese
        self.Molybdenum = Molybdenum
        self.Phosphorus = Phosphorus
        self.Potassium = Potassium
        self.Selenium = Selenium
        self.Zinc = Zinc
        self.Vitaminc = Vitaminc

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)
