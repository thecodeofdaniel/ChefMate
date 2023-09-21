import requests, json
import api_file

BASE_URL = f"https://www.themealdb.com/api/json/v2/{api_file.api_key}/filter.php?i="


INGREDIENT = input("Enter Ingredient: ")

URL = BASE_URL + INGREDIENT

response = requests.get(URL)
response_dictionary = response.json()

print(json.dumps(response_dictionary, indent=4, sort_keys=True))
