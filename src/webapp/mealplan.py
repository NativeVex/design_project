import itertools
import json
import math
import os
import random
import sys

from webapp import data_src
from webapp.data_src import DataStructures
from webapp.models import Recipes


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

    # MOCK CODE
    with open("r2.json") as r:
        for recipe in r:
            fixme = json.loads(recipe.strip())
            for i in fixme["nutritional_values"]:
                fixme["nutritional_values"][i] = float(
                    fixme["nutritional_values"][i])
            recipes.append(json.dumps(fixme))
    return recipes
    # END MOCK CODE

    queried_recipes = Recipes.query.filter(
        Recipes.Calories > Calories_min,
        Recipes.Calories < Calories_max,
        Recipes.Carbs > Carbs_min,
        Recipes.Carbs < Carbs_max,
        Recipes.Proteins > Proteins_min,
        Recipes.Proteins < Proteins_max,
    )

    for recipe in queried_recipes:
        skeleton = DataStructures.recipe_data()
        skeleton["name"] = recipe.name
        skeleton["nutritional value"]["calcium"] = recipe.calcium
        skeleton["nutritional value"]["calories"] = recipe.calories
        skeleton["nutritional value"]["carbohydrate"] = recipe.carbohydrate
        skeleton["nutritional value"]["cholesterol"] = recipe.cholesterol
        skeleton["nutritional value"]["fat"] = recipe.fat
        skeleton["nutritional value"]["fiber"] = recipe.fiber
        skeleton["nutritional value"]["iron"] = recipe.iron
        skeleton["nutritional value"][
            "monounsaturated_fat"] = recipe.monounsaturated_fat
        skeleton["nutritional value"][
            "polyunsaturated_fat"] = recipe.polyunsaturated_fat
        skeleton["nutritional value"]["potassium"] = recipe.potassium
        skeleton["nutritional value"]["protein"] = recipe.protein
        skeleton["nutritional value"]["saturated_fat"] = recipe.saturated_fat
        skeleton["nutritional value"]["sodium"] = recipe.sodium
        skeleton["nutritional value"]["sugar"] = recipe.sugar
        skeleton["nutritional value"]["trans_fat"] = recipe.trans_fat
        skeleton["nutritional value"]["vitamin_a"] = recipe.vitamin_a
        skeleton["nutritional value"]["vitamin_c"] = recipe.vitamin_c
        skeleton["nutritional value"]["type"] = recipe.type
        recipes.append(json.dumps(skeleton))

    the_void = DataStructures.recipe_data()
    the_void["name"] = "The Void"
    recipes.append(json.dumps(the_void))
    return recipes


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
                 json_splits):
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
        # TODO: data scaling; otherwise an error in calories will matter a lot more than an error in vitamin A
        RSS = 0
        for i in meal_plan:
            offset = self._diff_nutritional_values(health_requirements,
                                                   i["nutritional_values"])
            for j in offset:
                RSS += offset[j]**2
        return (RSS/len(meal_plan))/len(meal_plan[0]["nutritional_values"])
        # if we want some randomness so it doesn't always spit out the same meal plan we can uncomment and/or change the following line
        # RSS += random.random() * 2

    def _recipe_RSS(self, health_requirements, recipe_data):
        RSS = 0
        offset = self._diff_nutritional_values(
            health_requirements, recipe_data["nutritional_values"])
        for j in offset:
            RSS += offset[j]**2
        return RSS/len(recipe_data["nutritional_values"])

    def _nutritional_values_RSS(self, health_requirements, nutritional_values):
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
        hr_breakfast["protein"] = health_requirements["protein"] * calorie_split[0]
        hr_breakfast["iron"] = health_requirements["iron"] * avg_split[0]
        hr_breakfast["vitamin_a"] = health_requirements["vitamin_a"] * avg_split[0]
        hr_breakfast["vitamin_c"] = health_requirements["vitamin_c"] * avg_split[0]

        hr_lunch["calories"] = health_requirements["calories"] * calorie_split[1]
        hr_lunch["protein"] = health_requirements["protein"] * calorie_split[1]
        hr_lunch["iron"] = health_requirements["iron"] * avg_split[0]
        hr_lunch["vitamin_a"] = health_requirements["vitamin_a"] * avg_split[0]
        hr_lunch["vitamin_c"] = health_requirements["vitamin_c"] * avg_split[0]

        hr_dinner["calories"] = health_requirements["calories"] * calorie_split[2]
        hr_dinner["protein"] = health_requirements["protein"] * calorie_split[2]
        hr_dinner["iron"] = health_requirements["iron"] * avg_split[0]
        hr_dinner["vitamin_a"] = health_requirements["vitamin_a"] * avg_split[0]
        hr_dinner["vitamin_c"] = health_requirements["vitamin_c"] * avg_split[0]

        return hr_breakfast, hr_lunch, hr_dinner
    
    def _scale_recipe(self, recipe, scale):
        for idx in range(len(recipe["ingredients"])):
            i = recipe["ingredients"][idx]
            str_value = i.split(' ')[0]
            rest_of_str = i[len(str_value):]
            float_value = 0.0
            if '/' in str_value:
                frac = str_value.split('/')
                float_value = int(frac[0])/int(frac[1])
                float_value *= scale
            else:
                float_value = float(str_value) * scale
            recipe["ingredients"][idx] = str(float_value) + rest_of_str
        recipe["number_of_servings"] *= scale


    # this is the "head" of the code
    def gen_meal_plan(self) -> DataStructures.meal_plan:
        """Generates a mealplan based on the health requirements that the class was created with

        Creates n choose k different mealplans based on recipes gotten from DB, then calculates the
        RSS of each of these wrt the user's heatlh requirements. Returns the best mealplan, with the
        lowest RSS
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
                    i["number_of_servings"] /= n #Assume we get 0.66 servings here. Scale the recipe to make it 1
                    self._scale_recipe(i, 1/i["number_of_servings"])
                    i["nutritional_values"] = self._mul_nutritional_values(i["nutritional_values"], n)
                    best_meal_plan[0] = i

        lowest_RSS = math.inf
        for i in self.lunches:
            for n in range(1, 5):
                cur_RSS = self._nutritional_values_RSS(lunch_reqs, self._mul_nutritional_values(i["nutritional_values"], n))
                if cur_RSS < lowest_RSS:
                    lowest_RSS = cur_RSS
                    i["number_of_servings"] /= n
                    self._scale_recipe(i, 1/i["number_of_servings"])
                    i["nutritional_values"] = self._mul_nutritional_values(i["nutritional_values"], n)
                    best_meal_plan[1] = i

        lowest_RSS = math.inf
        for i in self.main_dishes:
            for j in self.side_dishes:
                for n in range(1, 5):
                    cur_RSS = self._nutritional_values_RSS(dinner_reqs, self._mul_nutritional_values(self._sum_nutritional_values(i["nutritional_values"], j["nutritional_values"]), n))
                    if cur_RSS < lowest_RSS:
                        lowest_RSS = cur_RSS
                        i["number_of_servings"] /= n
                        self._scale_recipe(i, 1/j["number_of_servings"])
                        j["number_of_servings"] /= n
                        self._scale_recipe(j, 1/j["number_of_servings"])
                        i["nutritional_values"] = self._mul_nutritional_values(i["nutritional_values"], n)
                        j["nutritional_values"] = self._mul_nutritional_values(j["nutritional_values"], n)
                        best_meal_plan[2] = i
                        best_meal_plan[3] = j

        return json.dumps(best_meal_plan)
