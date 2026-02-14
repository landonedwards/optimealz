def filter_recipes(recipes, constraints):
    valid_recipes = []

    for recipe in recipes:
        # skip any single recipe that violates the max cooking time 
        if recipe.cook_time > constraints.max_cook_time:
            continue

        if constraints.dietary_restriction:
            # skip recipe if it does not contain the dietary restriction(s) selected
            if constraints.dietary_restriction not in recipe.dietary_tags:
                continue

        valid_recipes.append(recipe)

    return valid_recipes

def score_recipe(recipe, constraints):
    score = 0

    # cheaper meals preferred 
    score += (10 - recipe.cost)

    # faster meals preferred
    score += (90 - recipe.cook_time) / 10

    if constraints.target_protein:
        # calculates percent of target protein this recipe provides. If greater than target protein, stop it at 1 (100%)
        score += min(recipe.nutrition["protein"] / constraints.target_protein, 1) * 5  # highest value

    if constraints.target_carbs:
        # doesn't give extra points for going over target threshold
        score += min(recipe.nutrition["carbs"] / constraints.target_carbs, 1) * 3  # moderate value

    if constraints.target_fat:
        score += min(recipe.nutrition["fat"] / constraints.target_fat, 1) * 2  # lowest value

    return score

def aggregate_ingredients(recipes):
    grocery = {}

    for recipe in recipes:
        # .items() returns a list of (key, value) tuples in the dict
        for ingredient, amount in recipe.ingredients.items():
            # grab the value of the ingredient if it exists and add amount needed for new recipe; if it does not, start at 0
            grocery[ingredient] = grocery.get(ingredient, 0) + amount
    
    return grocery

def build_meal_plan(recipes, constraints):
    # eliminate any single recipes that violate a contraint
    recipe_candidates = filter_recipes(recipes, constraints)

    ranked = sorted(recipe_candidates, 
                    # for each recipe, calculate its score and order it 
                    key=lambda r: score_recipe(r, constraints), 
                    # have the list sort highest to smallest (naturally does smallest to highest)
                    reverse=True)
    
    chosen = []
    total_calories = 0
    total_cost = 0
    
    for recipe in ranked:
        # exit early if we've already gathered the correct number of meals for the week
        if len(chosen) >= constraints.meals_per_week:
            break

        if total_calories + recipe.get_calories() > constraints.max_calories:
            continue

        if total_cost + recipe.cost > constraints.max_budget:
            continue

        # creates temporary list of names currently in chosen and compares the current recipe name against it
        if recipe.name in [recipe.name for recipe in chosen]:
            continue

        chosen.append(recipe)
        total_calories += recipe.get_calories()
        total_cost += recipe.cost

    return chosen

