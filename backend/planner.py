import random

def filter_recipes(recipes, constraints):
    valid_recipes = []

    for recipe in recipes:
        # skip any single recipe that violates the max cooking time (or doesn't have a cook time)
        if recipe.cook_time is None or recipe.cook_time > constraints.max_cook_time:
            continue

        if constraints.dietary_restriction:
            # skip recipe if it does not contain the dietary restriction(s) selected
            if constraints.dietary_restriction not in recipe.dietary_tags:
                continue

        valid_recipes.append(recipe)

    return valid_recipes

def score_recipe(recipe, remaining_calories, remaining_budget,
                 remaining_protein, remaining_carbs, remaining_fat):
    """
    Scores a recipe against what the current day still needs. All
    remaining values are the headroom left for this day after meals 
    already committed to it are subtracted. 
    """
    score = 0

    # reward recipes that are close to the remaining headroom
    if remaining_calories > 0:
        diff    = abs(recipe.get_calories() - remaining_calories)
        penalty = (diff / remaining_calories) * 10
        # max(0, ...) does not allow score to go negative
        score  += max(0, 10 - penalty) * 3    
 
    # cheaper meals preferred 
    score += (10 - recipe.cost)
 
    # faster meals preferred 
    score += (90 - recipe.cook_time) / 10
 
    # score how well this recipe satisfies what the day still needs.

    # calculates percent of target protein this recipe provides. If greater than remaining protein, stop it at 1 (100%)
    if remaining_protein and remaining_protein > 0:
        score += min(recipe.nutrition.get("protein", 0) / remaining_protein, 1) * 5  # highest value
 
    if remaining_carbs and remaining_carbs > 0:
        # doesn't give extra points for going over target threshold
        score += min(recipe.nutrition.get("carbs", 0) / remaining_carbs, 1) * 3      # moderate value
 
    if remaining_fat and remaining_fat > 0:
        score += min(recipe.nutrition.get("fat", 0) / remaining_fat, 1) * 2          # lowest value
 
    return score

def build_meal_plan(recipes, constraints):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
 
    meals_per_day = constraints.meals_per_day or 3
 
    # get per-day targets by dividing the weekly totals by 7
    daily_cal_target     =  constraints.max_calories   / 7
    daily_budget         =  constraints.max_budget     / 7
    daily_protein_target = (constraints.target_protein / 7) if constraints.target_protein else None
    daily_carbs_target   = (constraints.target_carbs   / 7) if constraints.target_carbs   else None
    daily_fat_target     = (constraints.target_fat     / 7) if constraints.target_fat     else None
 
    # filter out recipes that violate hard constraints (cook time, diet)
    # before the selection loop so we don't re-check on every iteration
    candidates = filter_recipes(recipes, constraints)
 
    if not candidates:
        return {day: [None] * meals_per_day for day in days}, []
 
    weekly_plan = {}
    all_chosen  = []
    # track names across the whole week to avoid repeating the same meal
    used_names  = set()
 
    for day in days:
        day_meals = []
 
        # running totals for what this day has consumed so far
        day_calories = 0
        day_cost     = 0
        day_protein  = 0
        day_carbs    = 0
        day_fat      = 0
 
        for slot in range(meals_per_day):
            # how much of each target this day still has room for
            remaining_calories =  daily_cal_target     - day_calories
            remaining_budget   =  daily_budget         - day_cost
            remaining_protein  = (daily_protein_target - day_protein) if daily_protein_target else None
            remaining_carbs    = (daily_carbs_target   - day_carbs)   if daily_carbs_target   else None
            remaining_fat      = (daily_fat_target     - day_fat)     if daily_fat_target     else None
 
            # this is the last meal slot of the day; it can use
            # all remaining headroom instead of splitting it equally,
            # so the day can still hit its calorie target even if earlier
            # slots ran under
            is_last_slot = (slot == meals_per_day - 1)
 
            # score every candidate against this slot's remaining need,
            # then sort highest-to-lowest; add small noise so identical
            # scores don't always resolve to the same recipe across runs
            def noisy_score(r):
                return score_recipe(
                    r,
                    remaining_calories,
                    remaining_budget,
                    remaining_protein,
                    remaining_carbs,
                    remaining_fat,
                ) + random.uniform(0, 0.5)
 
            ranked = sorted(candidates, key=noisy_score, reverse=True)
 
            picked = None
            for recipe in ranked:
                # never repeat a meal already used this week
                if recipe.name in used_names:
                    continue
 
                # for the last slot allow using all remaining headroom; for
                # earlier slots allow up to 120% of an equal share so one big
                # meal doesn't crowd out the rest
                if is_last_slot:
                    cal_limit = remaining_calories * 1.2
                else:
                    # equal share of what's left across remaining slots
                    slots_left = meals_per_day - slot
                    cal_limit  = (remaining_calories / slots_left) * 1.2
 
                if recipe.get_calories() > cal_limit:
                    continue
 
                # hard budget cap for this day
                if day_cost + recipe.cost > daily_budget * 1.1:   # 10% daily budget flex
                    continue
 
                picked = recipe
                break
 
            if picked:
                day_meals.append(picked)
                used_names.add(picked.name)
                all_chosen.append(picked)
                day_calories += picked.get_calories()
                day_cost     += picked.cost
                day_protein  += picked.nutrition.get("protein", 0)
                day_carbs    += picked.nutrition.get("carbs",   0)
                day_fat      += picked.nutrition.get("fat",     0)
            else:
                # no valid recipe found for this slot; pad with None
                # so the frontend always gets meals_per_day entries
                day_meals.append(None)
 
        weekly_plan[day] = day_meals
 
    return weekly_plan, all_chosen