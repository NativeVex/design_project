import json
from cmath import log
from locale import currency
from random import randint
from time import strftime
import os

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
from wtforms import (
    BooleanField,
    DecimalField,
    DecimalRangeField,
    Form,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    validators,
)

from webapp.data_src import DataStructures
from webapp.exerciseplan import (
    ExerciseplanGenerator,
    add_exercise_to_db,
    get_exerciseplan,
    save_exerciseplan,
)
from webapp.health_req import get_curr_health_req, get_old_health_req, save_health_req
from webapp.mealplan import (
    MealplanGenerator,
    add_recipe,
    get_mealplan,
    get_recipes_from_db,
    save_mealplan,
)
from webapp.models import Recipes, User, db

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(__name__)
app.config["SECRET_KEY"] = "5e4c0f48eef083bde520ef8027eb12e3f8bafcc763969d58"

app.config["SQLALCHEMY_DATABASE_URI"] = str(os.environ.get('URI'))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

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
    Calories = DecimalField("Calories:", [validators.InputRequired()])
    Carbs = DecimalField("Carbs:", [validators.InputRequired()])
    Proteins = DecimalField("Proteins:", [validators.InputRequired()])
    fat = DecimalField("Fat:", [validators.Optional()])
    fiber = DecimalField("Fiber:", [validators.Optional()])
    monounsaturated_fat = DecimalField("Monosaturated fat:",
                                       [validators.Optional()])
    polyunsaturated_fat = DecimalField("Polyunsaturated fat:",
                                       [validators.Optional()])
    saturated_fat = DecimalField("saturated fat:", [validators.Optional()])
    Cholesterol = DecimalField("Cholesterol:", [validators.Optional()])
    sugar = DecimalField("Sugar:", [validators.Optional()])
    trans_fat = DecimalField("Trans fat:", [validators.Optional()])
    Sodium = DecimalField("Sodium:", [validators.Optional()])
    Vitamina = DecimalField("Vitamina:", [validators.Optional()])
    Vitaminc = DecimalField("Vitaminc:", [validators.Optional()])
    Calcium = DecimalField("Calcium:", [validators.Optional()])
    Iron = DecimalField("Iron:", [validators.Optional()])
    Potassium = DecimalField("Potassium:", [validators.Optional()])


@app.route("/", methods=["GET", "POST"])
def login():
    """This function uses a post request to take
    in a username and password entered by the user to login
    and then redirects to the page where users enter their health requirements
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        session["email"] = email
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
    session.pop("email", None)  # removes temporary session exerciseplan
    session.pop("tempmealplan", None)  # removes temporary session mealplan
    session.pop("tempexerciseplan",
                None)  # removes temporary session exerciseplan
    session.pop("savedmealplan", None)  # removes saved session mealplan
    session.pop("savedexerciseplan",
                None)  # removes saved session exerciseplan
    session.pop("currenthealthrequirements",
                None)  # removes current session healthrequirements
    session.pop("oldhealthrequirements",
                None)  # removes old healthrequirements
    session.pop("newhealthrequirements",
                None)  # removes new healthrequirements

    return redirect("/")


@app.route("/changehealthrequirements", methods=["GET", "POST"])
def changehealthrequirements():
    """This function gets current health configurations for the user"""
    form = dietform(request.form)
    email = session["email"]

    curr_health_req = get_curr_health_req(email)

    old_health_req = get_old_health_req(email)

    return render_template(
        "healthrequirements.html",
        form=form,
        curr_health_req=curr_health_req,
        old_health_req=old_health_req,
    )


@app.route("/savenewhealthrequirements", methods=["GET", "POST"])
def savenewhealthrequirements():
    """This function saves new health configurations from user"""
    form = dietform(request.form)
    email = session["email"]

    if request.method == "POST":
        new_health_req = DataStructures.health_requirement()
        new_health_req["meal_req"]["calories"] = float(form.Calories.data)
        new_health_req["meal_req"]["carbohydrate"] = float(form.Carbs.data)
        new_health_req["meal_req"]["protein"] = float(form.Proteins.data)
        new_health_req["exercise_req"]["days"] = request.form.get("days")
        new_health_req["exercise_req"]["intensity"] = request.form.get(
            "intensity")
        new_health_req["exercise_req"]["targetmusclegroup"] = request.form.get(
            "targetmusclegroup")

        if form.fat.data != None:
            new_health_req["meal_req"]["fat"] = float(form.fat.data)
        else:
            new_health_req["meal_req"]["fat"] = 0.0

        if form.Cholesterol.data != None:
            new_health_req["meal_req"]["cholesterol"] = float(
                form.Cholesterol.data)
        else:
            new_health_req["meal_req"]["cholesterol"] = 0.0
        if form.Sodium.data != None:
            new_health_req["meal_req"]["sodium"] = float(form.Sodium.data)
        else:
            new_health_req["meal_req"]["sodium"] = 0.0

        if form.Vitamina.data != None:
            new_health_req["meal_req"]["vitamin_a"] = float(form.Vitamina.data)
        else:
            new_health_req["meal_req"]["vitamin_a"] = 0.0
        if form.Vitaminc.data != None:
            new_health_req["meal_req"]["vitamin_c"] = float(form.Vitaminc.data)
        else:
            new_health_req["meal_req"]["vitamin_c"] = 0.0

        if form.Calcium.data != None:
            new_health_req["meal_req"]["calcium"] = float(form.Calcium.data)
        else:
            new_health_req["meal_req"]["calcium"] = 0.0
        if form.fiber.data != None:
            new_health_req["meal_req"]["fiber"] = float(form.fiber.data)
        else:
            new_health_req["meal_req"]["fiber"] = 0.0

        if form.monounsaturated_fat.data != None:
            new_health_req["meal_req"]["monounsaturated_fat"] = float(
                form.monounsaturated_fat.data)
        else:
            new_health_req["meal_req"]["monounsaturated_fat"] = 0.0
        if form.polyunsaturated_fat.data != None:
            new_health_req["meal_req"]["polyunsaturated_fat"] = float(
                form.polyunsaturated_fat.data)
        else:
            new_health_req["meal_req"]["polyunsaturated_fat"] = 0.0
        if form.saturated_fat.data != None:
            new_health_req["meal_req"]["saturated_fat"] = float(
                form.saturated_fat.data)
        else:
            new_health_req["meal_req"]["saturated_fat"] = 0.0
        if form.sugar.data != None:
            new_health_req["meal_req"]["sugar"] = float(form.sugar.data)
        else:
            new_health_req["meal_req"]["sugar"] = 0.0
        if form.trans_fat.data != None:
            new_health_req["meal_req"]["trans_fat"] = float(
                form.trans_fat.data)
        else:
            new_health_req["meal_req"]["trans_fat"] = 0.0
        if form.Iron.data != None:
            new_health_req["meal_req"]["iron"] = float(form.Iron.data)
        else:
            new_health_req["meal_req"]["iron"] = 0.0
        if form.Potassium.data != None:
            new_health_req["meal_req"]["potassium"] = float(
                form.Potassium.data)
        else:
            new_health_req["meal_req"]["potassium"] = 0.0

        save_health_req(email, new_health_req)

        curr_health_req = get_curr_health_req(email)
        old_health_req = get_old_health_req(email)

        message = "New health requirements are saved!"
    return render_template(
        "healthrequirements.html",
        form=form,
        curr_health_req=curr_health_req,
        old_health_req=old_health_req,
        message=message,
    )


@app.route("/saveduserinfo/", methods=["GET"])
def saveduserinfo():
    """This function goes to the saveduserinfo page where
    the user sees their saved meal plan and their saved
    exercise plan
    """
    savedmealplan = get_mealplan(session["email"])
    savedexerciseplan = get_exerciseplan(session["email"])

    return render_template(
        "saveduserinfo.html",
        savedmealplan=savedmealplan,
        savedexerciseplan=savedexerciseplan,
    )


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

        jsoninfo = DataStructures.nutritional_values()
        jsoninfo["calories"] = float(form.Calories.data)
        jsoninfo["carbohydrate"] = float(form.Carbs.data)
        jsoninfo["protein"] = float(form.Proteins.data)

        if form.fat.data != None:
            jsoninfo["fat"] = float(form.fat.data)
        if form.Cholesterol.data != None:
            jsoninfo["cholesterol"] = float(form.Cholesterol.data)
        if form.Sodium.data != None:
            jsoninfo["sodium"] = float(form.Sodium.data)
        if form.Vitamina.data != None:
            jsoninfo["vitamin_a"] = float(form.Vitamina.data)
        if form.Vitaminc.data != None:
            jsoninfo["vitamin_c"] = float(form.Vitaminc.data)
        if form.Calcium.data != None:
            jsoninfo["calcium"] = float(form.Calcium.data)
        if form.fiber.data != None:
            jsoninfo["fiber"] = float(form.fiber.data)
        if form.monounsaturated_fat.data != None:
            jsoninfo["monounsaturated_fat"] = float(
                form.monounsaturated_fat.data)
        if form.polyunsaturated_fat.data != None:
            jsoninfo["polyunsaturated_fat"] = float(
                form.polyunsaturated_fat.data)
        if form.saturated_fat.data != None:
            jsoninfo["saturated_fat"] = float(form.saturated_fat.data)
        if form.sugar.data != None:
            jsoninfo["sugar"] = float(form.sugar.data)
        if form.trans_fat.data != None:
            jsoninfo["trans_fat"] = float(form.trans_fat.data)
        if form.Iron.data != None:
            jsoninfo["iron"] = float(form.Iron.data)
        if form.Potassium.data != None:
            jsoninfo["potassium"] = float(form.Potassium.data)

        caloriesbreakfast = request.form.get("caloriesbreakfastamount")

        firstslidervalue = float(request.form.get("caloriesbreakfastamount"))
        secondslidervalue = float(request.form.get("calorieslunchamount"))
        calorieslunch = secondslidervalue - firstslidervalue
        if calorieslunch < 0:
            message = "Invalid Slider Values, Please Enter Values Again"
            return render_template("mealplanner.html",
                                   form=form,
                                   message=message)
        caloriesdinner = 1 - secondslidervalue

        carbsbreakfast = request.form.get("carbsbreakfastamount")

        firstslidervalue2 = float(request.form.get("carbsbreakfastamount"))
        secondslidervalue2 = float(request.form.get("carbslunchamount"))
        carbslunch = secondslidervalue2 - firstslidervalue2
        if carbslunch < 0:
            message = "Invalid Slider Values, Please Enter Values Again"
            return render_template("mealplanner.html",
                                   form=form,
                                   message=message)
        carbsdinner = 1 - secondslidervalue2

        proteinsbreakfast = request.form.get("proteinsbreakfastamount")
        firstslidervalue3 = float(request.form.get("proteinsbreakfastamount"))
        secondslidervalue3 = float(request.form.get("proteinslunchamount"))
        proteinslunch = secondslidervalue3 - firstslidervalue3
        if proteinslunch < 0:
            message = "Invalid Slider Values, Please Enter Values Again"
            return render_template("mealplanner.html",
                                   form=form,
                                   message=message)
        proteinsdinner = 1 - secondslidervalue3

        list1 = [1, 2, 3]
        caloriesarr = []
        carbsarr = []
        proteinsarr = []
        caloriesarr.append(round(float(caloriesbreakfast), 2))
        caloriesarr.append(round(float(calorieslunch), 2))
        caloriesarr.append(round(float(caloriesdinner), 2))
        carbsarr.append(round(float(carbsbreakfast), 2))
        carbsarr.append(round(float(carbslunch), 2))
        carbsarr.append(round(float(carbsdinner), 2))
        proteinsarr.append(round(float(proteinsbreakfast), 2))
        proteinsarr.append(round(float(proteinslunch), 2))
        proteinsarr.append(round(float(proteinsdinner), 2))

        jsondata = {}
        jsondata["calorie_split"] = caloriesarr
        jsondata["carbs_split"] = carbsarr
        jsondata["protein_split"] = proteinsarr
        newjsonsplitdata = json.dumps(jsondata)
        newjsoninfo = json.dumps(jsoninfo)
        mpg = MealplanGenerator(newjsoninfo, newjsonsplitdata)
        mealplan = mpg.gen_meal_plan()
        session["tempmealplan"] = json.loads(mealplan)
        newmeal = json.loads(mealplan)
        return render_template("mealplans.html", bestmealplan=newmeal)
    elif request.method == "GET":
        return render_template("mealplans.html")


@app.route("/savemealplan", methods=["GET", "POST"])
def savemealplan():
    """This function goes to the saveduserinfo page where
    the user can see their saved meal plan
    """
    email = session["email"]
    mealplan = session["tempmealplan"]
    print(email)

    session["savedmealplan"] = save_mealplan(email, mealplan)

    # replacing single quotes with double quotes to change string to json format
    return redirect(url_for("saveduserinfo"))


class exerciseform(Form):
    sunday = BooleanField("Sunday")
    monday = BooleanField("Monday")
    tuesday = BooleanField("Tuesday")
    wednesday = BooleanField("Wednesday")
    thursday = BooleanField("Thursday")
    friday = BooleanField("Friday")
    saturday = BooleanField("Saturday")
    intensity = IntegerField("Intensity:",
                             validators=[validators.InputRequired()])
    targetmusclegroup = SelectField(
        "Choose Target Muscle Group",
        choices=[
            ("back"),
            ("shoulders"),
            ("arms"),
            ("core"),
            ("chest"),
            ("thighs"),
            ("hamstrings"),
            ("glutes"),
        ],
        validators=[validators.InputRequired()],
        validate_choice=True,
    )
    back = BooleanField("Back")
    shoulders = BooleanField("Shoulders")
    arms = BooleanField("Arms")
    core = BooleanField("Core")
    chest = BooleanField("Chest")
    thighs = BooleanField("Thighs")
    hamstrings = BooleanField("Hamstrings")
    glutes = BooleanField("Glutes")
    triceps = BooleanField("triceps")
    quads = BooleanField("quads")
    abs = BooleanField("abs")
    upperback = BooleanField("upperback")
    lowerback = BooleanField("lowerback")
    biceps = BooleanField("biceps")
    calves = BooleanField("calves")
    sideabs = BooleanField("sideabs")
    cardio = BooleanField("cardio")
    traps = BooleanField("traps")


@app.route("/saveexerciseplan", methods=["GET"])
def saveexerciseplan():
    """This function takes the generated best meal plan and saves it to
    the userinfo page where they can see their saved meal plan.
    """
    session["savedexerciseplan"] = save_exerciseplan(
        session["email"], session["tempexerciseplan"])

    if request.method == "GET":
        return redirect(url_for("saveduserinfo"))


@app.route("/exerciseplan", methods=["GET", "POST"])
def exerciseplan():
    """This function takes in user input on user's exercise
    requirements and uses a mock function to generate the best exercise
    plan and show it to users
    """
    form = exerciseform(request.form)
    if request.method == "POST":
        daysofweek = []

        if form.sunday.data != False:
            daysofweek.append("Sunday")
        if form.monday.data != False:
            daysofweek.append("Monday")
        if form.tuesday.data != False:
            daysofweek.append("Tuesday")
        if form.wednesday.data != False:
            daysofweek.append("Wednesday")
        if form.thursday.data != False:
            daysofweek.append("Thursday")
        if form.friday.data != False:
            daysofweek.append("Friday")
        if form.saturday.data != False:
            daysofweek.append("Saturday")

        exercisedata = DataStructures.exercise_reqs()
        if form.sunday.data != False:
            exercisedata["days"]["Sunday"] = True
        if form.monday.data != False:
            exercisedata["days"]["Monday"] = True
        if form.tuesday.data != False:
            exercisedata["days"]["Tuesday"] = True
        if form.wednesday.data != False:
            exercisedata["days"]["Wednesday"] = True
        if form.thursday.data != False:
            exercisedata["days"]["Thursday"] = True
        if form.friday.data != False:
            exercisedata["days"]["Friday"] = True
        if form.saturday.data != False:
            exercisedata["days"]["Saturday"] = True
        intensity = form.intensity.data

        exercisedata["level"] = int(intensity)

        # selectedtargetmuscles= form.targetmusclegroup.data
        targetmusclegroups = []
        if form.upperback.data != False:
            targetmusclegroups.append("upper back")
        if form.lowerback.data != False:
            targetmusclegroups.append("lower back")
        if form.triceps.data != False:
            targetmusclegroups.append("triceps")
        if form.abs.data != False:
            targetmusclegroups.append("abs")
        if form.calves.data != False:
            targetmusclegroups.append("calves")
        if form.sideabs.data != False:
            targetmusclegroups.append("side abs")
        if form.cardio.data != False:
            targetmusclegroups.append("cardio")
        if form.traps.data != False:
            targetmusclegroups.append("traps")
        if form.shoulders.data != False:
            targetmusclegroups.append("shoulders")
        if form.arms.data != False:
            targetmusclegroups.append("arms")
        if form.core.data != False:
            targetmusclegroups.append("core")
        if form.chest.data != False:
            targetmusclegroups.append("chest")
        if form.thighs.data != False:
            targetmusclegroups.append("thighs")
        if form.hamstrings.data != False:
            targetmusclegroups.append("hamstrings")
        if form.glutes.data != False:
            targetmusclegroups.append("glutes")

        list1 = [1, 2, 3]
        exercisedata["targetmusclegroups"] = targetmusclegroups

        newexerciseplan = json.dumps(exercisedata)
        epg = ExerciseplanGenerator(newexerciseplan)
        exerciseplan = epg.gen_exercise_plan()
        userexerciseplan = json.loads(exerciseplan)
        session["tempexerciseplan"] = userexerciseplan
        # daysofweek.clear()     may need to empty days of week list for future requests
        # targetmusclegroups.clear()
        return render_template("exerciseplan.html",
                               bestexerciseplan=userexerciseplan)

    elif request.method == "GET":
        return render_template("exerciseplan.html")


class foodsform(Form):
    newfood = StringField("Food:", validators=[validators.DataRequired()])


@app.route("/addfood", methods=["GET", "POST"])
def addfood():
    """This function takes user input to add a food recipe to
    the database

    """
    if request.method == "POST":
        newrecipename = request.form.get(
            "newrecipename")  # getting new food recipe to add to database
        newrecipeingredients = request.form.get("newrecipeingredients")
        foodtype = request.form.get("foodtype")
        numberofservings = request.form.get("numberofservings")
        newrecipedirections = request.form.get("newrecipedirections")

        newrecipecalories = request.form.get("newrecipecalories")
        newrecipecarbs = request.form.get("newrecipecarbs")
        newproteins = request.form.get("protein")
        fat = request.form.get("fat")
        cholesterol = request.form.get("cholesterol")
        sodium = request.form.get("sodium")
        vitamina = request.form.get("vitamina")
        vitaminc = request.form.get("vitaminc")
        calcium = request.form.get("calcium")
        fiber = request.form.get("fiber")
        monounsaturated_fat = request.form.get("monounsaturated_fat")
        polyunsaturated_fat = request.form.get("polyunsaturated_fat")
        saturated_fat = request.form.get("saturated_fat")
        sugar = request.form.get("sugar")
        trans_fat = request.form.get("trans_fat")
        iron = request.form.get("iron")
        potassium = request.form.get("potassium")
        newrecipe = DataStructures.recipe_data()
        newrecipe["name"] = newrecipename
        newrecipe["ingredients"] = [newrecipeingredients]
        newrecipe["directions"] = [newrecipedirections]

        if newrecipecalories != None and newrecipecalories != "":
            newrecipe["nutritional_values"]["calories"] = float(
                newrecipecalories)
        if newrecipecarbs != None and newrecipecarbs != "":
            newrecipe["nutritional_values"]["carbohydrate"] = float(
                newrecipecarbs)
        if newproteins != None and newproteins != "":
            newrecipe["nutritional_values"]["protein"] = float(newproteins)
        if fat != None and fat != "":
            newrecipe["nutritional_values"]["fat"] = float(fat)
        if cholesterol != None and cholesterol != "":
            newrecipe["nutritional_values"]["cholesterol"] = float(cholesterol)
        if sodium != None and sodium != "":
            newrecipe["nutritional_values"]["sodium"] = float(sodium)
        if vitamina != None and vitamina != "":
            newrecipe["nutritional_values"]["vitamin_a"] = float(vitamina)
        if vitaminc != None and vitaminc != "":
            newrecipe["nutritional_values"]["vitamin_c"] = float(vitaminc)
        if calcium != None and calcium != "":
            newrecipe["nutritional_values"]["calcium"] = float(calcium)
        if fiber != None and fiber != "":
            newrecipe["nutritional_values"]["fiber"] = float(fiber)
        if monounsaturated_fat != None and monounsaturated_fat != "":
            newrecipe["nutritional_values"]["monounsaturated_fat"] = float(
                monounsaturated_fat)
        if polyunsaturated_fat != None and polyunsaturated_fat != "":
            newrecipe["nutritional_values"]["polyunsaturated_fat"] = float(
                polyunsaturated_fat)
        if saturated_fat != None and saturated_fat != "":
            newrecipe["nutritional_values"]["saturated_fat"] = float(
                saturated_fat)
        if trans_fat != None and trans_fat != "":
            newrecipe["nutritional_values"]["trans_fat"] = float(trans_fat)
        if iron != None and iron != "":
            newrecipe["nutritional_values"]["iron"] = float(iron)
        if sugar != None and sugar != "":
            newrecipe["nutritional_values"]["sugar"] = float(sugar)
        if potassium != None and potassium != "":
            newrecipe["nutritional_values"]["potassium"] = float(potassium)

        if numberofservings != "" and numberofservings != None:
            newrecipe["number_of_servings"] = int(numberofservings)
        newrecipe["type"] = foodtype
        add_recipe(
            newrecipe["name"],
            newrecipe["directions"],
            newrecipe["ingredients"],
            newrecipe["nutritional_values"]["calories"],
            newrecipe["nutritional_values"]["carbohydrate"],
            newrecipe["nutritional_values"]["protein"],
            newrecipe["nutritional_values"]["cholesterol"],
            newrecipe["nutritional_values"]["fat"],
            newrecipe["nutritional_values"]["fiber"],
            newrecipe["nutritional_values"]["iron"],
            newrecipe["nutritional_values"]["monounsaturated_fat"],
            newrecipe["nutritional_values"]["polyunsaturated_fat"],
            newrecipe["nutritional_values"]["potassium"],
            newrecipe["nutritional_values"]["calcium"],
            newrecipe["nutritional_values"]["saturated_fat"],
            newrecipe["nutritional_values"]["sodium"],
            newrecipe["nutritional_values"]["sugar"],
            newrecipe["nutritional_values"]["trans_fat"],
            newrecipe["nutritional_values"]["vitamin_a"],
            newrecipe["nutritional_values"]["vitamin_c"],
            newrecipe["number_of_servings"],
            newrecipe["type"],
        )
        message = "Food recipe added!"

        return render_template("shoppinglist.html", message2=message)


@app.route("/addexercise", methods=["GET", "POST"])
def addexercise():
    """This function takes user input to add an exercise to
    the database

    """
    if request.method == "POST":
        # getting new exericse to add to database
        name = request.form["name"]
        intensity = request.form["intensity"]
        sets = request.form["sets"]
        reps = request.form["reps"]
        selectedtargetmuscles = request.form.getlist("muscles")
        exercisedata = DataStructures.exercise()

        if name != "" and name != None:
            exercisedata["name"] = name
        if intensity != "" and intensity != None:
            exercisedata["level"] = int(intensity)
        if sets != "" and sets != None:
            exercisedata["sets"] = int(sets)
        if reps != "" and reps != None:
            exercisedata["reps"] = int(reps)
        exercisedata["targetmusclegroups"] = selectedtargetmuscles
        add_exercise_to_db(
            exercisedata["name"],
            exercisedata["targetmusclegroups"],
            exercisedata["level"],
            exercisedata["sets"],
            exercisedata["reps"],
        )
        message = "Exercise added!"  # add exercise to database
        return render_template("shoppinglist.html", message=message)


@app.route("/listitems", methods=["GET", "POST"])
def listitems():
    """This function takes user input to add a meal plan of recipes to
    the database

    """
    if request.method == "POST":

        return render_template("shoppinglist.html")
    elif request.method == "GET":
        return render_template("shoppinglist.html")


@app.route("/exercises/", methods=["GET", "POST"])
def exercises():
    """This function shows the exercise requirements form
    to users where they can enter their exercise requirements
    """
    otherform = exerciseform(request.form)

    return render_template("exercises.html", form=otherform)


if __name__ == "__main__":
    app.run()
