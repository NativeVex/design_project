import os
import sys
import json
from flaskr import data_src
import itertools
import random


#TODO: make this actually connect to a DB and pull recipes. Might need to add inputs to do a preliminary filtering of the DB first.
#Idea for DB source: https://www.fatsecret.com/calories-nutrition/search?q=(encoded string)
#This returns an array of JSON strings. Do we instead want one giant json string? Good question.
def get_recipes_from_db():
    #Hard coded recipes for now
    recipes = []
    recipes.append('{"name":"Chicken Parm","ingredients":["Chicken","Parmesan"],"nutritional value":{"calories":254,"carbs":12.18,"protein":22.83,"fat":12.38,"cholesterol":108,"sodium":615,"vitaminA":66,"vitaminB1":0,"vitaminB2":0,"vitaminB3":0,"vitaminB5":0,"vitaminB6":0,"vitaminB9":0,"vitaminB12":0,"vitaminC":4.7,"vitaminD":0,"vitaminE":0,"vitaminK":0,"calcium":145,"copper":0,"fluoride":0,"iodine":0,"iron":1.9,"magnesium":0,"manganese":0,"molybdenum":0,"phosphorus":0,"potassium":353,"selenium":0,"zinc":0}}')

    adobo_chicken = data_src.recipe_data()
    adobo_chicken["name"] = "Adobo Chicken"
    adobo_chicken["ingredients"] = ["Chicken", "Adobo Sauce"]
    adobo_chicken["nutritional value"]["calories"] = 107
    adobo_chicken["nutritional value"]["fat"] = 4.93
    adobo_chicken["nutritional value"]["carbs"] = 2.48
    adobo_chicken["nutritional value"]["protein"] = 11.88
    adobo_chicken["nutritional value"]["sodium"] = 392
    adobo_chicken["nutritional value"]["vitaminA"] = 9
    adobo_chicken["nutritional value"]["vitaminC"] = 0.5
    adobo_chicken["nutritional value"]["calcium"] = 14
    adobo_chicken["nutritional value"]["iron"] = 1.05
    adobo_chicken["nutritional value"]["potassium"] = 147
    recipes.append(json.dumps(adobo_chicken))

    ice_cream_sandwich = data_src.recipe_data()
    ice_cream_sandwich["name"] = "Ice Cream Sandwich"
    ice_cream_sandwich["ingredients"] = ["Ice", "Cream", "Sandwich"]
    ice_cream_sandwich["nutritional value"]["calories"] = 143
    ice_cream_sandwich["nutritional value"]["fat"] = 5.6
    ice_cream_sandwich["nutritional value"]["carbs"] = 21.75
    ice_cream_sandwich["nutritional value"]["protein"] = 2.61
    ice_cream_sandwich["nutritional value"]["cholesterol"] = 20
    ice_cream_sandwich["nutritional value"]["sodium"] = 37
    ice_cream_sandwich["nutritional value"]["vitaminA"] = 53
    ice_cream_sandwich["nutritional value"]["vitaminC"] = 0.3
    ice_cream_sandwich["nutritional value"]["calcium"] = 60
    ice_cream_sandwich["nutritional value"]["iron"] = 0.28
    ice_cream_sandwich["nutritional value"]["potassium"] = 122
    ice_cream_sandwich["nutritional value"]
    recipes.append(json.dumps(ice_cream_sandwich))

    the_void = data_src.recipe_data()
    the_void["name"] = "The Void"
    recipes.append(json.dumps(the_void))
    return recipes

def sum_nutritional_values(n1, n2):
    """
    This function adds two dicts containing nutritional values, and returns their value in a third dict.
    Paramaters:
    n1 (dict): nutritional values
    n2 (dict): nutritional values
    Returns:
    dict: sum of n1 and n2
    """
    n3 = dict(n1)
    for i in n1:
        n3[i] += n2[i]
    return n3

def diff_nutritional_values(n1, n2):
    """
    This function subtracts two dicts containing nutritional values, and returns their value in a third dict.
    Paramaters:
    n1 (dict): nutritional values
    n2 (dict): nutritional values
    Returns:
    dict: difference of n1 and n2
    """
    n3 = dict(n1)
    for i in n1:
        print(i)
        n3[i] -= n2[i]
    return n3


def calculate_meal_plan_nutrition(recipes):
    """This function calculates the sum of the nutrition values for an array of recipes, i.e. if you
    ate all these recipes what nutrition would you get
    Paramaters:
    recipes (list): array of recipe objects
    Returns: dict: sum of all nutritional datas in recipe
    """
    nutrition_data = data_src.nutritional_values()
    for i in recipes:
        nutrition_data = sum_nutritional_values(nutrition_data, i["nutritional value"])
    return nutrition_data

def meal_plan_RSS(health_requirements, meal_plan):
    #TODO: data scaling; otherwise an error in calories will matter a lot more than an error in vitamin A
    RSS = 0
    for i in meal_plan:
        offset = diff_nutritional_values(health_requirements, i["nutritional value"])
        for j in offset:
            RSS += offset[j]**2
    return RSS
    #if we want some randomness so it doesn't always spit out the same meal plan we can uncomment and/or change the following line
    #RSS += random.random() * 2


#this is the "head" of the code
def gen_meal_plan(json_health_requirements, json_recipes):
#   print(json_health_requirements)
    available_recipes = []
    best_meal_plan = 0

    health_requirements = json.loads(json_health_requirements)

    #### If we change the get_recipes_from_db output to share one giant JSON string then life gets easier.
    for i in json_recipes:
        available_recipes.append(json.loads(i))
    #### END of the weird JSON array thingy.


    #n choose k reqs. For this proof of concept n is number of recipes and k is 3. Thus there are 
    # n! / (k!(n-k)!) answers. This is obviously impossible to compute for any significant number of recipes.
    #Thus, we need to do some form of optimization. Open to suggestions but for now our dataset is small so we can just do this.
    
    #We can assess the quality of a meal plan given the RSS of the meal plan wrt the reqs. With this we can compare
    #two meal plans and pick the better one.
    meals_per_meal_plan = 3
    possible_meal_plans_iterator = itertools.combinations(available_recipes, meals_per_meal_plan)

    #print all possible meal plans
    lowest_RSS = 1000000000000
    for i in possible_meal_plans_iterator:
        current_meal_plan_RSS = meal_plan_RSS(health_requirements, i)
        if (current_meal_plan_RSS < lowest_RSS):
            lowest_RSS = current_meal_plan_RSS
            best_meal_plan = i
#       for j in range(meals_per_meal_plan): 
#           print(i[j]["name"])
#       print("===")

    return json.dumps(best_meal_plan)

#this is one usecase
def mealplan(json_health_requirements):
    return gen_meal_plan(json_health_requirements, get_recipes_from_db())
