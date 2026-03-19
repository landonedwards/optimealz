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

def calculate_calorie_score(recipe_calories, constraints):
    """
    Rewards recipes that are close to the ideal calories per meal
    target.
    """
    if not constraints.max_calories or not constraints.meals_per_day:
        return 0
    
    target_per_meal = constraints.max_calories / constraints.meals_per_day
    # calculate how far off the recipe is (ex: 600 - 500 = 100)
    diff = abs(recipe_calories - target_per_meal)
    # ex: (100 / 500) * 10 = 2  
    penalty = (diff / target_per_meal) * 10

    # prevents score from becoming negative (ex: 10 - 2 = 8 points)
    return max(0, 10 - penalty)

def score_recipe(recipe, constraints):
    score = 0

    # meals that are on track to meet the calorie goal are preferred
    cal_score = calculate_calorie_score(recipe.get_calories(), constraints)
    score += (cal_score * 3)

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

def calculate_day_need_score(day_totals, active_targets):
    """
    Helper function for assign_meals_to_days(). Returns how far below 
    its targets this day currently is, as a combined percentage. Higher
    score means it is a needier day and it should receive the next meal.
    """
    total_deficit = 0
    for key, target in active_targets.items():
        if target:
            # calculate percentage of this target still unfulfilled 
            deficit = max(0, target - day_totals[key]) / target
            total_deficit += deficit
    return total_deficit

def assign_meals_to_days(selected_recipes, constraints):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    if constraints.meals_per_day is not None and constraints.meals_per_day <= 0:
        raise ValueError("meals_per_day must be greater than 0")
    
    day_buckets = {day: [] for day in days}

    day_totals = {
        day: {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        for day in days
    }

    # only include macros the user set a target for
    active_targets = {"calories": constraints.max_calories}
    if constraints.target_protein:
        active_targets["protein"] = constraints.target_protein
    if constraints.target_carbs:
        active_targets["carbs"] = constraints.target_carbs
    if constraints.target_fat:
        active_targets["fat"] = constraints.target_fat

    # highest calorie meals first
    sorted_by_calories = sorted(selected_recipes, 
                                key=lambda r: r.get_calories(),
                                reverse=True)
    
    for recipe in sorted_by_calories:
        eligible_days = [day for day in days if len(day_buckets[day]) < constraints.meals_per_day]
        if not eligible_days:
            break  # all days are full, stop assigning

        # find the day furthest from meeting its targets
        neediest_day = max(eligible_days, 
                           key=lambda day: calculate_day_need_score(day_totals[day], active_targets))
        
        day_buckets[neediest_day].append(recipe)

        # update that day's running totals so the next iteration
        # reflects this meal being committed to it
        day_totals[neediest_day]["calories"] += recipe.get_calories()
        day_totals[neediest_day]["protein"]  += recipe.nutrition.get("protein", 0)
        day_totals[neediest_day]["carbs"]    += recipe.nutrition.get("carbs", 0)
        day_totals[neediest_day]["fat"]      += recipe.nutrition.get("fat", 0)

    # pad any short days with None so the frontend always gets
    # exactly meals_per_day slots per day to render
    for day in days:
        while len(day_buckets[day]) < constraints.meals_per_day:
            day_buckets[day].append(None)

    return day_buckets

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
    chosen_names = set()
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

        if recipe.name in chosen_names:
            continue

        if exceeds_macros(macro_totals, recipe, constraints):
            continue

        chosen.append(recipe)
        chosen_names.add(recipe.name)
        total_calories += recipe.get_calories()
        total_cost += recipe.cost

        # update macro totals
        for key in macro_totals:
            macro_totals[key] += recipe.nutrition.get(key, 0)

    weekly_plan = assign_meals_to_days(chosen, constraints)
    return weekly_plan, chosen

