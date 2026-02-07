def generate_meal_plan(recipes, max_calories, max_budget, dietary_restriction=None):
    plan = []

    total_calories = 0
    total_cost = 0
    
    for recipe in recipes:
        if dietary_restriction:
            if dietary_restriction not in recipe.dietary_tags:
                continue

        if total_calories + recipe.get_calories() > max_calories:
            continue

        if total_cost + recipe.cost > max_budget:
            continue

        plan.append(recipe)
        total_calories += recipe.get_calories()
        total_cost += recipe.cost

    return {
        # returns an array of all the recipe names added to plan
        "meals" : [recipe.name for recipe in plan],
        "total_calories" : total_calories,
        "total_cost" : total_cost
    }

