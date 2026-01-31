from typing import List, Dict

class Recipe:
    def __init__(
        self,
        name: str,
        calories: int,
        cost: float,
        cook_time: int,
        dietary_tags: List[str],
        nutrition: Dict[str, float],
        ingredients: Dict[str, float]
    ):
        self.name = name
        self.calories = calories
        self.cost = cost
        self.cook_time = cook_time
        self.dietary_tags = dietary_tags
        self.nutrition = nutrition
        self.ingredients = ingredients