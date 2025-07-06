import customtkinter as ctk
import subprocess
import webbrowser
from PIL import Image

# Create the main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SUMO Traffic Simulation")
app.geometry("500x400")

# Load the logo
try:
    logo = ctk.CTkImage(light_image=Image.open("logo.png"), size=(100, 100))
    logo_label = ctk.CTkLabel(app, image=logo, text="")
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Error loading logo: {e}")

# Project title
title_label = ctk.CTkLabel(app, text="SUMO Traffic Simulation", font=("Arial", 20))
title_label.pack(pady=5)

# Project description
desc_label = ctk.CTkLabel(app, text="A real-time traffic simulation using SUMO and Python.", wraplength=400)
desc_label.pack(pady=5)

# Function to start SUMO simulation
def start_simulation():
    subprocess.Popen(["python", "simulation.py"])

# Function to start Dash app
def start_dashboard():
    subprocess.Popen(["python", "dashboard.py"])  # Run the Dash server
    webbrowser.open("http://127.0.0.1:8050/")  # Open the Dash dashboard in the browser

# Start Simulation Button
start_button = ctk.CTkButton(app, text="Start Simulation", command=start_simulation)
start_button.pack(pady=10)

# Start Dashboard Button
dash_button = ctk.CTkButton(app, text="Start Dashboard", command=start_dashboard)
dash_button.pack(pady=10)

# Run the UI loop
app.mainloop()
