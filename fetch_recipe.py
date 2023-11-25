from config import MEAL_URL
import requests

def get_recipe_details(idMeal: str) -> (str, list[str]):
    # url to get recipe instructions and ingredients
    url = MEAL_URL + idMeal

    # Grab the json output
    response = requests.get(url)
    response = response.json()

    # Grab the instructions
    instructions = response["meals"][0]["strInstructions"]
    instructions = ' '.join(instructions.replace('\n', ' ').split()) # Format

    # Format ingredients
    ingredients = []
    for i in range(1, 21):
        ingredient_key = f'strIngredient{i}'
        measure_key = f'strMeasure{i}'

        ingredient = response['meals'][0][ingredient_key].strip()
        measure = response['meals'][0][measure_key].strip()

        # If the ingredient is empty, we reached the end of the ingredients
        if ingredient == "":
            break

        ingredients.append(f"{measure} {ingredient}")

    return instructions, ingredients
