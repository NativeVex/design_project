import json
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
from flask_login import LoginManager
from wtforms import Form, StringField, SubmitField, validators

from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator
from webapp.newuser import createnewuser

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(__name__)

app.config["SECRET_KEY"] = "5e4c0f48eef083bde520ef8027eb12e3f8bafcc763969d58"


class signupform(Form):
    email = StringField("Email:", validators=[validators.DataRequired()])
    username = StringField("Username:", validators=[validators.DataRequired()])
    password = StringField("Password:", validators=[validators.DataRequired()])


class loginform(Form):
    username = StringField("Carbs:", validators=[validators.DataRequired()])
    password = StringField("Proteins:", validators=[validators.DataRequired()])


class dietform(Form):
    Calories = StringField("Calories:", validators=[validators.DataRequired()])
    Carbs = StringField("Carbs:", validators=[validators.DataRequired()])
    Proteins = StringField("Proteins:", validators=[validators.DataRequired()])
    Fibers = StringField("Fibers:", validators=[validators.DataRequired()])
    Allergies = StringField("Allergies:",
                            validators=[validators.DataRequired()])


@app.route("/", methods=["GET", "POST"])
def login():
    """This function uses a post request to take
    in a username and password entered by the user to login
    and then redirects to the page where users enter their health requirements

    """
    userloginform = loginform(request.form)
    if request.method == "POST":
        session["username"] = request.form.get("username")
        password = request.form.get("password")
        return redirect(url_for("diet"))
    else:
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
        if "@" not in email:
            abort(404)
        jsonuser = createnewuser(email, username, password)
        return render_template("signup.html", jsonnewuser=jsonuser)
    else:
        return render_template("signup.html")


@app.route("/diet/", methods=["GET", "POST"])
def diet():
    """This function goes to the mealplanner page where
    the user sees a form where they can enter their diet requirements

    """
    form = dietform(request.form)
    return render_template("mealplanner.html", form=form)


@app.route("/mealplan", methods=["GET", "POST"])
def mealplan():
    """This function goes to the mealplans page where
    the user their generated meal plan from their entered
    diet requirements

    """
    if request.method == "POST":
        Calories = request.form.get("Calories")
        Carbs = request.form.get("Carbs")
        protein = request.form.get("Proteins")
        list1 = [1, 2, 3]
        if (calories.isnumeric() == False or carbs.isnumeric() == False
                or protein.isnumeric() == False):
            abort(404)

        jsoninfo = DataStructures.nutritional_values()
        jsoninfo["calories"] = int(Calories)
        jsoninfo["carbs"] = int(Carbs)
        jsoninfo["protein"] = int(protein)
        jsonstring = json.dumps(jsoninfo)
        mpg = MealplanGenerator(jsonstring)
        mealplan = mpg.gen_meal_plan()
        jsondata = json.loads(mealplan)
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


@app.route("/listitems/")
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
