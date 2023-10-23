import customtkinter as ctk
import os
from PIL import Image
import requests, json
import api_file

# Grab the directory where this file is being run
CURR_DIR = os.path.dirname(os.path.abspath(__file__))

# Set dark/light mode based on system
ctk.set_appearance_mode("system")

# Add custom theme
ctk.set_default_color_theme(f"{CURR_DIR}/theme.json")

class ScrollableRecipes(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)

        self.command = command
        self.label_list = []
        self.textbox_list = []

    def add_item(self, item, image=None):
        name = ctk.CTkLabel(
            self,
            text=item,
            image=image,
            compound="top",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        textbox = ctk.CTkTextbox(
            self,
        )

        name.grid(
            row=len(self.label_list),
            column=0,
            pady=(0,10),
            padx=10,
        )

        textbox.grid(
            row=len(self.textbox_list),
            column=1,
            pady=(0,30),
            sticky="nsew"
        )

        self.label_list.append(name)
        self.textbox_list.append(textbox)

    # def remove_item(self, item):
    #     for label, button in zip(self.label_list, self.button_list):
    #         if item == label.cget("text"):
    #             label.destroy()
    #             button.destroy()
    #             self.label_list.remove(label)
    #             self.button_list.remove(button)
    #             return

# Create the UI
class ChefMate(ctk.CTk):
    width = 700
    height = 800

    def __init__(self) -> None:
        super().__init__()
        self.title("ChefMate")
        self.geometry(f"{self.width}x{self.height}")

        # Center content
        self.grid_columnconfigure(0, weight=1)

        # Add title above search bar
        self.search_title = ctk.CTkLabel(
            self,
            text="Enter ingredients",
            pady=10,
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.search_title.grid(row=0, column=0, columnspan=2)

        # Create the frame that will contain the search box and button
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=1, column=0, columnspan=2)

        # Create search box
        self.search_box = ctk.CTkEntry(
            self.search_frame,
            width=300,
            placeholder_text="chicken breast, garlic, salt"
        )
        self.search_box.grid(row=0, column=0)

        # Create search button
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=20,
            command=self.search_recipes
        )
        self.search_button.grid(row=0, column=1)

        # Create scrollable frame containing the recipes
        self.recipes = ScrollableRecipes(
            self,
            width=800,
            height=700,
            corner_radius=0
        )
        self.recipes.grid(row=3, column=0, padx=0, pady=30, sticky="nsew")

        # Add some recipes
        for i in range(2):
            self.recipes.add_item(
                f"Recipe {i}",
                image=ctk.CTkImage(
                    Image.open(os.path.join(CURR_DIR, "images", "salmon.jpg")),
                    size=(300,300)
                )
            )

    def search_recipes(self):
        ingredients = self.search_box._entry.get()

        # TODO: Create a function to format the input.
        # For example remove any extra spaces between words between commas.
        # As well as remove any space before/after the comma
        #   Ex. chicken   breast  ,     salt -> chicken breast,salt
        # Then remove any space and replace with underscore.
        #   Ex. chicken breast,salt -> chicken_breast,salt
        
    def format_user_input(user_input):
        # Removes any extra spaces between words
        user_input = ' '.join(user_input.split())
        
        # Removes spaces before and after commas
        user_input = user_input.replace(' ,', ',').replace(', ', ',')
        
        # Replace spaces with underscores
        user_input = user_input.replace(' ', '_')
        
        return user_input


        # TODO: Once you've formatted the input from the user. Make the API call
        # with the base url. Output the response to the terminal.

    BASE_URL = f"https://www.themealdb.com/api/json/v2/{api_file.api_key}/filter.php?i="

    # Prompt the user to enter ingredient
    INGREDIENT = input("Enter Ingredient: ")

    INGREDIENT = format_user_input(INGREDIENT)

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
    selected_id_meal = None

    for meal_id, meal_name in meal_dict.items():
        if meal_name == selected_meal_name:
            selected_id_meal = meal_id
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

                break

    #Error handling if meal is not found
    else:
        print("Meal not found!")

chefmate = ChefMate()
chefmate.mainloop()
