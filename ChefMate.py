import requests, json
import api_file
from config import BASE_URL

# Prompt the user to enter ingredient
INGREDIENT = input("Enter Ingredient: ")

URL = BASE_URL + INGREDIENT

response = requests.get(URL)
response_dictionary = response.json()

meal_dict = {meal["idMeal"]: meal["strMeal"] for meal in response_dictionary["meals"]}

print("Meal Options:")
for meal in response_dictionary["meals"]:
    print(f"- {meal['strMeal']} (Preview: {meal['strMealThumb']})")
print("\n")

# Prompt the user to enter a meal name
selected_meal_name = input("Enter a meal name from the above list: ")

# Find the idMeal corresponding to the entered meal name
selected_id_meal = next((id for id, name in meal_dict.items() if name == selected_meal_name), None)

#Error handling if meal is not found
if not selected_id_meal:
    print("Meal not found!")
else:
    # Fetch the recipe
    RECIPE_URL = f"https://www.themealdb.com/api/json/v2/{api_file.api_key}/lookup.php?i={selected_id_meal}"
    recipe_response = requests.get(RECIPE_URL)
    recipe_data = recipe_response.json()
    meal_details = recipe_data["meals"][0]

    # Display meal details in a more organized format
    print("\nRecipe for", meal_details["strMeal"])
    print("Category:", meal_details["strCategory"])
    print("Region:", meal_details["strArea"])
    print("\nIngredients:")
    for i in range(1, 21):
        ingredient = meal_details[f"strIngredient{i}"]
        measure = meal_details[f"strMeasure{i}"]
        if ingredient and ingredient.strip() != "":
            print(f"- {ingredient.strip()} ({measure.strip()})")

    print("\nInstructions:")
    print(meal_details["strInstructions"].strip())

    # If there's a YouTube link, display it
    if meal_details["strYoutube"]:
        print("\nWatch the recipe on YouTube:", meal_details["strYoutube"])