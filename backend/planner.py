import random

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

def exceeds_macros(current_totals, recipe, constraints):
    """
    Prevents plan from drifting far beyond macro targets. Allows
    some flexibility but blocks extreme overshoots. 
    """

    # helper function to compare what the combined total (current total + recipe.macro) would be vs. allowed amount 
    def exceeds(key, target):
        # if no target value for macro...
        if not target:
            return False
        
        # allows up to 20% over target
        allowed = target * 1.2
        # returns whether current total + recipe macro content is greater than 1.2x the target
        return current_totals[key] + recipe.nutrition.get(key, 0) > allowed  # second value (0) in get() is a fallback value
    
    return (
        # returns true if any of these would exceed allowed (target * 1.2)
        exceeds("protein", constraints.target_protein) or
        exceeds("carbs", constraints.target_carbs) or
        exceeds("fat", constraints.target_fat)
    )

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
        for item in recipe.ingredients:

            name = item["name"]
            amount = item["amount"]
            unit = item["unit"]

            key = f"{name}_{unit}" # prevents mixing cups vs grams

            # use a combined key to keep units separate (ex: "spinach_g")
            if key not in grocery:
                grocery[key] = {
                    "name": name,
                    "amount": 0,
                    "unit": unit
                }

            # grab the value of the ingredient if it exists and add amount needed for new recipe
            grocery[key]["amount"] += amount
    
    return list(grocery.values())
    
def assign_meals_to_days(selected_recipes, meals_per_day=3):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    if meals_per_day is not None and meals_per_day <= 0:
        raise ValueError("meals_per_day must be greater than 0")
    
    weekly_plan = {}
    # enumerate adds a counter to an iterable (0: Sunday)
    for day_index, day in enumerate(days):
        # calculate start index based on current index and number of meals per day (0 * 3 = 0)
        start = day_index * meals_per_day
        # calculate end index based on number of meals per day (0 + 3 = 3)
        end = start + meals_per_day
        # grab the slice of the array using the start and end indices (0:3 (first three recipes would go to Sunday))
        daily_meals = selected_recipes[start:end]

        # pad with None if there aren't enough meals left (helps JS render more consistently)
        while len(daily_meals) < meals_per_day:
            daily_meals.append(None)

        weekly_plan[day] = daily_meals

    return weekly_plan

def build_meal_plan(recipes, constraints):
    # eliminate any single recipes that violate a contraint
    recipe_candidates = filter_recipes(recipes, constraints)

    # shuffle so the plan isn't the same every time (even with same constraints)
    random.shuffle(recipe_candidates)

    ranked = sorted(recipe_candidates, 
                    # for each recipe, calculate its score and order it 
                    key=lambda r: score_recipe(r, constraints), 
                    # have the list sort highest to smallest (naturally does smallest to highest)
                    reverse=True)
    
    chosen = []
    total_calories = 0
    total_cost = 0
    macro_totals = {"protein": 0, "carbs": 0, "fat": 0}
    
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

        if exceeds_macros(macro_totals, recipe, constraints):
            continue

        chosen.append(recipe)

        total_calories += recipe.get_calories()
        total_cost += recipe.cost

        # update macro totals
        for key in macro_totals:
            macro_totals[key] += recipe.nutrition.get(key, 0)

    return chosen

