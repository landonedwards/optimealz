from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from typing import Optional
from .recipes import RECIPES
from .planner import build_meal_plan, aggregate_ingredients
from .nutrition_api import search_foods, get_nutrition_by_fdc_id
from .models import Ingredient

load_dotenv()
USDA_API_KEY = os.getenv("USDA_API_KEY")

app = FastAPI()

app.add_middleware(CORSMiddleware, 
                   # change this to my site's URL, so not just any site can send requests
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.get("/")
def root():
    return {"message": "Optimealz API running"}

class Constraints(BaseModel):
    max_calories: int
    max_budget: float
    max_cook_time: int = 90
    dietary_restriction: Optional[str] = None

    target_protein: Optional[int] = None
    target_carbs: Optional[int] = None
    target_fat: Optional[int] = None

    meals_per_week: int = 7

@app.post("/generate-plan")
def generate_plan(constraints: Constraints):
    selected_meals = build_meal_plan(RECIPES, constraints)
    grocery_list = aggregate_ingredients(selected_meals)

    return {
        "meals": [recipe.name for recipe in selected_meals],
        "total_cost": sum(recipe.cost for recipe in selected_meals),
        "total_calories": sum(recipe.get_calories() for recipe in selected_meals),
        "grocery_list": grocery_list
    }