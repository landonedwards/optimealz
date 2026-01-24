from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .recipes import RECIPES
from .planner import generate_meal_plan

app = FastAPI()

app.add_middleware(CORSMiddleware, 
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.get("/")
def root():
    return {"message": "Optimealz API running"}

@app.post("/generate-plan")
def generate_plan(max_calories: int, 
                  max_budget: float, 
                  dietary_restriction: str | None = None
                  ):
    plan = generate_meal_plan(RECIPES, max_calories, max_budget, dietary_restriction)
    return plan