from .models import Recipe

RECIPES = [
    Recipe(
        name="Chicken Rice Bowl",
        cost=6.75,
        cook_time=25,
        dietary_tags=["high-protein", "gluten-free"],
        nutrition={
            "calories": 520,
            "protein": 42,
            "carbs": 55,
            "fat": 12
        },
        ingredients={
            "chicken breast": 200,
            "white rice": 150,
            "olive oil": 10
        }
    ),

    Recipe(
        name="Vegetable Stir Fry",
        cost=5.25,
        cook_time=15,
        dietary_tags=["vegetarian", "vegan"],
        nutrition={
            "calories": 410,
            "protein": 18,
            "carbs": 60,
            "fat": 14
        },
        ingredients={
            "tofu": 150,
            "mixed vegetables": 200,
            "soy sauce": 15
        }
    ),

    Recipe(
        name="Turkey Avocado Wrap",
        cost=6.00,
        cook_time=10,
        dietary_tags=["high-protein"],
        nutrition={
            "calories": 460,
            "protein": 35,
            "carbs": 40,
            "fat": 18
        },
        ingredients={
            "turkey breast": 120,
            "tortilla": 1,
            "avocado": 75
        }
    ),

    Recipe(
        name="Pasta with Marinara",
        cost=4.75,
        cook_time=20,
        dietary_tags=["vegetarian"],
        nutrition={
            "calories": 580,
            "protein": 20,
            "carbs": 85,
            "fat": 10
        },
        ingredients={
            "pasta": 180,
            "marinara sauce": 150
        }
    ),

    Recipe(
        name="Salmon Quinoa Bowl",
        cost=8.50,
        cook_time=30,
        dietary_tags=["gluten-free", "high-protein"],
        nutrition={
            "calories": 600,
            "protein": 45,
            "carbs": 50,
            "fat": 20
        },
        ingredients={
            "salmon": 180,
            "quinoa": 120,
            "lemon": 30
        }
    )
]
