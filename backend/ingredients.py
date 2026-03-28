from .models import Ingredient

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

 
# maps each unit → (dimension, factor_to_base)
# factor_to_base: multiply amount by this to get ml (volume) or g (weight)
UNIT_CONVERSIONS = {
    # ── volume ───────────────────────────────
    "ml":        ("volume", 1),
    "l":         ("volume", 1000),
    "tsp":       ("volume", 4.92892),
    "teaspoon":  ("volume", 4.92892),
    "tbsp":      ("volume", 14.7868),
    "tablespoon":("volume", 14.7868),
    "fl oz":     ("volume", 29.5735),
    "cup":       ("volume", 240),
    "cups":      ("volume", 240),
    "pint":      ("volume", 473.176),
    "quart":     ("volume", 946.353),
    "gallon":    ("volume", 3785.41),
 
    # ── weight ───────────────────────────────
    "g":         ("weight", 1),
    "kg":        ("weight", 1000),
    "oz":        ("weight", 28.3495),
    "lb":        ("weight", 453.592),
    "pound":     ("weight", 453.592),
    "pounds":    ("weight", 453.592),
}

def _to_base(amount, unit):
    """
    Converts amount to its base unit (ml or g).
    Returns None if the unit is not in the conversion table
    (e.g. countables like 'eggs' or unknown units).
    """
    entry = UNIT_CONVERSIONS.get(unit.lower().strip())
    if entry is None:
        return None, None
    dimension, factor = entry
    return amount * factor, dimension
 
def _from_base(base_amount, target_unit):
    """
    Converts a base-unit amount (ml or g) back into target_unit.
    Used to restate all entries in the dominant unit before summing.
    """
    entry = UNIT_CONVERSIONS.get(target_unit.lower().strip())
    if entry is None:
        return base_amount
    _, factor = entry
    return base_amount / factor

def aggregate_ingredients(recipes):
    """
    Collects all ingredient entries across all recipes, converts
    same-dimension units so they can be merged, and returns one
    grocery list entry per (ingredient, dimension) pair.
    """
 
    # raw_entries[ingredient_name][dimension] = list of (amount, unit).
    # collect everything first, then decide the dominant unit per group.
    raw_entries = {}
 
    for recipe in recipes:
        for item in recipe.ingredients:
            name   = item["name"].strip().lower()
            amount = item["amount"]
            unit   = item["unit"].strip() if item["unit"] else ""
 
            if name not in raw_entries:
                raw_entries[name] = {}
 
            base_amount, dimension = _to_base(amount, unit)
 
            if dimension is None:
                # countable or unknown unit — group under a special "countable" dimension
                # so they accumulate separately from any weight/volume entries
                dimension = f"countable_{unit}"
 
            if dimension not in raw_entries[name]:
                raw_entries[name][dimension] = []
 
            raw_entries[name][dimension].append({
                "amount":      amount,
                "unit":        unit,
                "base_amount": base_amount if base_amount is not None else amount,
            })
 
    grocery = []
 
    for name, dimensions in raw_entries.items():
        for dimension, entries in dimensions.items():
 
            if dimension.startswith("countable"):
                # countable/unknown: sum amounts as-is, keep the unit from
                # whichever entry had the largest single amount
                dominant_unit = max(entries, key=lambda e: e["amount"])["unit"]
                total = round(sum(e["amount"] for e in entries), 1)
                grocery.append({"name": name, "amount": total, "unit": dominant_unit})
                continue
 
            # find which original unit had the largest total base amount;
            # that becomes the display unit for the merged entry
            unit_totals = {}
            for e in entries:
                u = e["unit"]
                unit_totals[u] = unit_totals.get(u, 0) + e["base_amount"]
 
            dominant_unit = max(unit_totals, key=unit_totals.get)
 
            # convert every entry into the dominant unit and sum
            total_base = sum(e["base_amount"] for e in entries)
            total_in_dominant = round(_from_base(total_base, dominant_unit), 1)
 
            grocery.append({
                "name":   name,
                "amount": total_in_dominant,
                "unit":   dominant_unit,
            })

    # sort grocery list alphabetically by name
    return sorted(grocery, key=lambda item: item["name"])