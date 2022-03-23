import json
from random import randint
from time import strftime

from flask import Flask, flash, jsonify, render_template, request
from flask_login import LoginManager
from models import User, db
from wtforms import Form, StringField, SubmitField, validators

from webapp import data_src
from webapp.mealplan import gen_meal_plan, get_recipes_from_db

app = Flask(__name__, instance_relative_config=True)

login = LoginManager()
login.login_view = "users.login"

db.init_app(app)
login.init_app(app)


@login.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


class dietform(Form):
    Calories = StringField("Calories:", validators=[validators.DataRequired()])
    Carbs = StringField("Carbs:", validators=[validators.DataRequired()])
    Proteins = StringField("Proteins:", validators=[validators.DataRequired()])
    Fibers = StringField("Fibers:", validators=[validators.DataRequired()])
    Allergies = StringField("Allergies:",
                            validators=[validators.DataRequired()])


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/points/")
def points():
    return render_template("points.html")


@app.route("/signup/")
def signup():
    return render_template("signup.html")


@app.route("/diet/", methods=["GET", "POST"])
def diet():
    form = dietform(request.form)
    if request.method == "POST":
        Calories = request.form["Calories"]
        Carbs = request.form["Carbs"]
        Proteins = request.form["Proteins"]
        Fibers = request.form["Fibers"]
        Allergies = request.form["Allergies"]

        if form.validate():
            if (int(Calories) < 0 or int(Carbs) < 0 or int(Proteins) < 0
                    or int(Fibers) < 0):
                flash("Error: No negative numbers allowed")
            else:
                flash("You entered this many calories: {}".format(Calories))

        else:
            flash("Error: All Fields are Required")

    return render_template("mealplanner.html", form=form)


@app.route("/mealplan", methods=["GET", "POST"])
def mealplan():
    if request.method == "POST":
        Calories = request.form.get("Calories")
        Carbs = request.form.get("Carbs")
        protein = request.form.get("Proteins")
        list1 = [1, 2, 3]

        jsoninfo = data_src.nutritional_values()
        jsoninfo["calories"] = int(Calories)
        jsoninfo["carbs"] = int(Carbs)
        jsoninfo["protein"] = int(protein)
        jsonstring = json.dumps(jsoninfo)
        mealplan = gen_meal_plan(jsonstring)
        return render_template("mealplans.html", bestmealplan=mealplan)
    elif request.method == "GET":
        return render_template("mealplans.html")


@app.route("/exerciseplan/")
def exerciseplan():
    exerciseplan = ["run", "jump"]  # get exerciseplan for week from database
    return render_template("exerciseplan.html", exerciseplan=exerciseplan)


class foodsform(Form):
    newfood = StringField("Food:", validators=[validators.DataRequired()])


@app.route("/listitems/")
def listitems():
    foodform = dietform(request.form)
    if request.method == "POST":
        newfood = request.form["Food"]

        if foodform.validate():

            return render_template("shoppinglist.html", form=foodform)

        else:
            flash("Error: All Fields are Required")

    return render_template("shoppinglist.html", form=foodform)


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
    otherform = exerciseform(request.form)
    if request.method == "POST":
        duration = request.form["duration"]
        intensity = request.form["intensity"]
        frequency = request.form["frequency"]
        musclegroups = request.form["musclegroups"]

        if otherform.validate():
            if int(duration) < 0 or int(frequency) < 0:
                flash("Error: No negative numbers allowed")
            else:
                flash("You entered this much duration: {}".format(duration))

        else:
            flash("Error: All Fields are Required")

    return render_template("exercises.html", form=otherform)


if __name__ == "__main__":
    app.run()
