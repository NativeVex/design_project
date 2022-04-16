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
from webapp.exerciseplan import ExerciseplanGenerator

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
    Calories = DecimalField("Calories:",[validators.InputRequired()])
    Carbs = DecimalField("Carbs:",[validators.InputRequired()])
    Proteins = DecimalField("Proteins:",[validators.InputRequired()])
    fat = DecimalField("Fat:",[validators.Optional()])
    fiber=DecimalField("Fiber:",[validators.Optional()])
    monounsaturated_fat=DecimalField("Monosaturated fat:",[validators.Optional()])
    polyunsaturated_fat=DecimalField("Polyunsaturated fat:",[validators.Optional()])
    saturated_fat=DecimalField("saturated fat:",[validators.Optional()])
    Cholesterol=DecimalField("Cholesterol:",[validators.Optional()])
    sugar=DecimalField("Sugar:",[validators.Optional()])
    trans_fat=DecimalField("Trans fat:",[validators.Optional()])
    Sodium=DecimalField("Sodium:",[validators.Optional()])
    Vitamina=DecimalField("Vitamina:",[validators.Optional()])
    Vitaminc=DecimalField("Vitaminc:",[validators.Optional()])
    Calcium=DecimalField("Calcium:",[validators.Optional()])
    Iron=DecimalField("Iron:",[validators.Optional()])
    Potassium=DecimalField("Potassium:",[validators.Optional()])
    


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
    form = dietform(request.form)
    if request.method == "POST":

        jsoninfo=DataStructures.nutritional_values()
        jsoninfo["calories"]=float(form.Calories.data)
        jsoninfo["carbohydrate"]=float(form.Carbs.data)
        jsoninfo["protein"]=float(form.Proteins.data)


        if(form.fat.data!=None):
            jsoninfo["fat"]=float(form.fat.data)
        if(form.Cholesterol.data!=None):
            jsoninfo["cholesterol"]=float(form.Cholesterol.data)
        if(form.Sodium.data!=None):
            jsoninfo["sodium"]=float(form.Sodium.data)
        if(form.Vitamina.data!=None):
            jsoninfo["vitamin_a"]=float(form.Vitamina.data)
        if(form.Vitaminc.data!=None):
            jsoninfo["vitamin_c"]=float(form.Vitaminc.data)
        if(form.Calcium.data!=None):
            jsoninfo["calcium"]=float(form.Calcium.data)
        if(form.fiber.data!=None):
            jsoninfo["fiber"]=float(form.fiber.data)
        if(form.monounsaturated_fat.data!=None):
            jsoninfo["monounsaturated_fat"]=float(form.monounsaturated_fat.data)
        if(form.polyunsaturated_fat.data!=None):
            jsoninfo["polyunsaturated_fat"]=float(form.polyunsaturated_fat.data)
        if(form.saturated_fat.data!=None):
            jsoninfo["saturated_fat"]=float(form.saturated_fat.data)
        if(form.sugar.data!=None):
            jsoninfo["sugar"]=float(form.sugar.data)
        if(form.trans_fat.data!=None):
            jsoninfo["trans_fat"]=float(form.trans_fat.data)
        if(form.Iron.data!=None):
            jsoninfo["iron"]=float(form.Iron.data)
        if(form.Potassium.data!=None):
            jsoninfo["potassium"]=float(form.Potassium.data)
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
        caloriesarr=[]
        carbsarr=[]
        proteinsarr=[]
        caloriesarr.append(float(caloriesbreakfast))
        caloriesarr.append(float(calorieslunch))
        caloriesarr.append(round(float(caloriesdinner),1))
        carbsarr.append(float(carbsbreakfast))
        carbsarr.append(float(carbslunch))
        carbsarr.append(round(float(carbsdinner),1))
        proteinsarr.append(float(proteinsbreakfast))
        proteinsarr.append(float(proteinslunch))
        proteinsarr.append(round(float(proteinsdinner),1))

        jsondata={}
        jsondata['calorie_split']=caloriesarr
        jsondata['carbs_split']=carbsarr
        jsondata['protein_split']=proteinsarr
        newjsonsplitdata=json.dumps(jsondata)
        newjsoninfo=json.dumps(jsoninfo)
        mpg = MealplanGenerator(newjsoninfo,newjsonsplitdata)
        mealplan = mpg.gen_meal_plan()
        newmealplan=json.loads(mealplan)
        session["tempmealplan"]=newmealplan
        return render_template("mealplans.html", bestmealplan=newmealplan,newjsonsplitdata=newjsonsplitdata,newjsoninfo=newjsoninfo)
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
    back=BooleanField('Back')
    shoulders=BooleanField('Shoulders')
    arms=BooleanField('Arms')
    core=BooleanField('Core')
    chest=BooleanField('Chest')
    thighs=BooleanField('Thighs')
    hamstrings=BooleanField('Hamstrings')
    glutes=BooleanField('Glutes')
    triceps=BooleanField('triceps')
    quads=BooleanField('quads')
    abs=BooleanField('abs')
    upperback=BooleanField('upperback')
    lowerback=BooleanField('lowerback')
    biceps=BooleanField('biceps')
    calves=BooleanField('calves')
    sideabs=BooleanField('sideabs')
    cardio=BooleanField('cardio')
    traps=BooleanField('traps')





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

        exercisedata=DataStructures.exercise_reqs()   
        if(form.sunday.data!=False):
            exercisedata["days"]["Sunday"]=True
        if(form.monday.data!=False):
            exercisedata["days"]["Monday"]=True
        if(form.tuesday.data!=False):
            exercisedata["days"]["Tuesday"]=True
        if(form.wednesday.data!=False):
            exercisedata["days"]["Wednesday"]=True
        if(form.thursday.data!=False):
            exercisedata["days"]["Thursday"]=True
        if(form.friday.data!=False):
            exercisedata["days"]["Friday"]=True
        if(form.saturday.data!=False):
            exercisedata["days"]["Saturday"]=True
        intensity=form.intensity.data

        exercisedata["level"]=int(intensity)

        #selectedtargetmuscles= form.targetmusclegroup.data
        targetmusclegroups=[]
        if(form.upperback.data!=False):
            targetmusclegroups.append("upper back")
        if(form.lowerback.data!=False):
            targetmusclegroups.append("lower back")
        if(form.triceps.data!=False):
            targetmusclegroups.append("triceps")
        if(form.abs.data!=False):
            targetmusclegroups.append("abs")
        if(form.calves.data!=False):
            targetmusclegroups.append("calves")
        if(form.sideabs.data!=False):
            targetmusclegroups.append("side abs")
        if(form.cardio.data!=False):
            targetmusclegroups.append("cardio")
        if(form.traps.data!=False):
            targetmusclegroups.append("traps")
        if(form.shoulders.data!=False):
            targetmusclegroups.append("shoulders")
        if(form.arms.data!=False):
            targetmusclegroups.append("arms")
        if(form.core.data!=False):
            targetmusclegroups.append("core")
        if(form.chest.data!=False):
            targetmusclegroups.append("chest")
        if(form.thighs.data!=False):
            targetmusclegroups.append("thighs")
        if(form.hamstrings.data!=False):
            targetmusclegroups.append("hamstrings")
        if(form.glutes.data!=False):
            targetmusclegroups.append("glutes")
        
        list1 = [1, 2, 3]
        exercisedata["targetmusclegroups"]=targetmusclegroups

        newexerciseplan=json.dumps(exercisedata)
        epg = ExerciseplanGenerator(newexerciseplan)
        exerciseplan = epg.gen_exercise_plan()
        userexerciseplan=json.loads(exerciseplan)
        session["tempexerciseplan"]=userexerciseplan
        #daysofweek.clear()     may need to empty days of week list for future requests
        #targetmusclegroups.clear()
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
        newrecipename=request.form.get("newrecipename")       #getting new food recipe to add to database
        newrecipeingredients=request.form.get("newrecipeingredients")
        foodtype=request.form.get("foodtype")
        numberofservings=request.form.get("numberofservings")
        newrecipedirections=request.form.get("newrecipedirections")

        newrecipecalories=request.form.get("newrecipecalories")
        newrecipecarbs=request.form.get("newrecipecarbs")
        newproteins=request.form.get("protein")
        fat=request.form.get("fat")
        cholesterol=request.form.get("cholesterol")
        sodium=request.form.get("sodium")
        vitamina=request.form.get("vitamina")
        vitaminc=request.form.get("vitaminc")
        calcium=request.form.get("calcium")
        fiber=request.form.get("fiber")
        monounsaturated_fat=request.form.get("monounsaturated_fat")
        polyunsaturated_fat=request.form.get("polyunsaturated_fat")
        saturated_fat=request.form.get("saturated_fat")
        sugar=request.form.get("sugar")
        trans_fat=request.form.get("trans_fat")
        iron=request.form.get("iron")
        potassium=request.form.get("potassium")
        newrecipe=DataStructures.recipe_data()
        newrecipe["name"]=newrecipename
        newrecipe["ingredients"]=[newrecipeingredients]
        newrecipe["directions"]=[newrecipedirections]

        if(newrecipecalories!=None and newrecipecalories!=''):
            newrecipe["nutritional_values"]["calories"] = float(newrecipecalories)
        if(newrecipecarbs!=None and newrecipecarbs!=''):
            newrecipe["nutritional_values"]["carbohydrate"] = float(newrecipecarbs)
        if(newproteins!=None and newproteins!=''):
            newrecipe["nutritional_values"]["protein"] = float(newproteins)
        if(fat!=None and fat!=''):
            newrecipe["nutritional_values"]["fat"] = float(fat)
        if(cholesterol!=None and cholesterol!=''):
            newrecipe["nutritional_values"]["cholesterol"] = float(cholesterol)
        if(sodium!=None and sodium!=''):
            newrecipe["nutritional_values"]["sodium"] = float(sodium)
        if(vitamina!=None and vitamina!=''):
            newrecipe["nutritional_values"]["vitamin_a"] = float(vitamina)
        if(vitaminc!=None and vitaminc!=''):
            newrecipe["nutritional_values"]["vitamin_c"] = float(vitaminc)
        if(calcium!=None and calcium!=''):
            newrecipe["nutritional_values"]["calcium"] = float(calcium)
        if(fiber!=None and fiber!=''):
            newrecipe["nutritional_values"]["fiber"] = float(fiber)
        if(monounsaturated_fat!=None and monounsaturated_fat!=''):
            newrecipe["nutritional_values"]["monounsaturated_fat"] = float(monounsaturated_fat)
        if(polyunsaturated_fat!=None and polyunsaturated_fat!=''):
            newrecipe["nutritional_values"]["polyunsaturated_fat"] = float(polyunsaturated_fat)
        if(saturated_fat!=None and saturated_fat!=''):
            newrecipe["nutritional_values"]["saturated_fat"] = float(saturated_fat)
        if(trans_fat!=None and trans_fat!=''):
            newrecipe["nutritional_values"]["trans_fat"] = float(trans_fat)
        if(iron!=None and iron!=''):
            newrecipe["nutritional_values"]["iron"] = float(iron)
        if(sugar!=None and sugar!=''):
            newrecipe["nutritional_values"]["sugar"] = float(sugar)
        if(potassium!=None and potassium!=''):
            newrecipe["nutritional_values"]["potassium"] = float(potassium)
        
        if(numberofservings!='' and numberofservings!=None):
            newrecipe["number_of_servings"]=int(numberofservings)
        newrecipe["type"]=foodtype  
                                    #add newfoodrecipe to database
        return render_template("shoppinglist.html",jsonrecipe=newrecipe)
    


@app.route("/addexercise", methods=["GET", "POST"])
def addexercise():
    """This function takes user input to add an exercise to
    the database
    
    """
    if request.method == "POST":
           #getting new exericse to add to database
        name=request.form["name"]
        intensity=request.form["intensity"]
        sets=request.form["sets"]
        reps=request.form["reps"]
        selectedtargetmuscles = request.form.getlist("muscles")
        exercisedata=DataStructures.exercise()
        
        if(name!='' and name!=None):
            exercisedata["name"]=name
        if(intensity!='' and intensity!=None):
            exercisedata["level"]=int(intensity)
        if(sets!='' and sets!=None):
            exercisedata["sets"]=int(sets)
        if(reps!='' and reps!=None):
            exercisedata["reps"]=int(reps)
        exercisedata["targetmusclegroups"]=selectedtargetmuscles
        newexercise=json.dumps(exercisedata)
        newaddedexercise=json.loads(newexercise)     
                                                    #add exercise to database
        return render_template("shoppinglist.html",exercise=newaddedexercise,intensity=intensity,muscles=selectedtargetmuscles)



@app.route("/listitems", methods=["GET", "POST"])
def listitems():
    """This function takes user input to add a meal plan of recipes to
     the database
    
    """
    if request.method == "POST":
        mealplan=DataStructures.meal_plan()                                     #getting new mealplan to add to database
        newfoodname1=request.form.get("newfoodname1")
        newfoodingredients1=request.form.get("newfoodingredients1")
        newfooddirections1=request.form.get("newfooddirections1")
        newfood1numberofservings=request.form.get("newfood1numberofservings")
        newfood1type=request.form.get("newfood1type")

        newfoodcalories1=request.form.get("Calories1")
        newfoodcarbs1=request.form.get("Carbs1")
        newfoodproteins1=request.form.get("Proteins1")
        fat1=request.form.get("fats1")
        cholesterol1=request.form.get("cholesterols1")
        sodium1=request.form.get("sodiums1")
        vitamina1=request.form.get("vitamina1")
        vitaminc1=request.form.get("vitaminc1")
        calcium1=request.form.get("calciums1")
        fiber1=request.form.get("fiber1")
        monounsaturated_fat1=request.form.get("monounsaturated_fat1")
        polyunsaturated_fat1=request.form.get("polyunsaturated_fat1")
        saturated_fat1=request.form.get("saturated_fat1")
        sugar1=request.form.get("sugar1")
        trans_fat1=request.form.get("trans_fat1")
        iron1=request.form.get("iron1")
        potassium1=request.form.get("potassium1")
        newfood1=DataStructures.recipe_data()
        newfood1["name"]=newfoodname1
        newfood1["ingredients"]=[newfoodingredients1]
        newfood1["directions"]=[newfooddirections1]
        if(newfood1numberofservings!='' and newfood1numberofservings!=None):
            newfood1["number_of_servings"]=int(newfood1numberofservings)
        newfood1["type"]=newfood1type

        if(newfoodcalories1!=None and newfoodcalories1!=''):
            newfood1["nutritional_values"]["calories"] = float(newfoodcalories1)
        if(newfoodcarbs1!=None and newfoodcarbs1!=''):
            newfood1["nutritional_values"]["carbohydrate"] = float(newfoodcarbs1)
        if(newfoodproteins1!=None and newfoodproteins1!=''):
            newfood1["nutritional_values"]["protein"] = float(newfoodproteins1)
        if(fat1!=None and fat1!=''):
            newfood1["nutritional_values"]["fat"] = float(fat1)
        if(cholesterol1!=None and cholesterol1!=''):
            newfood1["nutritional_values"]["cholesterol"] = float(cholesterol1)
        if(sodium1!=None and sodium1!=''):
            newfood1["nutritional_values"]["sodium"] = float(sodium1)
        if(vitamina1!=None and vitamina1!=''):
            newfood1["nutritional_values"]["vitamin_a"] = float(vitamina1)
        if(vitaminc1!=None and vitaminc1!=''):
            newfood1["nutritional_values"]["vitamin_c"] = float(vitaminc1)
        if(calcium1!=None and calcium1!=''):
            newfood1["nutritional_values"]["calcium"] = float(calcium1)
        if(fiber1!=None and fiber1!=''):
            newfood1["nutritional_values"]["fiber"] = float(fiber1)
        if(monounsaturated_fat1!=None and monounsaturated_fat1!=''):
            newfood1["nutritional_values"]["monounsaturated_fat"] = float(monounsaturated_fat1)
        if(polyunsaturated_fat1!=None and polyunsaturated_fat1!=''):
            newfood1["nutritional_values"]["polyunsaturated_fat"] = float(polyunsaturated_fat1)
        if(saturated_fat1!=None and saturated_fat1!=''):
            newfood1["nutritional_values"]["saturated_fat"] = float(saturated_fat1)
        if(sugar1!=None and sugar1!=''):
            newfood1["nutritional_values"]["sugar"] = float(sugar1)
        if(trans_fat1!=None and trans_fat1!=''):
            newfood1["nutritional_values"]["trans_fat"] = float(trans_fat1)
        if(iron1!=None and iron1!=''):
            newfood1["nutritional_values"]["iron1"] = float(iron1)
        if(potassium1!=None and potassium1!=''):
            newfood1["nutritional_values"]["potassium"] = float(potassium1)
        
        mealplan[0]=json.dumps(newfood1)
        
        newfoodname2=request.form.get("newfoodname2")
        newfoodingredients2=request.form.get("newfoodingredients2")
        newfooddirections2=request.form.get("newfooddirections2")
        newfood2numberofservings=request.form.get("newfood2numberofservings")
        newfood2type=request.form.get("newfood2type")

        newfoodcalories2=request.form.get("Calories2")
        newfoodcarbs2=request.form.get("Carbs2")
        newfoodproteins2=request.form.get("Proteins2")
        fat2=request.form.get("fats2")
        cholesterol2=request.form.get("cholesterols2")
        sodium2=request.form.get("sodiums2")
        vitamina2=request.form.get("vitamina2")
        vitaminc2=request.form.get("vitaminc2")
        calcium2=request.form.get("calciums2")
        fiber2=request.form.get("fiber2")
        monounsaturated_fat2=request.form.get("monounsaturated_fat2")
        polyunsaturated_fat2=request.form.get("polyunsaturated_fat2")
        saturated_fat2=request.form.get("saturated_fat2")
        sugar2=request.form.get("sugar2")
        trans_fat2=request.form.get("trans_fat2")
        iron2=request.form.get("iron2")
        potassium2=request.form.get("potassium2")
        newfood2=DataStructures.recipe_data()
        newfood2["name"]=newfoodname2
        newfood2["ingredients"]=[newfoodingredients2]
        newfood2["directions"]=[newfooddirections2]
        if(newfood2numberofservings!='' and newfood2numberofservings!=None):
            newfood2["number_of_servings"]=int(newfood2numberofservings)
        newfood2["type"]=newfood2type

        if(newfoodcalories2!=None and newfoodcalories2!=''):
            newfood2["nutritional_values"]["calories"] = float(newfoodcalories2)
        if(newfoodcarbs2!=None and newfoodcarbs2!=''):
            newfood2["nutritional_values"]["carbohydrate"] = float(newfoodcarbs2)
        if(newfoodproteins2!=None and newfoodproteins2!=''):
            newfood2["nutritional_values"]["protein"] = float(newfoodproteins2)
        if(fat2!=None and fat2!=''):
            newfood2["nutritional_values"]["fat"] = float(fat2)
        if(cholesterol2!=None and cholesterol2!=''):
            newfood2["nutritional_values"]["cholesterol"] = float(cholesterol2)
        if(sodium2!=None and sodium2!=''):
            newfood2["nutritional_values"]["sodium"] = float(sodium2)
        if(vitamina2!=None and vitamina2!=''):
            newfood2["nutritional_values"]["vitamin_a"] = float(vitamina2)
        if(vitaminc2!=None and vitaminc2!=''):
            newfood2["nutritional_values"]["vitamin_c"] = float(vitaminc2)
        if(calcium2!=None and calcium2!=''):
            newfood2["nutritional_values"]["calcium"] = float(calcium2)
        if(fiber2!=None and fiber2!=''):
            newfood2["nutritional_values"]["fiber"] = float(fiber2)
        if(monounsaturated_fat2!=None and monounsaturated_fat2!=''):
            newfood2["nutritional_values"]["monounsaturated_fat"] = float(monounsaturated_fat2)
        if(polyunsaturated_fat2!=None and polyunsaturated_fat2!=''):
            newfood2["nutritional_values"]["polyunsaturated_fat"] = float(polyunsaturated_fat2)
        if(saturated_fat2!=None and saturated_fat2!=''):
            newfood2["nutritional_values"]["saturated_fat"] = float(saturated_fat2)
        if(sugar2!=None and sugar2!=''):
            newfood2["nutritional_values"]["sugar"] = float(sugar2)
        if(trans_fat2!=None and trans_fat2!=''):
            newfood1["nutritional_values"]["trans_fat"] = float(trans_fat2)
        if(iron2!=None and iron2!=''):
            newfood2["nutritional_values"]["iron1"] = float(iron2)
        if(potassium2!=None and potassium2!=''):
            newfood2["nutritional_values"]["potassium"] = float(potassium2)

        mealplan[1]=json.dumps(newfood2)
        
        newfoodname3=request.form.get("newfoodname3")
        newfoodingredients3=request.form.get("newfoodingredients3")
        newfooddirections3=request.form.get("newfooddirections3")
        newfood3numberofservings=request.form.get("newfood3numberofservings")
        newfood3type=request.form.get("newfood3type")

        newfoodcalories3=request.form.get("Calories3")
        newfoodcarbs3=request.form.get("Carbs3")
        newfoodproteins3=request.form.get("Proteins3")
        fat3=request.form.get("fats3")
        cholesterol3=request.form.get("cholesterols3")
        sodium3=request.form.get("sodiums3")
        vitamina3=request.form.get("vitamina3")
        vitaminc3=request.form.get("vitaminc3")
        calcium3=request.form.get("calciums3")
        fiber3=request.form.get("fiber3")
        monounsaturated_fat3=request.form.get("monounsaturated_fat3")
        polyunsaturated_fat3=request.form.get("polyunsaturated_fat3")
        saturated_fat3=request.form.get("saturated_fat3")
        sugar3=request.form.get("sugar3")
        trans_fat3=request.form.get("trans_fat3")
        iron3=request.form.get("iron3")
        potassium3=request.form.get("potassium3")
        newfood3=DataStructures.recipe_data()
        newfood3["name"]=newfoodname3
        newfood3["ingredients"]=[newfoodingredients3]
        newfood3["directions"]=[newfooddirections3]
        if(newfood3numberofservings!='' and newfood3numberofservings!=None):
            newfood3["number_of_servings"]=int(newfood3numberofservings)
        newfood3["type"]=newfood3type

        if(newfoodcalories3!=None and newfoodcalories3!=''):
            newfood3["nutritional_values"]["calories"] = float(newfoodcalories3)
        if(newfoodcarbs3!=None and newfoodcarbs3!=''):
            newfood3["nutritional_values"]["carbohydrate"] = float(newfoodcarbs3)
        if(newfoodproteins3!=None and newfoodproteins3!=''):
            newfood3["nutritional_values"]["protein"] = float(newfoodproteins3)
        if(fat3!=None and fat3!=''):
            newfood3["nutritional_values"]["fat"] = float(fat3)
        if(cholesterol3!=None and cholesterol3!=''):
            newfood3["nutritional_values"]["cholesterol"] = float(cholesterol3)
        if(sodium3!=None and sodium3!=''):
            newfood3["nutritional_values"]["sodium"] = float(sodium3)
        if(vitamina3!=None and vitamina3!=''):
            newfood3["nutritional_values"]["vitamin_a"] = float(vitamina3)
        if(vitaminc3!=None and vitaminc3!=''):
            newfood3["nutritional_values"]["vitamin_c"] = float(vitaminc3)
        if(calcium3!=None and calcium3!=''):
            newfood3["nutritional_values"]["calcium"] = float(calcium3)
        if(fiber3!=None and fiber3!=''):
            newfood3["nutritional_values"]["fiber"] = float(fiber3)
        if(monounsaturated_fat3!=None and monounsaturated_fat3!=''):
            newfood3["nutritional_values"]["monounsaturated_fat"] = float(monounsaturated_fat3)
        if(polyunsaturated_fat3!=None and polyunsaturated_fat3!=''):
            newfood3["nutritional_values"]["polyunsaturated_fat"] = float(polyunsaturated_fat3)
        if(saturated_fat3!=None and saturated_fat3!=''):
            newfood3["nutritional_values"]["saturated_fat"] = float(saturated_fat3)
        if(sugar3!=None and sugar3!=''):
            newfood3["nutritional_values"]["sugar"] = float(sugar3)
        if(trans_fat3!=None and trans_fat3!=''):
            newfood1["nutritional_values"]["trans_fat"] = float(trans_fat3)
        if(iron3!=None and iron3!=''):
            newfood3["nutritional_values"]["iron1"] = float(iron3)
        if(potassium3!=None and potassium3!=''):
            newfood3["nutritional_values"]["potassium"] = float(potassium3)
        mealplan[2]=json.dumps(newfood3)
    
    
        
        
       
        
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
