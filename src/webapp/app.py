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
from wtforms import Form, StringField, IntegerField,DecimalField,DecimalRangeField,BooleanField,SelectField,SubmitField, validators

from webapp.data_src import DataStructures
from webapp.mealplan import MealplanGenerator
from webapp.models import User, db

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
    Calories = DecimalRangeField('Calories:',[validators.NumberRange(min=0, max=1),validators.InputRequired()],default=0)
    Carbs = DecimalRangeField('Carbs:',[validators.NumberRange(min=0, max=1),validators.InputRequired()],default=0)
    Proteins = DecimalRangeField('Proteins:',[validators.NumberRange(min=0, max=1),validators.InputRequired()],default=0)
    fat = DecimalField("Fat:",[validators.Optional()])
    Cholesterol=DecimalField("Cholesterol:",[validators.Optional()])
    Sodium=DecimalField("Sodium:",[validators.Optional()])
    Vitamina=DecimalField("Vitamina:",[validators.Optional()])
    Calcium=DecimalField("Calcium:",[validators.Optional()])
    Copper=DecimalField("Copper:",[validators.Optional()])
    Fluoride=DecimalField("Fluoride:",[validators.Optional()])
    Iodine=DecimalField("Iodine:",[validators.Optional()])
    Iron=DecimalField("Iron:",[validators.Optional()])
    Magnesium=DecimalField("Magnesium:",[validators.Optional()])
    Manganese=DecimalField("Manganese:",[validators.Optional()])
    Molybdenum=DecimalField("Molybdenum:",[validators.Optional()])
    Phosphorus=DecimalField("Phosphorus:",[validators.Optional()])
    Potassium=DecimalField("Potassium:",[validators.Optional()])
    Selenium=DecimalField("Selenium:",[validators.Optional()])
    Zinc=DecimalField("Zinc:",[validators.Optional()])


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
    session.pop("tempmealplan", None)  # removes temporary session mealplan
    session.pop("tempexerciseplan", None)  # removes temporary session exerciseplan
    session.pop("savedmealplan", None)  # removes saved session mealplan
    session.pop("savedexerciseplan", None)  # removes saved session exerciseplan
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
        if (user):  # if a user is found, we want to redirect back to signup page so user can try again
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

    if request.method == "POST":
        caloriesbreakfast = request.form.get("caloriesbreakfastamount")
        calorieslunch = request.form.get("calorieslunchamount")
        if(((float(caloriesbreakfast))+(float(calorieslunch)))<1):
            caloriesdinner=1-(float(caloriesbreakfast)+float(calorieslunch))
        elif(((float(caloriesbreakfast))+(float(calorieslunch)))==1):
            caloriesdinner=0.0
        else:
            caloriesdinner=0.0
        carbsbreakfast = request.form.get("carbsbreakfastamount")
        carbslunch = request.form.get("carbslunchamount")
        if(((float(carbsbreakfast))+(float(carbslunch)))<1):
            carbsdinner=1-(float(carbsbreakfast)+float(carbslunch))
        elif(((float(carbsbreakfast))+(float(carbslunch)))==1):
            carbsdinner=0.0
        else:
            carbsdinner=0.0
        proteinsbreakfast = request.form.get("proteinsbreakfastamount")
        proteinslunch = request.form.get("proteinslunchamount")
        if(((float(proteinsbreakfast))+(float(proteinslunch)))<1):
            proteinsdinner=1-(float(proteinsbreakfast)+float(proteinslunch))
        elif(((float(proteinsbreakfast))+(float(proteinslunch)))==1):
            proteinsdinner=0.0
        else:
            proteinsdinner=0.0
        list1 = [1, 2, 3]

        jsoninfo = DataStructures.nutritional_values()
        jsoninfo["calories"] = float(caloriesbreakfast)
        jsoninfo["carbs"] = float(carbsbreakfast)
        jsoninfo["protein"] = float(proteinsbreakfast)
        
        jsonstring = json.dumps(jsoninfo)
        mpg = MealplanGenerator(jsonstring)
        mealplan = mpg.gen_meal_plan()
        jsondata = json.loads(mealplan)
        session["tempmealplan"]=jsondata
        return render_template("mealplans.html", bestmealplan=jsondata,jsoninfo=jsoninfo)
    elif request.method == "GET":
        return render_template("mealplans.html")


@app.route("/savemealplan", methods=["GET"])
def savemealplan():
    """This function goes to the saveduserinfo page where
    the user can see their saved meal plan

    """
    session["savedmealplan"]=session["tempmealplan"]
    if request.method == "GET":
         # replacing single quotes with double quotes to change string to json format
        return redirect(url_for('saveduserinfo'))


class exerciseform(Form):
    sunday = BooleanField('Sunday')
    monday = BooleanField('Monday')
    tuesday = BooleanField('Tuesday')
    wednesday = BooleanField('Wednesday')
    thursday = BooleanField('Thursday')
    friday = BooleanField('Friday')
    saturday = BooleanField('Saturday')
    intensity = IntegerField("Intensity:",validators=[validators.InputRequired()])
    targetmusclegroup = SelectField('Choose Target Muscle Group', choices=[('back'), ('shoulders'), ('arms'),('core'),('chest'),('thighs'),('hamstrings'),('glutes')],validators=[validators.InputRequired()],validate_choice=True)


@app.route("/saveexerciseplan", methods=["GET"])
def saveexerciseplan():
    """This function takes the generated best meal plan and saves it to
    the userinfo page where they can see their saved meal plan.

    """
    session["savedexerciseplan"]=session["tempexerciseplan"]
    if request.method == "GET":
        return redirect(url_for('saveduserinfo'))


@app.route("/exerciseplan", methods=["GET", "POST"])
def exerciseplan():
    """This function takes in user input on user's exercise
    requirements and uses a mock function to generate the best exercise
    plan and show it to users

    """
    form=exerciseform(request.form)
    if request.method == "POST":
        daysofweek=[]
        
        if(form.sunday.data!=False):
            daysofweek.append("Sunday")
        if(form.monday.data!=False):
            daysofweek.append("Monday")
        if(form.tuesday.data!=False):
            daysofweek.append("Tuesday")
        if(form.wednesday.data!=False):
            daysofweek.append("Wednesday")
        if(form.thursday.data!=False):
            daysofweek.append("Thursday")
        if(form.friday.data!=False):
            daysofweek.append("Friday")
        if(form.saturday.data!=False):
            daysofweek.append("Saturday")

        intensity=form.intensity.data
        selectedtargetmuscles= form.targetmusclegroup.data

        list1 = [1, 2, 3]
    
        jsonexercises = DataStructures.get_exercises_from_db()
        jsonexerciseplan = json.loads(jsonexercises)
        session["tempexerciseplan"]=jsonexerciseplan
        print("hello")
        #daysofweek.clear()     need to empty days of week list for future requests
        return render_template("exerciseplan.html",
                               bestexerciseplan=jsonexerciseplan,days=daysofweek,intensity=intensity,muscles=selectedtargetmuscles)
        
    elif request.method == "GET":
        return render_template("exerciseplan.html")


class foodsform(Form):
    newfood = StringField("Food:", validators=[validators.DataRequired()])

@app.route("/addfood", methods=["GET", "POST"])
def addfood():
    if request.method == "POST":
        newrecipename=request.form.get("newrecipename")       #getting new food recipe to add to database
        newrecipeingredients=request.form.get("newrecipeingredients")
        newrecipecalories=request.form.get("newrecipecalories")
        newrecipecarbs=request.form.get("newrecipecarbs")
        newproteins=request.form.get("protein")
        newrecipe=DataStructures.recipe_data()
        newrecipe["name"]=newrecipename
        newrecipe["ingredients"]=[newrecipeingredients]
        if(newrecipecalories!=None and newrecipecalories!=''):
            newrecipe["nutritional value"]["calories"] = float(newrecipecalories)
        if(newrecipecarbs!=None and newrecipecarbs!=''):
            newrecipe["nutritional value"]["carbs"] = float(newrecipecarbs)
        if(newproteins!=None and newproteins!=''):
            newrecipe["nutritional value"]["protein"] = float(newproteins)
       
    
        return render_template("shoppinglist.html",jsonrecipe=newrecipe)
    


@app.route("/addexercise", methods=["GET", "POST"])
def addexercise():
    if request.method == "POST":
        dayschecked=request.form.getlist("checkboxes")   #getting new exericse to add to database
        intensity=request.form["intensity"]
        selectedtargetmuscles = request.form.get("targetmuscledropdown")
        
        return render_template("shoppinglist.html",days=dayschecked,intensity=intensity,muscles=selectedtargetmuscles)



@app.route("/listitems", methods=["GET", "POST"])
def listitems():
    if request.method == "POST":
        mealplan=[]                                     #getting new mealplan to add to database
        newfoodname1=request.form.get("newfoodname1")
        newfoodingredients1=request.form.get("newfoodingredients1")
        newfoodcalories1=request.form.get("Calories1")
        newfoodcarbs1=request.form.get("Carbs1")
        newfoodproteins1=request.form.get("Proteins1")
        newfood1=DataStructures.recipe_data()
        newfood1["name"]=newfoodname1
        newfood1["ingredients"]=[newfoodingredients1]
        if(newfoodcalories1!=None and newfoodcalories1!=''):
            newfood1["nutritional value"]["calories"] = newfoodcalories1
        if(newfoodcarbs1!=None and newfoodcarbs1!=''):
            newfood1["nutritional value"]["carbs"] = newfoodcarbs1
        if(newfoodproteins1!=None and newfoodproteins1!=''):
            newfood1["nutritional value"]["protein"] = newfoodproteins1
        mealplan.append(json.dumps(newfood1))
        newfoodname2=request.form.get("newfoodname2")
        newfoodingredients2=request.form.get("newfoodingredients2")
        newfoodcalories2=request.form.get("Calories2")
        newfoodcarbs2=request.form.get("Carbs2")
        newfoodproteins2=request.form.get("Proteins2")
        newfood2=DataStructures.recipe_data()
        newfood2["name"]=newfoodname2
        newfood2["ingredients"]=[newfoodingredients2]
        if(newfoodcalories2!=None and newfoodcalories2!=''):
            newfood2["nutritional value"]["calories"] = newfoodcalories2
        if(newfoodcarbs2!=None and newfoodcarbs2!=''):
            newfood2["nutritional value"]["carbs"] = newfoodcarbs2
        if(newfoodproteins2!=None and newfoodproteins2!=''):
            newfood2["nutritional value"]["protein"] = newfoodproteins2
        mealplan.append(json.dumps(newfood2))
        newfoodname3=request.form.get("newfoodname3")
        newfoodingredients3=request.form.get("newfoodingredients3")
        newfoodcalories3=request.form.get("Calories3")
        newfoodcarbs3=request.form.get("Carbs3")
        newfoodproteins3=request.form.get("Proteins3")
        newfood3=DataStructures.recipe_data()
        newfood3["name"]=newfoodname3
        newfood3["ingredients"]=[newfoodingredients3]
        if(newfoodcalories3!=None and newfoodcalories3!=''):
            newfood3["nutritional value"]["calories"] = newfoodcalories3
        if(newfoodcarbs3!=None and newfoodcarbs3!=''):
            newfood3["nutritional value"]["carbs"] = newfoodcarbs3
        if(newfoodproteins3!=None and newfoodproteins3!=''):
            newfood3["nutritional value"]["protein"] = newfoodproteins3
        mealplan.append(json.dumps(newfood3))
        
    
        
        
       
        
        return render_template("shoppinglist.html",mealplan=mealplan)
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
