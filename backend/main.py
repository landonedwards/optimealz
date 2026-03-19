from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os
from typing import Optional, List, Any
from .recipes import RECIPES
from .planner import build_meal_plan, aggregate_ingredients
from .models import Ingredient

load_dotenv()
USDA_API_KEY = os.getenv("USDA_API_KEY")
# loads any existing recipes from the cache

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
    max_calories: int = Field(..., gt=0)
    max_budget: float = Field(..., gt=0)
    max_cook_time: int = Field(default=90, gt=0)
    dietary_restriction: Optional[str] = None

    target_protein: Optional[int] = Field(default=None, ge=0)
    target_carbs: Optional[int] = Field(default=None, ge=0)
    target_fat: Optional[int] = Field(default=None, ge=0)

    meals_per_day: Optional[int] = 3
    # 3 meals x 7 days
    meals_per_week: int = Field(default=21, ge=1)

@app.post("/generate-plan")
def generate_plan(constraints: Constraints):
    weekly_plan, all_meals = build_meal_plan(RECIPES, constraints)
    grocery_list = aggregate_ingredients(all_meals)

    return {
        "week": {
            day: [
                meal.to_dict() if meal else None   # handle padded empty slots
                for meal in meals
            ]
            for day, meals in weekly_plan.items()
        },
        "totals": {
            "cost": sum(meal.cost for meal in all_meals),
            "calories": sum(meal.get_calories() for meal in all_meals)
        },
        "grocery_list": grocery_list
    }