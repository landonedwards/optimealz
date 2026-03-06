from .dataset_builder import load_cached_dataset, build_dataset

RECIPES = load_cached_dataset()

if RECIPES is None:
    print("Retreving recipes from APIs...")
    build_dataset()
    RECIPES = load_cached_dataset