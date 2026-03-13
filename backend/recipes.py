from .dataset_builders import load_cached_dataset, build_balanced_dataset

RECIPES = load_cached_dataset()

if RECIPES is None:
    print("Retreving recipes from APIs...")
    build_balanced_dataset()
    RECIPES = load_cached_dataset()