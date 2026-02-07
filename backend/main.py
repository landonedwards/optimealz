from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Optional
from .recipes import RECIPES
from .planner import generate_meal_plan
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

@app.get("/generate-plan")
def generate_plan(max_calories: int,
                  max_budget: float,
                  dietary_restriction: Optional[str] = None):
    return generate_meal_plan(recipes=RECIPES, 
                              max_calories=max_calories, 
                              max_budget=max_budget,
                              dietary_restriction=dietary_restriction)

@app.post("/generate-plan")
def generate_plan(max_calories: int, 
                  max_budget: float, 
                  dietary_restriction: str | None = None
                  ):
    plan = generate_meal_plan(RECIPES, max_calories, max_budget, dietary_restriction)
    return plan