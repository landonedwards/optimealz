def generate_meal_plan(recipes, max_calories, max_budget, dietary_restriction=None):
    selected = []

    total_calories = 0
    total_cost = 0
    
    for recipe in recipes:
        if dietary_restriction:
            if dietary_restriction not in recipe["diet"]:
                continue

        if total_calories + recipe["calories"] > max_calories:
            continue

        if total_cost + recipe["cost"] > max_budget:
            continue

        selected.append(recipe)
        total_calories += recipe["calories"]
        total_cost += recipe["cost"]

    return {
        "meals" : selected,
        "total_calories" : total_calories,
        "total_cost" : total_cost
    }

