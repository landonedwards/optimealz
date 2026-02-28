from .models import Recipe

RECIPES = [
    # --- COMPLEX POULTRY & MEAT ---
    Recipe(
        name="Mediterranean Stuffed Chicken",
        cost=11.50,
        cook_time=35,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 540, "protein": 45, "carbs": 12, "fat": 28},
        ingredients=[
            {"name": "chicken breast", "amount": 200, "unit": "g"},
            {"name": "spinach", "amount": 1, "unit": "cup"},
            {"name": "feta cheese", "amount": 30, "unit": "g"},
            {"name": "sun-dried tomatoes", "amount": 4, "unit": "pcs"},
            {"name": "garlic", "amount": 2, "unit": "cloves"},
            {"name": "olive oil", "amount": 1, "unit": "tbsp"},
            {"name": "oregano", "amount": 1, "unit": "tsp"}
        ]
    ),
    Recipe(
        name="Korean Beef Bulgogi Bowl",
        cost=13.00,
        cook_time=25,
        dietary_tags=["high-protein"],
        nutrition={"calories": 680, "protein": 38, "carbs": 70, "fat": 22},
        ingredients=[
            {"name": "flank steak", "amount": 150, "unit": "g"},
            {"name": "soy sauce", "amount": 3, "unit": "tbsp"},
            {"name": "brown sugar", "amount": 1, "unit": "tbsp"},
            {"name": "sesame oil", "amount": 1, "unit": "tsp"},
            {"name": "white rice", "amount": 1, "unit": "cup"},
            {"name": "kimchi", "amount": 0.25, "unit": "cup"},
            {"name": "shredded carrots", "amount": 0.5, "unit": "cup"},
            {"name": "green onions", "amount": 2, "unit": "stalks"}
        ]
    ),
    Recipe(
        name="Turkey Meatballs & Zoodles",
        cost=9.25,
        cook_time=30,
        dietary_tags=["high-protein", "low-carb", "gluten-free"],
        nutrition={"calories": 420, "protein": 35, "carbs": 18, "fat": 24},
        ingredients=[
            {"name": "ground turkey", "amount": 180, "unit": "g"},
            {"name": "zucchini", "amount": 2, "unit": "pcs"},
            {"name": "marinara sauce", "amount": 0.75, "unit": "cup"},
            {"name": "parmesan", "amount": 2, "unit": "tbsp"},
            {"name": "egg", "amount": 1, "unit": "pcs"},
            {"name": "almond flour", "amount": 2, "unit": "tbsp"},
            {"name": "italian seasoning", "amount": 1, "unit": "tsp"}
        ]
    ),

    # --- VEGETARIAN FEASTS ---
    Recipe(
        name="Vegetarian Buddha Bowl",
        cost=8.50,
        cook_time=20,
        dietary_tags=["vegetarian", "vegan", "gluten-free"],
        nutrition={"calories": 510, "protein": 18, "carbs": 65, "fat": 22},
        ingredients=[
            {"name": "chickpeas", "amount": 0.5, "unit": "can"},
            {"name": "quinoa", "amount": 0.5, "unit": "cup"},
            {"name": "sweet potato", "amount": 0.5, "unit": "pcs"},
            {"name": "kale", "amount": 1, "unit": "cup"},
            {"name": "tahini", "amount": 2, "unit": "tbsp"},
            {"name": "lemon juice", "amount": 1, "unit": "tbsp"},
            {"name": "maple syrup", "amount": 1, "unit": "tsp"},
            {"name": "pumpkin seeds", "amount": 1, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Mushroom & Spinach Lasagna",
        cost=10.00,
        cook_time=50,
        dietary_tags=["vegetarian"],
        nutrition={"calories": 590, "protein": 25, "carbs": 55, "fat": 28},
        ingredients=[
            {"name": "lasagna noodles", "amount": 4, "unit": "sheets"},
            {"name": "ricotta cheese", "amount": 0.5, "unit": "cup"},
            {"name": "mozzarella", "amount": 0.5, "unit": "cup"},
            {"name": "mushrooms", "amount": 100, "unit": "g"},
            {"name": "frozen spinach", "amount": 0.5, "unit": "cup"},
            {"name": "marinara sauce", "amount": 1, "unit": "cup"},
            {"name": "garlic", "amount": 1, "unit": "clove"},
            {"name": "onion", "amount": 0.25, "unit": "pcs"}
        ]
    ),

    # --- HEARTY SEAFOOD ---
    Recipe(
        name="Fish Tacos with Slaw",
        cost=11.00,
        cook_time=20,
        dietary_tags=["high-protein"],
        nutrition={"calories": 480, "protein": 32, "carbs": 42, "fat": 18},
        ingredients=[
            {"name": "tilapia fillet", "amount": 180, "unit": "g"},
            {"name": "corn tortillas", "amount": 3, "unit": "pcs"},
            {"name": "shredded cabbage", "amount": 1, "unit": "cup"},
            {"name": "greek yogurt", "amount": 2, "unit": "tbsp"},
            {"name": "lime", "amount": 1, "unit": "pcs"},
            {"name": "cilantro", "amount": 2, "unit": "tbsp"},
            {"name": "cumin", "amount": 0.5, "unit": "tsp"},
            {"name": "chili powder", "amount": 0.5, "unit": "tsp"}
        ]
    ),
    Recipe(
        name="Shrimp & Sausage Jambalaya",
        cost=14.50,
        cook_time=40,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 620, "protein": 40, "carbs": 55, "fat": 26},
        ingredients=[
            {"name": "shrimp", "amount": 150, "unit": "g"},
            {"name": "andouille sausage", "amount": 1, "unit": "link"},
            {"name": "white rice", "amount": 0.75, "unit": "cup"},
            {"name": "bell pepper", "amount": 0.5, "unit": "pcs"},
            {"name": "onion", "amount": 0.5, "unit": "pcs"},
            {"name": "celery", "amount": 1, "unit": "stalk"},
            {"name": "cajun seasoning", "amount": 1, "unit": "tbsp"},
            {"name": "chicken broth", "amount": 1.5, "unit": "cups"}
        ]
    ),

    # --- GLOBAL FLAVORS ---
    Recipe(
        name="Chicken Tikka Masala",
        cost=12.00,
        cook_time=45,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 610, "protein": 42, "carbs": 45, "fat": 28},
        ingredients=[
            {"name": "chicken breast", "amount": 200, "unit": "g"},
            {"name": "tomato puree", "amount": 0.5, "unit": "cup"},
            {"name": "heavy cream", "amount": 0.25, "unit": "cup"},
            {"name": "onion", "amount": 0.5, "unit": "pcs"},
            {"name": "ginger", "amount": 1, "unit": "tsp"},
            {"name": "garlic", "amount": 2, "unit": "cloves"},
            {"name": "garam masala", "amount": 1, "unit": "tbsp"},
            {"name": "turmeric", "amount": 0.5, "unit": "tsp"},
            {"name": "basmati rice", "amount": 1, "unit": "cup"}
        ]
    ),
    Recipe(
        name="Pad Thai",
        cost=9.50,
        cook_time=25,
        dietary_tags=["gluten-free"],
        nutrition={"calories": 580, "protein": 22, "carbs": 75, "fat": 20},
        ingredients=[
            {"name": "rice noodles", "amount": 100, "unit": "g"},
            {"name": "shrimp", "amount": 100, "unit": "g"},
            {"name": "tofu", "amount": 50, "unit": "g"},
            {"name": "bean sprouts", "amount": 0.5, "unit": "cup"},
            {"name": "egg", "amount": 1, "unit": "pcs"},
            {"name": "peanuts", "amount": 2, "unit": "tbsp"},
            {"name": "fish sauce", "amount": 2, "unit": "tbsp"},
            {"name": "tamarind paste", "amount": 1, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Falafel Pita Wrap",
        cost=6.75,
        cook_time=20,
        dietary_tags=["vegetarian"],
        nutrition={"calories": 520, "protein": 18, "carbs": 68, "fat": 22},
        ingredients=[
            {"name": "falafel balls", "amount": 4, "unit": "pcs"},
            {"name": "pita bread", "amount": 1, "unit": "pcs"},
            {"name": "hummus", "amount": 2, "unit": "tbsp"},
            {"name": "cucumber", "amount": 0.25, "unit": "pcs"},
            {"name": "tomato", "amount": 0.5, "unit": "pcs"},
            {"name": "red onion", "amount": 0.1, "unit": "pcs"},
            {"name": "tzatziki", "amount": 2, "unit": "tbsp"}
        ]
    ),

    # --- COMFORT FOOD ---
    Recipe(
        name="Shepherd's Pie",
        cost=10.50,
        cook_time=50,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 540, "protein": 32, "carbs": 45, "fat": 26},
        ingredients=[
            {"name": "ground lamb", "amount": 150, "unit": "g"},
            {"name": "potatoes", "amount": 2, "unit": "pcs"},
            {"name": "peas and carrots", "amount": 0.5, "unit": "cup"},
            {"name": "onion", "amount": 0.5, "unit": "pcs"},
            {"name": "beef broth", "amount": 0.5, "unit": "cup"},
            {"name": "butter", "amount": 1, "unit": "tbsp"},
            {"name": "milk", "amount": 2, "unit": "tbsp"},
            {"name": "thyme", "amount": 0.5, "unit": "tsp"}
        ]
    ),
    Recipe(
        name="Buffalo Cauliflower Mac",
        cost=8.00,
        cook_time=30,
        dietary_tags=["vegetarian"],
        nutrition={"calories": 610, "protein": 22, "carbs": 65, "fat": 30},
        ingredients=[
            {"name": "macaroni", "amount": 100, "unit": "g"},
            {"name": "cauliflower florets", "amount": 1, "unit": "cup"},
            {"name": "cheddar cheese", "amount": 0.75, "unit": "cup"},
            {"name": "buffalo sauce", "amount": 2, "unit": "tbsp"},
            {"name": "milk", "amount": 0.5, "unit": "cup"},
            {"name": "butter", "amount": 1, "unit": "tbsp"},
            {"name": "bread crumbs", "amount": 2, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Lentil & Vegetable Shepard's Pie",
        cost=5.50,
        cook_time=45,
        dietary_tags=["vegetarian", "vegan", "gluten-free"],
        nutrition={"calories": 420, "protein": 18, "carbs": 62, "fat": 8},
        ingredients=[
            {"name": "dry lentils", "amount": 0.5, "unit": "cup"},
            {"name": "potatoes", "amount": 2, "unit": "pcs"},
            {"name": "mushroom broth", "amount": 1, "unit": "cup"},
            {"name": "mixed veggies", "amount": 1, "unit": "cup"},
            {"name": "onion", "amount": 0.5, "unit": "pcs"},
            {"name": "garlic", "amount": 1, "unit": "clove"},
            {"name": "olive oil", "amount": 1, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Pulled Pork Sliders",
        cost=11.00,
        cook_time=30,
        dietary_tags=["high-protein"],
        nutrition={"calories": 650, "protein": 35, "carbs": 55, "fat": 32},
        ingredients=[
            {"name": "pork shoulder", "amount": 150, "unit": "g"},
            {"name": "slider buns", "amount": 3, "unit": "pcs"},
            {"name": "bbq sauce", "amount": 3, "unit": "tbsp"},
            {"name": "coleslaw mix", "amount": 0.5, "unit": "cup"},
            {"name": "apple cider vinegar", "amount": 1, "unit": "tsp"},
            {"name": "honey", "amount": 1, "unit": "tsp"}
        ]
    ),
    Recipe(
        name="Classic Cobb Salad",
        cost=9.75,
        cook_time=15,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 520, "protein": 38, "carbs": 12, "fat": 36},
        ingredients=[
            {"name": "romaine lettuce", "amount": 2, "unit": "cups"},
            {"name": "chicken breast", "amount": 100, "unit": "g"},
            {"name": "bacon bits", "amount": 2, "unit": "tbsp"},
            {"name": "hard boiled egg", "amount": 1, "unit": "pcs"},
            {"name": "avocado", "amount": 0.5, "unit": "pcs"},
            {"name": "blue cheese", "amount": 2, "unit": "tbsp"},
            {"name": "cherry tomatoes", "amount": 5, "unit": "pcs"},
            {"name": "red wine vinaigrette", "amount": 2, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Chicken Souvlaki Pita",
        cost=9.50,
        cook_time=25,
        dietary_tags=["high-protein"],
        nutrition={"calories": 510, "protein": 38, "carbs": 48, "fat": 18},
        ingredients=[
            {"name": "chicken breast", "amount": 200, "unit": "g"},
            {"name": "pita bread", "amount": 1, "unit": "pcs"},
            {"name": "cucumber", "amount": 0.5, "unit": "pcs"},
            {"name": "greek yogurt", "amount": 3, "unit": "tbsp"},
            {"name": "garlic", "amount": 2, "unit": "cloves"},
            {"name": "lemon juice", "amount": 1, "unit": "tbsp"},
            {"name": "dried oregano", "amount": 1, "unit": "tsp"},
            {"name": "cherry tomatoes", "amount": 5, "unit": "pcs"},
            {"name": "red onion", "amount": 0.25, "unit": "pcs"}
        ]
    ),
    Recipe(
        name="Beef & Broccoli Pepper Steak",
        cost=11.00,
        cook_time=20,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 540, "protein": 36, "carbs": 42, "fat": 24},
        ingredients=[
            {"name": "sirloin strips", "amount": 180, "unit": "g"},
            {"name": "broccoli florets", "amount": 2, "unit": "cups"},
            {"name": "bell pepper", "amount": 1, "unit": "pcs"},
            {"name": "soy sauce", "amount": 3, "unit": "tbsp"},
            {"name": "ginger", "amount": 1, "unit": "tsp"},
            {"name": "garlic", "amount": 1, "unit": "clove"},
            {"name": "cornstarch", "amount": 1, "unit": "tsp"},
            {"name": "sesame seeds", "amount": 1, "unit": "tsp"},
            {"name": "brown rice", "amount": 1, "unit": "cup"}
        ]
    ),
    Recipe(
        name="Turkey Chili with Cornbread",
        cost=8.75,
        cook_time=45,
        dietary_tags=["high-protein"],
        nutrition={"calories": 590, "protein": 34, "carbs": 75, "fat": 16},
        ingredients=[
            {"name": "ground turkey", "amount": 150, "unit": "g"},
            {"name": "kidney beans", "amount": 0.5, "unit": "can"},
            {"name": "diced tomatoes", "amount": 1, "unit": "can"},
            {"name": "onion", "amount": 0.5, "unit": "pcs"},
            {"name": "chili powder", "amount": 1, "unit": "tbsp"},
            {"name": "cornmeal", "amount": 0.5, "unit": "cup"},
            {"name": "milk", "amount": 0.25, "unit": "cup"},
            {"name": "egg", "amount": 1, "unit": "pcs"},
            {"name": "honey", "amount": 1, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Sheet Pan Chicken & Veggies",
        cost=8.50,
        cook_time=35,
        dietary_tags=["gluten-free", "high-protein"],
        nutrition={"calories": 420, "protein": 40, "carbs": 25, "fat": 18},
        ingredients=[
            {"name": "chicken breast", "amount": 200, "unit": "g"},
            {"name": "brussels sprouts", "amount": 1, "unit": "cup"},
            {"name": "baby carrots", "amount": 0.5, "unit": "cup"},
            {"name": "red potatoes", "amount": 2, "unit": "pcs"},
            {"name": "olive oil", "amount": 2, "unit": "tbsp"},
            {"name": "garlic powder", "amount": 1, "unit": "tsp"},
            {"name": "paprika", "amount": 1, "unit": "tsp"},
            {"name": "thyme", "amount": 0.5, "unit": "tsp"}
        ]
    ),
    Recipe(
        name="Pork Carnitas Bowls",
        cost=10.50,
        cook_time=50,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 610, "protein": 35, "carbs": 55, "fat": 28},
        ingredients=[
            {"name": "pork shoulder", "amount": 180, "unit": "g"},
            {"name": "orange juice", "amount": 0.25, "unit": "cup"},
            {"name": "lime", "amount": 1, "unit": "pcs"},
            {"name": "cumin", "amount": 1, "unit": "tsp"},
            {"name": "white rice", "amount": 1, "unit": "cup"},
            {"name": "black beans", "amount": 0.25, "unit": "cup"},
            {"name": "pickled jalapenos", "amount": 1, "unit": "tbsp"},
            {"name": "cilantro", "amount": 2, "unit": "tbsp"},
            {"name": "avocado", "amount": 0.5, "unit": "pcs"}
        ]
    ),

    # --- SEAFOOD ---
    Recipe(
        name="Lemon Butter Scallops & Risotto",
        cost=15.50,
        cook_time=40,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 580, "protein": 28, "carbs": 60, "fat": 26},
        ingredients=[
            {"name": "sea scallops", "amount": 150, "unit": "g"},
            {"name": "arborio rice", "amount": 0.75, "unit": "cup"},
            {"name": "chicken broth", "amount": 2, "unit": "cups"},
            {"name": "parmesan cheese", "amount": 0.25, "unit": "cup"},
            {"name": "butter", "amount": 2, "unit": "tbsp"},
            {"name": "lemon", "amount": 0.5, "unit": "pcs"},
            {"name": "white wine", "amount": 2, "unit": "tbsp"},
            {"name": "fresh parsley", "amount": 1, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Mediterranean Baked Cod",
        cost=12.00,
        cook_time=25,
        dietary_tags=["gluten-free", "high-protein"],
        nutrition={"calories": 380, "protein": 34, "carbs": 15, "fat": 20},
        ingredients=[
            {"name": "cod fillets", "amount": 200, "unit": "g"},
            {"name": "cherry tomatoes", "amount": 10, "unit": "pcs"},
            {"name": "kalamata olives", "amount": 8, "unit": "pcs"},
            {"name": "capers", "amount": 1, "unit": "tbsp"},
            {"name": "olive oil", "amount": 1, "unit": "tbsp"},
            {"name": "garlic", "amount": 2, "unit": "cloves"},
            {"name": "zucchini", "amount": 1, "unit": "pcs"},
            {"name": "fresh basil", "amount": 5, "unit": "leaves"}
        ]
    ),

    # --- VEGETARIAN & VEGAN ---
    Recipe(
        name="Sweet Potato & Chickpea Curry",
        cost=6.50,
        cook_time=35,
        dietary_tags=["vegetarian", "vegan", "gluten-free"],
        nutrition={"calories": 480, "protein": 14, "carbs": 75, "fat": 15},
        ingredients=[
            {"name": "sweet potato", "amount": 1, "unit": "pcs"},
            {"name": "canned chickpeas", "amount": 0.5, "unit": "can"},
            {"name": "coconut milk", "amount": 0.5, "unit": "cup"},
            {"name": "spinach", "amount": 1, "unit": "cup"},
            {"name": "onion", "amount": 0.5, "unit": "pcs"},
            {"name": "curry paste", "amount": 1, "unit": "tbsp"},
            {"name": "ginger", "amount": 1, "unit": "tsp"},
            {"name": "brown rice", "amount": 1, "unit": "cup"}
        ]
    ),
    Recipe(
        name="Vegetarian Enchiladas",
        cost=7.50,
        cook_time=40,
        dietary_tags=["vegetarian"],
        nutrition={"calories": 520, "protein": 20, "carbs": 65, "fat": 22},
        ingredients=[
            {"name": "corn tortillas", "amount": 3, "unit": "pcs"},
            {"name": "black beans", "amount": 0.5, "unit": "can"},
            {"name": "corn", "amount": 0.5, "unit": "cup"},
            {"name": "enchilada sauce", "amount": 1, "unit": "cup"},
            {"name": "shredded cheese", "amount": 0.5, "unit": "cup"},
            {"name": "bell pepper", "amount": 0.5, "unit": "pcs"},
            {"name": "onion", "amount": 0.25, "unit": "pcs"},
            {"name": "sour cream", "amount": 2, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Tofu Soba Noodle Bowl",
        cost=8.25,
        cook_time=20,
        dietary_tags=["vegetarian", "vegan"],
        nutrition={"calories": 450, "protein": 24, "carbs": 60, "fat": 14},
        ingredients=[
            {"name": "soba noodles", "amount": 80, "unit": "g"},
            {"name": "extra firm tofu", "amount": 150, "unit": "g"},
            {"name": "edamame", "amount": 0.5, "unit": "cup"},
            {"name": "shredded carrots", "amount": 0.5, "unit": "cup"},
            {"name": "soy sauce", "amount": 2, "unit": "tbsp"},
            {"name": "rice vinegar", "amount": 1, "unit": "tbsp"},
            {"name": "sesame oil", "amount": 1, "unit": "tsp"},
            {"name": "green onion", "amount": 1, "unit": "stalk"}
        ]
    ),
    Recipe(
        name="Mushroom Stroganoff",
        cost=7.00,
        cook_time=25,
        dietary_tags=["vegetarian"],
        nutrition={"calories": 490, "protein": 15, "carbs": 60, "fat": 24},
        ingredients=[
            {"name": "egg noodles", "amount": 100, "unit": "g"},
            {"name": "cremini mushrooms", "amount": 200, "unit": "g"},
            {"name": "vegetable broth", "amount": 0.5, "unit": "cup"},
            {"name": "sour cream", "amount": 0.25, "unit": "cup"},
            {"name": "onion", "amount": 0.5, "unit": "pcs"},
            {"name": "garlic", "amount": 2, "unit": "cloves"},
            {"name": "dior mustard", "amount": 1, "unit": "tsp"},
            {"name": "paprika", "amount": 1, "unit": "tsp"}
        ]
    ),
    Recipe(
        name="Pesto Gnocchi with Veggies",
        cost=9.00,
        cook_time=15,
        dietary_tags=["vegetarian"],
        nutrition={"calories": 560, "protein": 14, "carbs": 70, "fat": 28},
        ingredients=[
            {"name": "potato gnocchi", "amount": 150, "unit": "g"},
            {"name": "basil pesto", "amount": 3, "unit": "tbsp"},
            {"name": "cherry tomatoes", "amount": 8, "unit": "pcs"},
            {"name": "baby spinach", "amount": 1, "unit": "cup"},
            {"name": "parmesan cheese", "amount": 2, "unit": "tbsp"},
            {"name": "pine nuts", "amount": 1, "unit": "tbsp"},
            {"name": "garlic", "amount": 1, "unit": "clove"}
        ]
    ),

    # --- INTERNATIONAL & FUSION ---
    Recipe(
        name="Chicken Gyro Salad",
        cost=9.25,
        cook_time=15,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 410, "protein": 36, "carbs": 12, "fat": 26},
        ingredients=[
            {"name": "chicken breast", "amount": 150, "unit": "g"},
            {"name": "romaine lettuce", "amount": 2, "unit": "cups"},
            {"name": "cucumber", "amount": 0.5, "unit": "pcs"},
            {"name": "cherry tomatoes", "amount": 6, "unit": "pcs"},
            {"name": "feta cheese", "amount": 30, "unit": "g"},
            {"name": "tzatziki sauce", "amount": 2, "unit": "tbsp"},
            {"name": "red onion", "amount": 0.1, "unit": "pcs"},
            {"name": "kalamata olives", "amount": 5, "unit": "pcs"}
        ]
    ),
    Recipe(
        name="Beef Yakisoba",
        cost=11.50,
        cook_time=20,
        dietary_tags=["high-protein"],
        nutrition={"calories": 620, "protein": 34, "carbs": 75, "fat": 20},
        ingredients=[
            {"name": "yakisoba noodles", "amount": 150, "unit": "g"},
            {"name": "beef strips", "amount": 120, "unit": "g"},
            {"name": "cabbage", "amount": 1, "unit": "cup"},
            {"name": "carrots", "amount": 0.5, "unit": "cup"},
            {"name": "yakisoba sauce", "amount": 3, "unit": "tbsp"},
            {"name": "onion", "amount": 0.25, "unit": "pcs"},
            {"name": "ginger", "amount": 1, "unit": "tsp"},
            {"name": "garlic", "amount": 1, "unit": "clove"}
        ]
    ),
    Recipe(
        name="Moroccan Lamb Tagine",
        cost=14.00,
        cook_time=55,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 580, "protein": 36, "carbs": 45, "fat": 28},
        ingredients=[
            {"name": "lamb cubes", "amount": 180, "unit": "g"},
            {"name": "apricots", "amount": 5, "unit": "pcs"},
            {"name": "chickpeas", "amount": 0.25, "unit": "can"},
            {"name": "onion", "amount": 0.5, "unit": "pcs"},
            {"name": "cinnamon", "amount": 0.5, "unit": "tsp"},
            {"name": "cumin", "amount": 1, "unit": "tsp"},
            {"name": "ginger", "amount": 1, "unit": "tsp"},
            {"name": "couscous", "amount": 0.5, "unit": "cup"},
            {"name": "sliced almonds", "amount": 1, "unit": "tbsp"}
        ]
    ),

    # --- QUICK & LITE ---
    Recipe(
        name="Caprese Chicken Pasta",
        cost=10.00,
        cook_time=20,
        dietary_tags=["high-protein"],
        nutrition={"calories": 590, "protein": 42, "carbs": 60, "fat": 22},
        ingredients=[
            {"name": "penne pasta", "amount": 100, "unit": "g"},
            {"name": "chicken breast", "amount": 150, "unit": "g"},
            {"name": "cherry tomatoes", "amount": 10, "unit": "pcs"},
            {"name": "fresh mozzarella", "amount": 50, "unit": "g"},
            {"name": "balsamic glaze", "amount": 1, "unit": "tbsp"},
            {"name": "fresh basil", "amount": 4, "unit": "leaves"},
            {"name": "garlic", "amount": 2, "unit": "cloves"},
            {"name": "olive oil", "amount": 1, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Turkey Burger with Sweet Potato Fries",
        cost=8.75,
        cook_time=30,
        dietary_tags=["high-protein"],
        nutrition={"calories": 560, "protein": 34, "carbs": 50, "fat": 24},
        ingredients=[
            {"name": "ground turkey", "amount": 150, "unit": "g"},
            {"name": "burger bun", "amount": 1, "unit": "pcs"},
            {"name": "sweet potato", "amount": 1, "unit": "pcs"},
            {"name": "lettuce", "amount": 1, "unit": "leaf"},
            {"name": "tomato slice", "amount": 2, "unit": "pcs"},
            {"name": "onion slice", "amount": 1, "unit": "pcs"},
            {"name": "avocado mayo", "amount": 1, "unit": "tbsp"},
            {"name": "olive oil", "amount": 1, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Lentil Bolognese",
        cost=5.00,
        cook_time=30,
        dietary_tags=["vegetarian", "vegan"],
        nutrition={"calories": 440, "protein": 20, "carbs": 75, "fat": 6},
        ingredients=[
            {"name": "brown lentils", "amount": 0.75, "unit": "cup"},
            {"name": "spaghetti", "amount": 100, "unit": "g"},
            {"name": "crushed tomatoes", "amount": 1, "unit": "cup"},
            {"name": "carrot", "amount": 0.5, "unit": "pcs"},
            {"name": "celery", "amount": 1, "unit": "stalk"},
            {"name": "onion", "amount": 0.25, "unit": "pcs"},
            {"name": "garlic", "amount": 2, "unit": "cloves"},
            {"name": "italian herbs", "amount": 1, "unit": "tsp"}
        ]
    ),
    Recipe(
        name="Shrimp & Avocado Salad",
        cost=13.00,
        cook_time=10,
        dietary_tags=["high-protein", "gluten-free", "low-carb"],
        nutrition={"calories": 380, "protein": 32, "carbs": 14, "fat": 24},
        ingredients=[
            {"name": "shrimp", "amount": 180, "unit": "g"},
            {"name": "avocado", "amount": 1, "unit": "pcs"},
            {"name": "mixed greens", "amount": 2, "unit": "cups"},
            {"name": "cucumber", "amount": 0.5, "unit": "pcs"},
            {"name": "lemon", "amount": 0.5, "unit": "pcs"},
            {"name": "olive oil", "amount": 1, "unit": "tbsp"},
            {"name": "red pepper flakes", "amount": 0.5, "unit": "tsp"},
            {"name": "cilantro", "amount": 1, "unit": "tbsp"}
        ]
    ),
    Recipe(
        name="Peanut Chicken Satay with Cucumber Salad",
        cost=11.00,
        cook_time=25,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={"calories": 520, "protein": 40, "carbs": 20, "fat": 32},
        ingredients=[
            {"name": "chicken breast", "amount": 200, "unit": "g"},
            {"name": "peanut butter", "amount": 2, "unit": "tbsp"},
            {"name": "coconut milk", "amount": 2, "unit": "tbsp"},
            {"name": "soy sauce", "amount": 1, "unit": "tbsp"},
            {"name": "lime juice", "amount": 1, "unit": "tbsp"},
            {"name": "cucumber", "amount": 1, "unit": "pcs"},
            {"name": "red onion", "amount": 0.25, "unit": "pcs"},
            {"name": "rice vinegar", "amount": 1, "unit": "tbsp"},
            {"name": "honey", "amount": 1, "unit": "tsp"}
        ]
    )
]