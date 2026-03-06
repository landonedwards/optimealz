import os 
import requests
from dotenv import load_dotenv

load_dotenv()

USDA_API_KEY = os.getenv("USDA_API_KEY")

def search_foods(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches the USDA FoodData Central database for foods matching
    the query. Returns a list of food items with basic identifying information.
    """
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": USDA_API_KEY,
        "query": query,
        "pageSize": max_results
    }

    response = requests.get(url, params=params)
    # prevents program from silently continuing if the response is unsuccessful
    response.raise_for_status()

    # converts JSON response to Python dict
    data = response.json()

    # grab list of foods from response
    foods = data.get("foods", [])

    results = []

    for food in foods:
        results.append({
            # grab food item's unique ID
            "fdc_id": food.get("fdcId"),
            "name": food.get("description"),
            "category": food.get("foodCategory"),
            "brand_name": food.get("brandName")
        })

    return results

def get_nutrition_by_fdc_id(fdc_id: int) -> dict:
    # opportunity to make this into a reusable function (repeated in both functions)
    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    params = { "api_key": USDA_API_KEY }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    nutrients = data.get("foodNutrients", [])

    nutrition = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }

    for nutrient in nutrients:
        name = nutrient["nutrient"]["name"].lower()
        value = nutrient.get("amount", 0)

        # will add other nutrients later (fiber, vitamins, etc.)
        if "energy" in name:
            nutrition["calories"] = value
        elif "protein" in name:
            nutrition["protein"] = value
        elif "carbohydrate" in name:
            nutrition["carbs"] = value
        elif "total lipid" in name:
            nutrition["fat"] = value

    return nutrition