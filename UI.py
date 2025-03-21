import tkinter as tk
from tkinter import ttk
import subprocess

# Function to handle button click
def on_select(option):
    global combo
    global search_domains
    label.destroy()
    global standardPSO
    standardPSO = "1"

    search_domains = [
        "Sphere",
        "Rosenbrock",
        "Ackley",
        "Griewank",
        "Rastrigin",
        "Schaffer2D",
        "Shifted Sphere",
        "Shifted Schwefel",
        "Shifted and Rotated Elliptic",
        "Schwefel shifted with Noise",
        "El-Attar-Vidyasagar-Dutta",
        "Weierstrass",
        "Shifted Rotated Griewank",
        "Shifted Rotated Ackley",
        "Shifted Rastrigin",
        "Shifted Rotated Rastrigin",
        "Weirstrass shifted and Rotated",
        "Schwefel",
        "Griewank plus Rosenbrock, Amplified and Dampened",
        "Ridge",
        "Shekel-25",
        "Shubert-3",
        "Trid",
        "Egg Crate",
        "Himmelblau",
        "Holder Table Function",
        "Keane Function",
        "Bird Function",
        "Xin-She Yang N.4",
        "Cross-in-Tray",
        "Schwefel 2.21"
    ]

    # if visualise search domain is selected
    if option == 0:
        funcSelect = tk.Label(root, text="Choose a Search Domain:", font=("Arial", 12))
        funcSelect.pack(pady=10)

        combo = ttk.Combobox(root, values=search_domains)
        combo.pack(pady=10)
        combo.bind("<<ComboboxSelected>>", pass_domain)
    else:
        subprocess.run(["python", "evaluate.py"] + search_domains)  # Run script_b.py

# passes selected domain to visualise to searchDomain.py
def pass_domain(event):
    selected_value = combo.get()
    subprocess.run(["python", "visualise.py", selected_value] + search_domains)
    #print(f"Selected: {selected_value}")

# Create main window
root = tk.Tk()
root.title("Select an Option")
root.geometry("500x300")

# Label
label = tk.Label(root, text="Choose an option:", font=("Arial", 12))
label.pack(pady=10)

# Buttons for options
btn1 = tk.Button(root, text="Visualise Standard PSO", command=lambda: on_select(0), width=25)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Run Standard PSO on all Search Domains", command=lambda: on_select(1), width=40)
btn2.pack(pady=5)

# Run the UI
root.mainloop()
    