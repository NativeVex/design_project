import json
from cmath import log
from random import randint
from time import strftime

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import DecimalField, Form, StringField, SubmitField, validators

from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator
from webapp.models import Recipes, User, db

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(__name__)
app.config["SECRET_KEY"] = "5e4c0f48eef083bde520ef8027eb12e3f8bafcc763969d58"

# change this URI to postgres in production!!!!
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db.init_app(app)
db.create_all(app=app)


class signupform(Form):
    email = StringField("Email:", validators=[validators.DataRequired()])
    username = StringField("Username:", validators=[validators.DataRequired()])
    password = StringField("Password:", validators=[validators.DataRequired()])


class loginform(Form):
    email = StringField("Email:", validators=[validators.DataRequired()])
    password = StringField("Password:", validators=[validators.DataRequired()])


class dietform(Form):
    Calories = DecimalField("Calories:",
                            validators=[validators.InputRequired()])
    Carbs = DecimalField("Carbs:", validators=[validators.InputRequired()])
    Proteins = DecimalField("Proteins:",
                            validators=[validators.InputRequired()])
    fat = DecimalField("Fat:", [validators.Optional()])
    Cholesterol = DecimalField("Cholesterol:", [validators.Optional()])
    Sodium = DecimalField("Sodium:", [validators.Optional()])
    Vitamina = DecimalField("Vitamina:", [validators.Optional()])
    Calcium = DecimalField("Calcium:", [validators.Optional()])
    Copper = DecimalField("Copper:", [validators.Optional()])
    Fluoride = DecimalField("Fluoride:", [validators.Optional()])
    Iodine = DecimalField("Iodine:", [validators.Optional()])
    Iron = DecimalField("Iron:", [validators.Optional()])
    Magnesium = DecimalField("Magnesium:", [validators.Optional()])
    Manganese = DecimalField("Manganese:", [validators.Optional()])
    Molybdenum = DecimalField("Molybdenum:", [validators.Optional()])
    Phosphorus = DecimalField("Phosphorus:", [validators.Optional()])
    Potassium = DecimalField("Potassium:", [validators.Optional()])
    Selenium = DecimalField("Selenium:", [validators.Optional()])
    Zinc = DecimalField("Zinc:", [validators.Optional()])


@app.route("/", methods=["GET", "POST"])
def login():
    """This function uses a post request to take
    in a username and password entered by the user to login
    and then redirects to the page where users enter their health requirements

    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if user and check_password_hash(user.password_hashed, password):
            message = "Welcome to your diet planner!"
            # if the user exists go to mealplanner page
            return redirect(url_for("diet"))
            """ 
            
            return redirect(url_for('diet'),message=message))
            """
        else:
            message = "Please check your login details and try again."
            return render_template("login.html", message=message)
    """
    message=request.args['message']
    return render_template("login.html",message=message)

    """
    return render_template("login.html")


@app.route("/logout")
def logout():
    """This function logs the user out by removing
    the session username and redirecting to the home login page

    """

    session.pop("username", None)  # removes session username
    return redirect("/")


@app.route("/points/")
def points():
    """This function shows a calendar of the points earned by
    users

    """
    return render_template("points.html")


@app.route("/saveduserinfo/")
def saveduserinfo():
    """This function goes to the saveduserinfo page where
    the user sees their saved meal plan and their saved
    exercise plan

    """
    return render_template("saveduserinfo.html")


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    """This function goes to the signup page where
    the user sees a form where they can sign up using their email,
    username, and password

    """
    usersignupform = signupform(request.form)
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()
        if (
                user
        ):  # if a user is found, we want to redirect back to signup page so user can try again
            message = "Email address already exists"
            return render_template("signup.html", message=message)
        else:
            # create a new user with the form data.
            new_user = User(email=email,
                            username=username,
                            password_plaintext=password)

            db.session.add(new_user)
            db.session.commit()

            message = "Thank you for signing up!"
            return redirect(url_for("login"))
            """
              return redirect(url_for('login', message = message))

            """
    return render_template("signup.html", form=usersignupform)


@app.route("/diet/", methods=["GET", "POST"])
def diet():
    """This function goes to the mealplanner page where
    the user sees a form where they can enter their diet requirements

    """
    """
    message=request.args['message']
    return render_template("mealplanner.html", message=message)

    
    
    """
    form = dietform(request.form)
    return render_template("mealplanner.html", form=form)


@app.route("/mealplan", methods=["GET", "POST"])
def mealplan():
    """This function goes to the mealplans page where
    the user their generated meal plan from their entered
    diet requirements
    """
    form = dietform(request.form)

    if request.method == "POST":
        Calories = form.Calories.data
        Carbs = form.Carbs.data
        protein = form.Proteins.data
        list1 = [1, 2, 3]

        jsoninfo = DataStructures.nutritional_values()
        jsoninfo["calories"] = float(Calories)
        jsoninfo["carbs"] = float(Carbs)
        jsoninfo["protein"] = float(protein)
        if form.fat.data != None:
            jsoninfo["fat"] = float(form.fat.data)
        if form.Cholesterol.data != None:
            jsoninfo["cholesterol"] = float(form.Cholesterol.data)
        if form.Sodium.data != None:
            jsoninfo["sodium"] = float(form.Sodium.data)
        if form.Vitamina.data != None:
            jsoninfo["vitaminA"] = float(form.Vitamina.data)
        if form.Calcium.data != None:
            jsoninfo["calcium"] = float(form.Calcium.data)
        if form.Copper.data != None:
            jsoninfo["copper"] = float(form.Copper.data)
        if form.Fluoride.data != None:
            jsoninfo["fluoride"] = float(form.Fluoride.data)
        if form.Iodine.data != None:
            jsoninfo["iodine"] = float(form.Iodine.data)
        if form.Iron.data != None:
            jsoninfo["iron"] = float(form.Iron.data)
        if form.Magnesium.data != None:
            jsoninfo["magnesium"] = float(form.Magnesium.data)
        if form.Manganese.data != None:
            jsoninfo["manganese"] = float(form.Manganese.data)
        if form.Molybdenum.data != None:
            jsoninfo["molybdenum"] = float(form.Molybdenum.data)
        if form.Phosphorus.data != None:
            jsoninfo["phosphorus"] = float(form.Phosphorus.data)
        if form.Potassium.data != None:
            jsoninfo["potassium"] = float(form.Potassium.data)
        if form.Selenium.data != None:
            jsoninfo["selenium"] = float(form.Selenium.data)
        if form.Zinc.data != None:
            jsoninfo["zinc"] = float(form.Zinc.data)

        jsonstring = json.dumps(jsoninfo)
        mpg = MealplanGenerator(jsonstring)
        mealplan = mpg.gen_meal_plan()
        jsondata = json.loads(mealplan)
        session["tempmealplan"] = jsondata
        return render_template("mealplans.html", bestmealplan=jsondata)
    elif request.method == "GET":
        return render_template("mealplans.html")


@app.route("/savemealplan", methods=["POST"])
def savemealplan():
    """This function goes to the saveduserinfo page where
    the user can see their saved meal plan

    """

    if request.method == "POST":
        bestmealplan = request.form["bestmealplan"]
        mealplan = bestmealplan.replace(
            "'", '"'
        )  # replacing single quotes with double quotes to change string to json format
        newmealplan = json.loads(mealplan)
        return render_template("saveduserinfo.html", bestmealplan=newmealplan)


@app.route("/saveexerciseplan", methods=["POST"])
def saveexerciseplan():
    """This function takes the generated best meal plan and saves it to
    the userinfo page where they can see their saved meal plan.

    """

    if request.method == "POST":
        bestexerciseplan = request.form["bestexerciseplan"]
        exerciseplan = bestexerciseplan.replace(
            "'", '"'
        )  # replacing single quotes with double quotes to change string to json format
        newexerciseplan = json.loads(exerciseplan)
        return render_template("saveduserinfo.html",
                               bestexerciseplan=newexerciseplan)


@app.route("/exerciseplan", methods=["GET", "POST"])
def exerciseplan():
    """This function takes in user input on user's exercise
    requirements and uses a mock function to generate the best exercise
    plan and show it to users

    """
    if request.method == "POST":
        duration = request.form.get("duration")
        intensity = request.form.get("intensity")
        frequency = request.form.get("frequency")
        list1 = [1, 2, 3]

        jsonexercises = DataStructures.get_exercises_from_db()
        jsonexerciseplan = json.loads(jsonexercises)
        return render_template("exerciseplan.html",
                               bestexerciseplan=jsonexerciseplan)
    elif request.method == "GET":
        return render_template("exerciseplan.html")


class foodsform(Form):
    newfood = StringField("Food:", validators=[validators.DataRequired()])


@app.route("/listitems")
def listitems():
    # get shopping list ingredients for meal plan from database
    return render_template("shoppinglist.html")


class exerciseform(Form):
    duration = StringField("duration:", validators=[validators.DataRequired()])
    intensity = StringField("intensity:",
                            validators=[validators.DataRequired()])
    frequency = StringField("frequency:",
                            validators=[validators.DataRequired()])
    musclegroups = StringField("musclegroups:",
                               validators=[validators.DataRequired()])


@app.route("/exercises/", methods=["GET", "POST"])
def exercises():
    """This function shows the exercise requirements form
    to users where they can enter their exercise requirements

    """
    otherform = exerciseform(request.form)

    return render_template("exercises.html", form=otherform)


if __name__ == "__main__":
    app.run()
