import customtkinter as ctk


# Set dark/light mode based on system
ctk.set_appearance_mode("system")

# Add custom theme
ctk.set_default_color_theme("./theme.json")

# Create the UI
class ChefMate(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ChefMate")
        self.configure(padx=20, pady=20)

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
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            label_text="Recipes",
            width=800,
        )
        self.scroll_frame.grid(row=2, column=0, pady=20, columnspan=2)

    def search_recipes(self):
        ingredients = self.search_box._entry.get()

        # TODO: Create a function to format the input.
        # For example remove any extra spaces between words between commas.
        # As well as remove any space before/after the comma
        #   Ex. chicken   breast  ,     salt -> chicken breast,salt
        # Then remove any space and replace with underscore.
        #   Ex. chicken breast,salt -> chicken_breast,salt

        # TODO: Once you've formatted the input from the user. Make the API call
        # with the base url. Output the response to the terminal.

chefmate = ChefMate()
chefmate.mainloop()
