import requests
import json
import os
from dotenv import load_dotenv
from .models import Recipe

load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
CACHE_FILE = "recipes_cache.json"

def fetch_recipes_batch(offset=0, batch_size=50):

    url = "https://api.spoonacular.com/recipes/complexSearch"

    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "number": batch_size,
        "offset": offset,
        "addRecipeNutrition": True,
        "addRecipeInformation": True, # required for tags and price
        "fillIngredients": True       # required for extendedIngredients
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return data["results"]


def normalize_recipe(recipe):

    # normalize nutrients 
    nutrients = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }

    for nutrient in recipe["nutrition"]["nutrients"]:
        name = nutrient["name"].lower()

        if "calories" in name:
            nutrients["calories"] = nutrient["amount"]
        elif "protein" in name:
            nutrients["protein"] = nutrient["amount"]
        elif "carbohydrates" in name:
            nutrients["carbs"] = nutrient["amount"]
        elif "fat" in name:
            nutrients["fat"] = nutrient["amount"]

    # normalize ingredients
    ingredients = []

    for ingredient in recipe["extendedIngredients"]:
        ingredients[ingredient["name"]] = {
            "amount": ingredient["amount"],
            "unit": ingredient["unit"]
        }

    tags = []

    if recipe.get("vegetarian"):
        tags.append("vegetarian")
    if recipe.get("vegan"):
        tags.append("vegan")
    if recipe.get("glutenFree"):
        tags.append("gluten-free")
    if recipe.get("dairyFree"):
        tags.append("dairy-free")

    # converts from cents to dollars
    cost = recipe.get("pricePerServing", 0) / 100

    return {
        "name": recipe.get("title"),
        "cook_time": recipe.get("readyInMinutes"),
        "cost": cost,
        "source_url": recipe.get("sourceUrl"),
        "ingredients": ingredients,
        "nutrition": nutrients,
        "dietary_tags": tags
    }


def build_dataset(total_recipes=300, batch_size=50):

    recipes = []

    for offset in range(0, total_recipes, batch_size):

        batch = fetch_recipes_batch(offset, batch_size)

        for recipe in batch:
            recipes.append(normalize_recipe(recipe))

    with open(CACHE_FILE, "w") as file:
        # saves retrieved dataset to JSON cache
        json.dump(recipes, file, indent=2)

    return recipes

def load_cached_dataset():
    """
    Load recipes from cache if available
    """
    if not os.path.exists(CACHE_FILE):
        return None
    
    with open(CACHE_FILE, "r") as file:
        data = json.load(file)

    recipes = []

    for recipe in data:
        recipes.append(
            Recipe(
                name=recipe["name"],
                cost=recipe["cost"],
                cook_time=recipe["cook_time"],
                dietary_tags=recipe["dietary_tags"],
                nutrition=recipe["nutrition"],
                ingredients=recipe["ingredients"],
                source_url=recipe.get("source_url")
            )
        )

    return recipes