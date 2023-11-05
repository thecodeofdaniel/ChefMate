import customtkinter as ctk
import os
from PIL import Image
import requests, json
from config import BASE_URL

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

    def add_item(self, recipe_name, image=None):
        # Recipe Label
        name = ctk.CTkLabel(
            self,
            text=recipe_name,
            image=image,
            compound="top",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        name.grid(
            row=len(self.label_list),
            column=0,
            pady=(0,10),
            padx=0,
        )
        # Recipe instructions
        textbox = ctk.CTkTextbox(
            self,
        )
        textbox.grid(
            row=len(self.textbox_list),
            column=1,
            pady=(0,30),
            sticky="nsew"
        )

        # Add recipe label to list
        self.label_list.append(name)
        # Add recipe instructions to list
        self.textbox_list.append(textbox)

    def remove_recipes(self):
        for label, textbox in zip(self.label_list, self.textbox_list):
            print(label.cget("text"))
            label.destroy()
            textbox.destroy()
        self.label_list.clear()
        self.textbox_list.clear()


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
            corner_radius=0,
        )
        self.recipes.grid(column=0, padx=30, pady=20, sticky="nsew")

        # Add some recipes
        for i in range(2):
            self.recipes.add_item(
                f"Recipe {i}",
                image=ctk.CTkImage(
                    Image.open(os.path.join(CURR_DIR, "images", "salmon.jpg")),
                    size=(300,300)
                )
            )

        # self.recipes.remove_recipes()

    def search_recipes(self):
        ingredients = str(self.search_box._entry.get())   # Get ingredients from searchbox
        ingredients = self.format_user_input(ingredients) # Format input for API call
        url = BASE_URL + ingredients
        response = requests.get(url)
        print(response.json())


    def format_user_input(self, user_input):
        # Removes any extra spaces between words
        user_input = ' '.join(user_input.split())

        # Removes spaces before and after commas
        user_input = user_input.replace(' ,', ',').replace(', ', ',')

        # Replace spaces with underscores
        user_input = user_input.replace(' ', '_')

        return user_input


chefmate = ChefMate()
chefmate.mainloop()
