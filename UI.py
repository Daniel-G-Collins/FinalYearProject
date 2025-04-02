import tkinter as tk
from tkinter import ttk
import subprocess

# Function to handle button click
def on_select(option):
    ###
    global combo
    global search_domains
    label.destroy()
    global standardPSO
    standardPSO = "1"
    global label_domain, combo_domain, label_particle_type, combo_particle_type, submit_button, label_topology, combo_topology
    if label_domain is not None:
        label_domain.destroy()
    if combo_domain is not None:
        combo_domain.destroy()
    if label_particle_type is not None:
        label_particle_type.destroy()
    if combo_particle_type is not None:
        combo_particle_type.destroy()
    if submit_button is not None:
        submit_button.destroy()
    if label_topology is not None:
        label_topology.destroy()
    if combo_topology is not None:
        combo_topology.destroy()
    ###
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
        swarmTypes = ["Standard", "Standard With Dampening Factor"]
        topologies = ["Global", "Ring", "VN"]

        # Label for search domain
        label_domain = tk.Label(root, text="Choose a Search Domain:", font=("Arial", 12))
        label_domain.pack(pady=10)

        # Combobox for search domain
        combo_domain = ttk.Combobox(root, values=search_domains)
        combo_domain.pack(pady=10)

        #Combobox and label for topology
        label_topology = tk.Label(root, text="Choose a Topology:", font=("Arial", 12))
        label_topology.pack(pady=10)

        combo_topology = ttk.Combobox(root, values=topologies)
        combo_topology.pack(pady=10)

        # Label for particle type
        label_particle_type = tk.Label(root, text="Choose a Swarm Type:", font=("Arial", 12))
        label_particle_type.pack(pady=10)
      
        # Combobox for particle type
        combo_particle_type = ttk.Combobox(root, values=swarmTypes)
        combo_particle_type.current(0)  # Set default selection to "Standard PSO"
        combo_particle_type.pack(pady=10)

        # Submit button
        submit_button = tk.Button(root, text="Submit", command=pass_domain, width=20)
        submit_button.pack(pady=20)
    else:
        subprocess.run(["python", "evaluate.py"] + search_domains)  # Run script_b.py

# passes selected domain to visualise to searchDomain.py
def pass_domain():
    selected_value = combo_domain.get()
    selected_particle_type = combo_particle_type.get()
    topology = combo_topology.get()
    subprocess.run(["python", "visualise.py", selected_value, topology, selected_particle_type] + search_domains)
    print(f"Selected: {selected_value}\nParticle Type: {selected_particle_type}")

# Create main window
root = tk.Tk()
root.title("Select an Option")
root.geometry("500x500")

# Label
label = tk.Label(root, text="Choose an option:", font=("Arial", 12))
label.pack(pady=10)

swarm_label = tk.Label(root, text="Choose a Swarm Type:", font=("Arial", 12))
swarm_label.pack(pady=10)

# Buttons for options
btn1 = tk.Button(root, text="Visualise Standard PSO", command=lambda: on_select(0), width=25)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Run Standard PSO on all Search Domains", command=lambda: on_select(1), width=40)
btn2.pack(pady=5)

label_domain = None
combo_domain = None
label_particle_type = None
combo_particle_type = None
submit_button = None
label_topology = None
combo_topology = None

# Run the UI
root.mainloop()
    