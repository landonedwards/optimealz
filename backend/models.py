from typing import List, Dict

class Recipe:
    def __init__(
        self,
        name: str,
        cost: float,
        cook_time: int,
        dietary_tags: List[str],
        nutrition: Dict[str, float],
        ingredients: Dict[str, float]
    ):
        self.name = name
        self.cost = cost
        self.cook_time = cook_time
        self.dietary_tags = dietary_tags
        self.nutrition = nutrition
        self.ingredients = ingredients

    def get_calories(self):
        return self.nutrition.get("calories", 0)
    
    def to_dict(self):
        return {
            "name": self.name,
            "cost": self.cost,
            "cook_time": self.cook_time,
            "calories": self.get_calories(),
            "nutrition": self.nutrition,
            "dietary_tags": self.dietary_tags
        }

class Ingredient:
    def __init__(self, name, calories, protein, carbs, fat):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat

class MealPlan:
    def __init__(self, recipes):
        self.recipes = recipes

    def total_nutrition(self):
        totals = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0
        }

        for recipe in self.recipes:
            for key in totals:
                totals[key] += recipe.nutrition.get(key, 0)
        
        return totals
    
    def total_cost(self):
        return sum(recipe.cost for recipe in self.recipes)
    
    def to_dict(self):
        return {
            # creates an array of recipe dictionaries
            "recipes": [r.to_dict() for r in self.recipes],
            "total_nutrition": self.total_nutrition(),
            "total_cost": self.total_cost() 
        }