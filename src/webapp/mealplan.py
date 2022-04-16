import itertools
import json
import math
import os
import random
import sys
import fractions
import copy

from numpy import poly

from webapp import data_src
from webapp.data_src import DataStructures
from webapp.models import Recipes, User, db


# TODO: make this actually connect to a DB and pull recipes. Might need to add inputs to do a preliminary filtering of the DB first.
# Idea for DB source: https://www.fatsecret.com/calories-nutrition/search?q=(encoded string)
# This returns an array of JSON strings. Do we instead want one giant json string? Good question.
def get_recipes_from_db(
    Calories_max=9999,
    Calories_min=0,
    Carbs_max=9999,
    Carbs_min=0,
    Proteins_max=9999,
    Proteins_min=0,
):
    recipes = []

    queried_recipes = Recipes.query.filter(
        Recipes.calories > Calories_min,
        Recipes.calories < Calories_max,
        Recipes.carbohydrate > Carbs_min,
        Recipes.carbohydrate < Carbs_max,
        Recipes.protein > Proteins_min,
        Recipes.protein < Proteins_max,
    )

    for recipe in queried_recipes:
        skeleton = DataStructures.recipe_data()
        skeleton["name"] = recipe.name
        skeleton["ingredients"] = json.loads(recipe.ingredients)
        skeleton["directions"] = json.loads(recipe.directions)
        skeleton["nutritional_values"]["calcium"] = recipe.calcium
        skeleton["nutritional_values"]["calories"] = recipe.calories
        skeleton["nutritional_values"]["carbohydrate"] = recipe.carbohydrate
        skeleton["nutritional_values"]["cholesterol"] = recipe.cholesterol
        skeleton["nutritional_values"]["fat"] = recipe.fat
        skeleton["nutritional_values"]["fiber"] = recipe.fiber
        skeleton["nutritional_values"]["iron"] = recipe.iron
        skeleton["nutritional_values"][
            "monounsaturated_fat"] = recipe.monounsaturated_fat
        skeleton["nutritional_values"][
            "polyunsaturated_fat"] = recipe.polyunsaturated_fat
        skeleton["nutritional_values"]["potassium"] = recipe.potassium
        skeleton["nutritional_values"]["protein"] = recipe.protein
        skeleton["nutritional_values"]["saturated_fat"] = recipe.saturated_fat
        skeleton["nutritional_values"]["sodium"] = recipe.sodium
        skeleton["nutritional_values"]["sugar"] = recipe.sugar
        skeleton["nutritional_values"]["trans_fat"] = recipe.trans_fat
        skeleton["nutritional_values"]["vitamin_a"] = recipe.vitamin_a
        skeleton["nutritional_values"]["vitamin_c"] = recipe.vitamin_c
        skeleton["type"] = json.loads(recipe.type)
        skeleton["number_of_servings"] = recipe.number_of_servings
        recipes.append(json.dumps(skeleton))

    return recipes


def save_mealplan(email: str, mealplan: DataStructures.mealplan) -> DataStructures.meal_plan:
    user = User.query.filter_by(email=email).first()

    if user:
        user.add_mealplan(json.dumps(mealplan))
    return mealplan

def get_mealplan(email: str)-> DataStructures.meal_plan:
    user = User.query.filter_by(email=email).first()

    if user:
        mealplan = user.get_mealplan()
    return mealplan

def add_recipe(
            name: str, 
            directions: list, 
            ingredients: list,
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
            calcium=0.0,
            saturated_fat=0.0,
            sodium=0.0,
            sugar=0.0,
            trans_fat=0.0,
            vitamin_a=0.0,
            vitamin_c=0.0,
            number_of_servings=0,
            type=[]):
    new_recipe = Recipes(
                        name, 
                        directions, 
                        ingredients,
                        calories,
                        carbohydrate,
                        protein,
                        cholesterol,
                        fat,
                        fiber,
                        iron,
                        monounsaturated_fat,
                        polyunsaturated_fat,
                        potassium,
                        calcium,
                        saturated_fat,
                        sodium,
                        sugar,
                        trans_fat,
                        vitamin_a,
                        vitamin_c,
                        number_of_servings,
                        type)
    db.session.add(new_recipe)
    db.session.commit()
    

class MealplanGenerator(data_src.DataStructures):
    recipes = []
    breakfasts = []
    lunches = []
    main_dishes = []
    side_dishes = []
    snacks = []  # leave for now
    user_health_requirements = None
    calorie_split = [0.25, 0.25, 0.5]
    protein_split = [0.25, 0.25, 0.5]
    carbs_split = [0.25, 0.25, 0.5]

    def __init__(self,
                 json_health_requirements,
                 json_splits = 
                '{"calorie_split": [0.25, 0.25, 0.5], "protein_split": [0.25, 0.25, 0.5], "carbs_split": [0.25, 0.25, 0.5]}'
                 ):
        """Plan Meals for Week Usecase

        Big paragraph
        in: user constraints
        out: suggested match

        queries recipes from DB
        """
        # Can be done in get_recipes_from_db()
        json_recipes = get_recipes_from_db()
        for i in json_recipes:
            j = json.loads(i)
            self.recipes.append(j)
            for k in j["type"]:
                if k == "Breakfast":
                    self.breakfasts.append(j)
                if k == "Lunch":
                    self.lunches.append(j)
                if k == "Main Dish":
                    self.main_dishes.append(j)
                if k == "Side Dish":
                    self.side_dishes.append(j)
                if k == "Snack":
                    self.snacks.append(j)

        self.user_health_requirements = json.loads(json_health_requirements)
        splits = json.loads(json_splits)
        calorie_split = splits['calorie_split']
        protein_split = splits['protein_split']
        carbs_split = splits['carbs_split']
            

    def _sum_nutritional_values(self, n1, n2):
        """Adds two nutritional value datastructures

        Adds the values of two nutritional value datastructures into a third datastructure
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

    def _diff_nutritional_values(self, n1, n2):
        """Subtracts two nutritional value datastructures

        This function subtracts two dicts containing nutritional values, and returns their value in a third dict.
        Paramaters:
        n1 (dict): nutritional values
        n2 (dict): nutritional values
        Returns:
        dict: difference of n1 and n2
        """
        n3 = dict(n1)
        for i in n1:
            n3[i] -= n2[i]
        return n3

    def _mul_nutritional_values(self, n1, n2):
        """Multiply a nutritional value datastructure by a scalar value

        This function multiplies all values in a dict containing nutritional values by a scalar value
        Paramaters:
        n1 (dict): nutritional values
        n2 (int/float): scalar to multipy by 
        Returns:
        dict: n1*n2
        """
        n3 = dict(n1)
        for i in n1:
            n3[i] *= n2
        return n3

    def _calculate_meal_plan_nutrition(self, recipes):
        """Calculates the total nutrition of a mealplan

        This function calculates the sum of the nutrition values for an array of recipes, i.e. if you
        ate all these recipes what nutrition would you get
        Paramaters:
        recipes (list): array of recipe objects
        Returns: dict: sum of all nutritional datas in recipe
        """
        nutrition_data = DataStructures.nutritional_values()
        for i in recipes:
            nutrition_data = self._sum_nutritional_values(
                nutrition_data, i["nutritional_values"])
        return nutrition_data

    def _meal_plan_RSS(self, health_requirements, meal_plan):
        """Calculates the RSS for a mealplan wrt health reqs
        Calculates the RSS (residual sum of squares) for a mealplan with regards to health requirements
        """
        RSS = 0
        for i in meal_plan:
            RSS += self._recipe_RSS(health_requirements, i)
        RSS /= len(meal_plan)
        return RSS

    def _recipe_RSS(self, health_requirements, recipe_data):
        """Calculates the RSS for a recipe wrt health reqs
        Calculates the RSS (residual sum of squares) for a recipe with regards to health requirements
        """
        return self._nutritional_values_RSS(health_requirements, recipe_data["nutritional_values"])

    def _nutritional_values_RSS(self, health_requirements, nutritional_values):
        """Calculates the RSS for a set of nutritional values wrt health reqs
        Calculates the RSS (residual sum of squares) for a set of nutritional values with regards to health requirements
        """
        # TODO: data scaling; otherwise an error in calories will matter a lot more than an error in vitamin A
        RSS = 0
        offset = self._diff_nutritional_values(health_requirements,
                                               nutritional_values)
        for j in offset:
            RSS += offset[j]**2
        return RSS/len(nutritional_values)

    def _balance_health_requirements(self, calorie_split, protein_split, carbs_split, health_requirements):
        hr_breakfast = self._mul_nutritional_values(health_requirements, carbs_split[0])
        hr_lunch = self._mul_nutritional_values(health_requirements, carbs_split[1])
        hr_dinner = self._mul_nutritional_values(health_requirements, carbs_split[2])
        avg_split = [
                (calorie_split[0] + protein_split[0] + carbs_split[0]) / 3,
                (calorie_split[1] + protein_split[1] + carbs_split[1]) / 3,
                (calorie_split[2] + protein_split[2] + carbs_split[2]) / 3
                ]

        hr_breakfast["calories"] = health_requirements["calories"] * calorie_split[0]
        hr_breakfast["protein"] = health_requirements["protein"] * protein_split[0]
        hr_breakfast["iron"] = health_requirements["iron"] * avg_split[0]
        hr_breakfast["vitamin_a"] = health_requirements["vitamin_a"] * avg_split[0]
        hr_breakfast["vitamin_c"] = health_requirements["vitamin_c"] * avg_split[0]

        hr_lunch["calories"] = health_requirements["calories"] * calorie_split[1]
        hr_lunch["protein"] = health_requirements["protein"] * protein_split[1]
        hr_lunch["iron"] = health_requirements["iron"] * avg_split[0]
        hr_lunch["vitamin_a"] = health_requirements["vitamin_a"] * avg_split[0]
        hr_lunch["vitamin_c"] = health_requirements["vitamin_c"] * avg_split[0]

        hr_dinner["calories"] = health_requirements["calories"] * calorie_split[2]
        hr_dinner["protein"] = health_requirements["protein"] * protein_split[2]
        hr_dinner["iron"] = health_requirements["iron"] * avg_split[0]
        hr_dinner["vitamin_a"] = health_requirements["vitamin_a"] * avg_split[0]
        hr_dinner["vitamin_c"] = health_requirements["vitamin_c"] * avg_split[0]

        return hr_breakfast, hr_lunch, hr_dinner
    
    def _scale_recipe(self, recipe, scale):
        for idx in range(len(recipe["ingredients"])):
            i = recipe["ingredients"][idx]
            str_value = i.split(' ')[0]
            rest_of_str = i[len(str_value):]
            fraction = fractions.Fraction(0, 1)
            if not str_value.replace('.','',1).isdigit() and not str_value.replace('/', '', 1).isdigit(): #not a number
                continue
            else:
                fraction = fractions.Fraction(str_value) #works for fractions, decimals, and ints
                fraction *= scale
                recipe["ingredients"][idx] = str(fraction) + rest_of_str
        recipe["number_of_servings"] = float(recipe["number_of_servings"] * scale)


    # this is the "head" of the code
    def gen_meal_plan(self) -> DataStructures.meal_plan:
        """Generates a mealplan based on the health requirements that the class was created with

        For each of 3 meals, picks the meal option that best matches the user's desired intake for that meal.
        Put each of the best meals together to generate a mealplan

        TODO: add snacks to lower mealplan RSS
        """
        best_meal_plan: DataStructures.meal_plan
        best_meal_plan = DataStructures.meal_plan(4)

        # TODO
        # Ability to add arbitrary # of snacks (favor coming at the RSS from the low end? Third slider so they can say how much they wanna snack?)
        # Ability to deduce which meal should be composed of main + side dish and which meal should be just a lunch
        # Figure out how to store both servings that recipe makes and how many of those to eat
        # Eliminate duplicate meals in day (or at least control for them -> total # of servings made == over the course of the week; maybe scale ingredients?)

        breakfast_reqs, lunch_reqs, dinner_reqs = self._balance_health_requirements(self.calorie_split, self.protein_split, self.carbs_split, self.user_health_requirements)

        lowest_RSS = math.inf
        for i in self.breakfasts:
            for n in range(1, 5):
                cur_RSS = self._nutritional_values_RSS(breakfast_reqs, self._mul_nutritional_values(i["nutritional_values"], n))
                if cur_RSS < lowest_RSS:
                    lowest_RSS = cur_RSS
                    self._scale_recipe(i, fractions.Fraction(n,fractions.Fraction(i["number_of_servings"])))
                    i["nutritional_values"] = self._mul_nutritional_values(i["nutritional_values"], n)
                    best_meal_plan[0] = i

        lowest_RSS = math.inf
        for i in self.lunches:
            for n in range(1, 5):
                cur_RSS = self._nutritional_values_RSS(lunch_reqs, self._mul_nutritional_values(i["nutritional_values"], n))
                if cur_RSS < lowest_RSS:
                    lowest_RSS = cur_RSS
                    self._scale_recipe(i, fractions.Fraction(n,fractions.Fraction(i["number_of_servings"])))
                    i["nutritional_values"] = self._mul_nutritional_values(i["nutritional_values"], n)
                    best_meal_plan[1] = i

        lowest_RSS = math.inf
        for i in self.main_dishes:
            for j in self.side_dishes:
                for n in range(1, 5):
                    cur_RSS = self._nutritional_values_RSS(dinner_reqs, self._mul_nutritional_values(self._sum_nutritional_values(i["nutritional_values"], j["nutritional_values"]), n))
                    if cur_RSS < lowest_RSS:
                        lowest_RSS = cur_RSS
                        self._scale_recipe(i, fractions.Fraction(n,fractions.Fraction(i["number_of_servings"])))
                        self._scale_recipe(j, fractions.Fraction(n,fractions.Fraction(j["number_of_servings"])))
                        i["nutritional_values"] = self._mul_nutritional_values(i["nutritional_values"], n)
                        j["nutritional_values"] = self._mul_nutritional_values(j["nutritional_values"], n)
                        best_meal_plan[2] = i
                        best_meal_plan[3] = j


        missing_nutrition = self._diff_nutritional_values(
                self.user_health_requirements,
                self._calculate_meal_plan_nutrition(best_meal_plan))

#       best_meal_plan_with_snacks = copy.deepcopy(best_meal_plan)
#       while True:
#           lowest_RSS = self._nutritional_values_RSS(missing_nutrition, DataStructures.nutritional_values())
#           best_snack = None
#           for i in self.snacks:
#               cur_RSS = self._nutritional_values_RSS(missing_nutrition, i["nutritional_values"])
#               if cur_RSS < lowest_RSS: #adding this snack is better
#                   best_snack = i
#                   lowest_RSS = cur_RSS
#           if best_snack == None: #no snacks were better than None
#               break
#           best_meal_plan_with_snacks.append(best_snack)

        return json.dumps(best_meal_plan)