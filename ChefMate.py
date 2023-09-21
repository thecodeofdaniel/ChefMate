import requests, json

BASE_URL = "https://www.themealdb.com/api/json/v1/1/filter.php?i="
API_KEY = "1"
INGREDIENT = input("Enter Ingredient: ")

URL = BASE_URL + INGREDIENT

response = requests.get(URL)
response_dictionary = response.json()

print(json.dumps(response_dictionary, indent=4, sort_keys=True))