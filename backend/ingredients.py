from models import Ingredient

def create_ingredient_from_food(food_data: dict) -> Ingredient:
    nutrients = food_data.get("foodNutrients", [])

    def find(name):
        for nutrient in nutrients:
            if name in nutrient.get("nutrientName", "").lower():
                return nutrient.get("value", 0)
        return 0
    
    return Ingredient(name=food_data["description"],
                      calories=find("energy"),
                      protein=find("protein"),
                      carbs=find("carbohydrate"),
                      fat=find("total lipid"))