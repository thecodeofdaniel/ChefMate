import customtkinter as ctk

app = ctk.CTk()
app.title("ChefMate")
app.configure(padx=100, pady=100)

# Set dark/light mode based on system
ctk.set_appearance_mode("system")
# Add custom theme
ctk.set_default_color_theme("./theme.json")

# Create a label above the input frame
label = ctk.CTkLabel(
    app,
    text="Enter ingredients",
    font=ctk.CTkFont(size=24, weight="bold"),
    pady=10,
)
label.grid(row=0, column=0, columnspan=2)  # Center the label in the first row

# Create a frame to contain the entry box and button
input_frame = ctk.CTkFrame(app)
input_frame.grid(row=1, column=0, columnspan=2)  # Center the frame in the second row

# Create an entry box inside the input frame
entry = ctk.CTkEntry(
    input_frame,
    width=300,
    placeholder_text="chicken breast, garlic, salt"
)
entry.grid(row=0, column=0)

# Create a button inside the input frame
button = ctk.CTkButton(
    input_frame,
    text="Search",
    width=20,
)
button.grid(row=0, column=1)


# Configure column weights for centering content
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Configure row weight for centering content vertically
app.grid_rowconfigure(1, weight=0)

# Run the tkinter main loop
app.mainloop()
