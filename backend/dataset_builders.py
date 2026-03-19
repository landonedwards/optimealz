import requests
import json
import os
from dotenv import load_dotenv
from .models import Recipe

load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
CACHE_FILE = "recipes_cache.json"

def fetch_batch(extra_params, batch_size=25):
    """
    Single fetch function used by every builder.
    extra_params is a dict of any Spoonacular complexSearch filters
    (e.g. minProtein, type, minCalories, query, cuisine, etc.)
    """
    url = "https://api.spoonacular.com/recipes/complexSearch"

    # base params required by every request
    params = {
        "apiKey":               SPOONACULAR_API_KEY,
        "number":               batch_size,
        "addRecipeNutrition":   True,   # needed for calories/protein/carbs/fat
        "addRecipeInformation": True,   # needed for dietary tags and price
        "fillIngredients":      True,   # needed for extendedIngredients list
        **extra_params,
    }

    response = requests.get(url, params=params)
    # prevents program from silently continuing if the response is unsuccessful
    response.raise_for_status()
    return response.json().get("results", [])


def normalize_recipe(raw_recipe):
    """
    Converts a raw Spoonacular result into the flat shape that
    Recipe() and load_cached_dataset() expect. Used by every builder.
    """

    nutrient_totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

    for nutrient in raw_recipe.get("nutrition", {}).get("nutrients", []):
        nutrient_name   = nutrient["name"].lower()
        nutrient_amount = nutrient.get("amount", 0)

        # match by substring so slight naming variations don't break parsing
        if "calorie"        in nutrient_name: 
            nutrient_totals["calories"] = nutrient_amount
        elif "protein"      in nutrient_name: 
            nutrient_totals["protein"]  = nutrient_amount
        elif "carbohydrate" in nutrient_name: 
            nutrient_totals["carbs"] = nutrient_amount
        elif "fat"          in nutrient_name: 
            nutrient_totals["fat"] = nutrient_amount

    # stored as a list of dicts so aggregate_ingredients() in planner.py
    # can iterate them with item["name"], item["amount"], item["unit"]
    ingredient_list = []
    for ingredient in raw_recipe.get("extendedIngredients", []):
        ingredient_list.append({
            "name":   ingredient.get("name", ""),
            "amount": ingredient.get("amount", 0),
            "unit":   ingredient.get("unit", ""),
        })

    # used by filter_recipes() in planner.py to enforce dietary restrictions
    dietary_tags = []
    if raw_recipe.get("vegetarian"): dietary_tags.append("vegetarian")
    if raw_recipe.get("vegan"):      dietary_tags.append("vegan")
    if raw_recipe.get("glutenFree"): dietary_tags.append("gluten-free")
    if raw_recipe.get("dairyFree"):  dietary_tags.append("dairy-free")

    # pricePerServing comes from Spoonacular in cents, so we convert to dollars
    cost_per_serving = raw_recipe.get("pricePerServing", 0) / 100

    return {
        "name":         raw_recipe.get("title"),
        "cook_time":    raw_recipe.get("readyInMinutes"),
        "cost":         cost_per_serving,
        "source_url":   raw_recipe.get("sourceUrl"),
        "ingredients":  ingredient_list,
        "nutrition":    nutrient_totals,
        "dietary_tags": dietary_tags,
    }


def load_cache():
    """
    Reads the raw JSON cache and returns (recipe_list, name_set).
    name_set is used by run_builder() for duplicate checking.
    Returns ([], set()) if no cache file exists yet.
    """
    if not os.path.exists(CACHE_FILE):
        print("No existing cache found. A new one will be created.")
        # returns tuple of list and set
        return [], set()

    with open(CACHE_FILE, "r") as file:
        recipes = json.load(file)

    existing_names = {recipe["name"] for recipe in recipes}
    print(f"Loaded existing cache: {len(recipes)} recipes")
    return recipes, existing_names


def load_cached_dataset():
    """
    Used by recipes.py at server startup. Reads the cache and returns
    a list of Recipe model instances ready for the planner to use.
    Returns None if no cache exists, indicating that a builder should
    be run first.
    """
    recipes, _ = load_cache()

    if not recipes:
        return None

    # convert each raw dict into a Recipe object the planner can work with
    return [
        Recipe(
            name =         recipe["name"],
            cost =         recipe["cost"],
            cook_time =    recipe["cook_time"],
            dietary_tags = recipe["dietary_tags"],
            nutrition =    recipe["nutrition"],
            ingredients =  recipe["ingredients"],
            source_url =   recipe.get("source_url"),
        )
        for recipe in recipes
    ]


def save_cache(recipes):
    with open(CACHE_FILE, "w") as file:
        json.dump(recipes, file, indent=2)
    print(f"Cache saved: {len(recipes)} total recipes.")


def run_builder(bucket_list, batch_size=25):
    """
    Core engine shared by every builder below.

    bucket_list: a list of dicts where each dict is a set of Spoonacular
    params defining one "bucket" to fetch. For example:
        {"query": "chicken", "minProtein": 40}
        {"type": "soup", "minCalories": 200}
        {"cuisine": "mediterranean"}

    Each bucket is fetched, normalized, and deduplicated against the
    existing cache before being merged in. Safe to run multiple times;
    recipes already in the cache are always skipped.
    """
    existing_recipes, existing_names = load_cache()
    new_recipes = []

    for bucket_params in bucket_list:
        # readable label used in progress output
        bucket_label = ", ".join(f"{key}={value}" for key, value in bucket_params.items())

        try:
            batch = fetch_batch(bucket_params, batch_size=batch_size)
        except requests.HTTPError as e:
            # skip this bucket and keep going rather than crashing the whole run
            print(f"  Warning: skipping bucket [{bucket_label}]: {e}")
            continue

        added = 0
        for raw_recipe in batch:
            normalized = normalize_recipe(raw_recipe)
            recipe_name = normalized["name"]

            # skip if already in cache or already added in this run
            if recipe_name in existing_names:
                continue

            # add to the name set immediately so within-run duplicates are
            # also caught (same recipe can appear in multiple buckets)
            existing_names.add(recipe_name)
            new_recipes.append(normalized)
            added += 1

        print(f"  [{bucket_label}]: +{added} new recipes")

    merged = existing_recipes + new_recipes
    save_cache(merged)
    print(f"Done. Added {len(new_recipes)} new recipes.\n")
    return merged


def build_balanced_dataset(total_recipes=300):
    """
    General-purpose builder. Each bucket represents a combination of a 
    calorie tier and meal type to ensure coverage across light, medium,
    and heavy meals throughout the day.
    """
    calorie_tiers = [
        {"minCalories": 600, "maxCalories": 1000},  # high-cal 
        {"minCalories": 350, "maxCalories": 600},   # moderate 
        {"minCalories": 100, "maxCalories": 350},   # light 
    ]
    meal_types = ["breakfast", "main course", "snack", "soup", "salad"]

    buckets = [
        {**tier, "type": meal_type}
        for tier in calorie_tiers
        for meal_type in meal_types
    ]

    # divide the total recipe target evenly across all buckets
    per_bucket = max(1, total_recipes // len(buckets))

    print("Building balanced dataset...")
    return run_builder(buckets, batch_size=per_bucket)


def build_protein_dataset():
    """
    High-protein recipes bucketed by main protein source. Sorted by highest
    protein first so tight minProtein thresholds don't return padded duplicates.
    """
    buckets = [
        {"query": "chicken",        "minProtein": 40, "sort": "protein", "sortDirection": "desc"},
        {"query": "beef",           "minProtein": 40, "sort": "protein", "sortDirection": "desc"},
        {"query": "salmon",         "minProtein": 35, "sort": "protein", "sortDirection": "desc"},
        {"query": "tuna",           "minProtein": 35, "sort": "protein", "sortDirection": "desc"},
        {"query": "turkey",         "minProtein": 30, "sort": "protein", "sortDirection": "desc"},
        {"query": "shrimp",         "minProtein": 30, "sort": "protein", "sortDirection": "desc"},
        {"query": "pork",           "minProtein": 30, "sort": "protein", "sortDirection": "desc"},
        {"query": "eggs",           "minProtein": 25, "sort": "protein", "sortDirection": "desc"},
        {"query": "greek yogurt",   "minProtein": 25, "sort": "protein", "sortDirection": "desc"},
        {"query": "cottage cheese", "minProtein": 25, "sort": "protein", "sortDirection": "desc"},
        {"query": "lentils",        "minProtein": 20, "sort": "protein", "sortDirection": "desc"},  # plant-based
        {"query": "tofu",           "minProtein": 20, "sort": "protein", "sortDirection": "desc"},  # plant-based
    ]

    print("Building protein-focused dataset...")
    return run_builder(buckets, batch_size=25)


def build_soup_and_salad_dataset():
    """
    Soups and salads bucketed by cuisine. These tend to be lower-calorie
    options that the balanced builder underrepresents because they score
    lower against calorie targets.
    """
    cuisines = [
        "american", "italian", "asian", "mexican",
        "mediterranean", "french", "middle eastern",
    ]

    # one bucket per cuisine for each meal type
    buckets = (
        [{"type": "soup",  "cuisine": cuisine} for cuisine in cuisines] +
        [{"type": "salad", "cuisine": cuisine} for cuisine in cuisines]
    )

    print("Building soup and salad dataset...")
    return run_builder(buckets, batch_size=20)


def build_cuisine_dataset():
    """
    Main courses bucketed by world cuisine. Breaks up the repetition that
    comes from unfiltered fetches, which tend to return American recipes heavily.
    """
    buckets = [
        {"type": "main course", "cuisine": cuisine}
        for cuisine in [
            "italian", "mexican", "asian", "indian", "mediterranean",
            "middle eastern", "french", "greek", "spanish", "thai",
            "japanese", "korean", "caribbean", "african",
        ]
    ]

    print("Building cuisine variety dataset...")
    return run_builder(buckets, batch_size=20)


def build_quick_meals_dataset():
    """
    Meals under 20 minutes. Users with tight cook-time constraints often end
    up with very few valid candidates from the other builders — this fills
    that gap.
    """
    buckets = [
        {"maxReadyTime": 20, "type": meal_type}
        for meal_type in ["main course", "breakfast", "snack", "salad"]
    ]

    print("Building quick meals dataset...")
    return run_builder(buckets, batch_size=25)


def build_budget_dataset():
    """
    Cheap meals sorted by price ascending. Spoonacular has no direct price
    ceiling filter, so we take the cheapest end of each meal type instead.
    """
    buckets = [
        {"type": meal_type, "sort": "price", "sortDirection": "asc"}
        for meal_type in ["main course", "breakfast", "snack", "soup", "salad"]
    ]

    print("Building budget meals dataset...")
    return run_builder(buckets, batch_size=25)


if __name__ == "__main__":
    build_balanced_dataset()
    build_protein_dataset()
    build_soup_and_salad_dataset()
    build_cuisine_dataset()
    build_quick_meals_dataset()
    build_budget_dataset()