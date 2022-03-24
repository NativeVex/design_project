import json
from random import randint
from time import strftime
from flask import Flask, jsonify, redirect, render_template, flash, request, session, url_for
from wtforms import Form, StringField, validators, StringField, SubmitField

from flaskr.data_src import DataStructures
from flaskr.mealplan import MealplanGenerator
from flaskr.exerciseplan import get_exercises_from_db

app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '5e4c0f48eef083bde520ef8027eb12e3f8bafcc763969d58'

class signupform(Form):
    email = StringField('Email:', validators=[validators.DataRequired()])
    username = StringField('Username:', validators=[validators.DataRequired()])
    password = StringField('Password:', validators=[validators.DataRequired()])

class loginform(Form):
    username = StringField('Carbs:', validators=[validators.DataRequired()])
    password = StringField('Proteins:', validators=[validators.DataRequired()])
   
class dietform(Form):
    Calories = StringField('Calories:', validators=[validators.DataRequired()])
    Carbs = StringField('Carbs:', validators=[validators.DataRequired()])
    Proteins = StringField('Proteins:', validators=[validators.DataRequired()])
    Fibers = StringField('Fibers:', validators=[validators.DataRequired()])
    Allergies = StringField('Allergies:', validators=[validators.DataRequired()])


@app.route("/login",methods = ['GET', 'POST'])
def login():
    userloginform = loginform(request.form)
    if request.method == 'POST':
      session['username'] = request.form['username']
      return redirect(url_for('diet'))
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
   session.pop('username', None)   #removes session username
   return redirect(url_for('login'))

@app.route("/points/")
def points():
    return render_template('points.html')

@app.route("/saveduserinfo/")
def saveduserinfo():
    return render_template('saveduserinfo.html')

@app.route("/signup/")
def signup():
    usersignupform = signupform(request.form)
    if request.method == 'POST':
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
    return render_template('signup.html')

@app.route('/diet/', methods=['GET', 'POST'])
def diet():
    form = dietform(request.form)
    if request.method == 'POST':
        Calories=request.form['Calories']
        Carbs=request.form['Carbs']
        Proteins=request.form['Proteins']
        Fibers=request.form['Fibers']
        Allergies=request.form['Allergies']

        if form.validate():
            if(int(Calories)<0 or int(Carbs)<0 or int(Proteins)<0 or int(Fibers)<0):
                flash('Error: No negative numbers allowed')
            else:
                flash('You entered this many calories: {}'.format(Calories))

        else:
            flash('Error: All Fields are Required')

    return render_template('mealplanner.html', form=form)


@app.route('/mealplan', methods=['GET','POST'])
def mealplan():
    if request.method == 'POST':
        Calories=request.form.get("Calories")
        Carbs=request.form.get("Carbs")
        protein=request.form.get("Proteins")
        list1=[1,2,3]

        jsoninfo = DataStructures.nutritional_values()
        jsoninfo["calories"] = int(Calories)
        jsoninfo["carbs"] = int(Carbs)
        jsoninfo["protein"] = int(protein)
        jsonstring = json.dumps(jsoninfo)
        mpg = MealplanGenerator(jsonstring)
        mealplan = mpg.gen_meal_plan()
        jsondata=json.loads(mealplan)
        return render_template("mealplans.html", bestmealplan=jsondata)
    elif request.method == 'GET':
        return render_template('mealplans.html')

    
        
            
@app.route('/savemealplan', methods=['POST'])
def savemealplan():
    
    if request.method == 'POST':
        bestmealplan = request.form['bestmealplan']
        mealplan=bestmealplan.replace("'",'"')   #replacing single quotes with double quotes to change string to json format
        newmealplan=json.loads(mealplan)
        return render_template("saveduserinfo.html", bestmealplan=newmealplan)

@app.route('/saveexerciseplan', methods=['POST'])
def saveexerciseplan():
    
    if request.method == 'POST':
        bestexerciseplan = request.form['bestexerciseplan']
        exerciseplan=bestexerciseplan.replace("'",'"')   #replacing single quotes with double quotes to change string to json format
        newexerciseplan=json.loads(exerciseplan)
        return render_template("saveduserinfo.html", bestexerciseplan=newexerciseplan)




@app.route('/exerciseplan', methods=['GET','POST'])
def exerciseplan():
    if request.method == 'POST':
        duration=request.form.get("duration")
        intensity=request.form.get("intensity")
        frequency=request.form.get("frequency")
        list1=[1,2,3]

        jsonexercises=get_exercises_from_db()
        jsonexerciseplan=json.loads(jsonexercises)
        return render_template("exerciseplan.html", bestexerciseplan=jsonexerciseplan)
    elif request.method == 'GET':
        return render_template('exerciseplan.html')


class foodsform(Form):
        newfood = StringField('Food:', validators=[validators.DataRequired()])

@app.route('/listitems/')
def listitems():
    #get shopping list ingredients for meal plan from database 
    return render_template('shoppinglist.html')



class exerciseform(Form):
    duration = StringField('duration:', validators=[validators.DataRequired()])
    intensity = StringField('intensity:', validators=[validators.DataRequired()])
    frequency = StringField('frequency:', validators=[validators.DataRequired()])
    musclegroups = StringField('musclegroups:', validators=[validators.DataRequired()])

@app.route('/exercises/', methods=['GET', 'POST'])
def exercises():
    otherform = exerciseform(request.form)
    if request.method == 'POST':
        duration=request.form['duration']
        intensity=request.form['intensity']
        frequency=request.form['frequency']
        musclegroups=request.form['musclegroups']

        if otherform.validate():
            if(int(duration)<0 or int(frequency)<0):
                flash('Error: No negative numbers allowed')
            else:
                flash('You entered this much duration: {}'.format(duration))

        else:
            flash('Error: All Fields are Required')

    return render_template('exercises.html', form=otherform)

if __name__ == "__main__":
    app.run()




