import os
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Define the function to plot the chains
def plot_chains(directory, chain_base_name, param_name, num_chains):
    all_param_values = {}

    # Iterate over all chain files
    for i in range(1, num_chains + 1):
        file_name = os.path.join(directory, f'{chain_base_name}.{i}.txt')

        with open(file_name, 'r') as f:
            lines = f.readlines()

        # Find the column index for the parameter
        header = lines[0].strip().split()
        param_index = None

        for j, name in enumerate(header):
            if name.lower() == param_name.lower():  # Use exact match for the parameter name
                param_index = j - 1
                break

        if param_index is None:
            print(f"Parameter '{param_name}' not found in file {file_name}.")
            continue

        # Initialize a list to store parameter values for this chain
        param_values = []

        # Parse the chain file starting from the second line (skip header)
        for line in lines[1:]:
            line = line.strip()

            # Skip empty lines and non-data lines
            if not line or not line[0].isdigit():
                continue

            # Split each line by whitespace
            values = line.split()

            try:
                # Extract the parameter value
                param_value = float(values[param_index])
                param_values.append(param_value)
            except ValueError:
                print(f"Skipping line due to conversion error: {line}")

        # Store the parameter values for this chain in a dictionary
        all_param_values[f'Chain {i}'] = np.array(param_values)

    # Create subplots
    num_rows = int(np.ceil(num_chains / 2))  # Calculate the required number of rows for two columns
    plt.figure(figsize=(20, 12))

    for idx, (chain_name, param_array) in enumerate(all_param_values.items(), start=1):
        plt.subplot(num_rows, 2, idx)
        plt.plot(param_array)
        plt.ylabel(param_name)
        plt.title(chain_name)
        plt.grid(True)

    # Adjust subplot spacing
    plt.tight_layout()
    plt.show()

# Define the function to select a directory
def select_directory():
    directory = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, directory)

# Define the function to start plotting
def start_plotting():
    directory = folder_entry.get()
    chain_base_name = chain_name_entry.get().strip()
    param_name = param_entry.get().strip()
    try:
        num_chains = int(chain_number_entry.get().strip())
    except ValueError:
        print("Please enter a valid number of chains.")
        return

    plot_chains(directory, chain_base_name, param_name, num_chains)

# Create the main window
root = ttk.Window(themename="cosmo", size=[1600, 800], scaling=2)
root.title("Cobaya Chains Plotter")
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12))  # Increase label font size
style.configure('TButton', font=('Helvetica', 12))  # Increase button font size
style.configure('TEntry', font=('Helvetica', 12))  # Increase entry font size

# Folder selection frame
folder_frame = ttk.Frame(root)
folder_frame.pack(padx=20, pady=20, fill=X)

folder_label = ttk.Label(folder_frame, text="Select Chains Directory")
folder_label.pack(side=LEFT)

folder_entry = ttk.Entry(folder_frame, width=50)
folder_entry.pack(side=LEFT, padx=10)

folder_button = ttk.Button(folder_frame, text="Browse", command=select_directory, bootstyle=PRIMARY)
folder_button.pack(side=LEFT)

# Chain name input frame
chain_frame = ttk.Frame(root)
chain_frame.pack(padx=20, pady=20, fill=X)

chain_name_label = ttk.Label(chain_frame, text="Chain Base Name (e.g., test)")
chain_name_label.pack(side=LEFT)

# Set default chain base name to "test"
chain_name_entry = ttk.Entry(chain_frame, width=50)
chain_name_entry.insert(0, "test")
chain_name_entry.pack(side=LEFT, padx=10)

# Chain number input frame
chain_number_frame = ttk.Frame(root)
chain_number_frame.pack(padx=20, pady=20, fill=X)

chain_number_label = ttk.Label(chain_number_frame, text="Number of Chains")
chain_number_label.pack(side=LEFT)

# Set default number of chains to "8"
chain_number_entry = ttk.Entry(chain_number_frame, width=50)
chain_number_entry.insert(0, "8")
chain_number_entry.pack(side=LEFT, padx=10)

# Parameter name input frame
param_frame = ttk.Frame(root)
param_frame.pack(padx=20, pady=20, fill=X)

param_label = ttk.Label(param_frame, text="Parameter Name")
param_label.pack(side=LEFT)

# Set default parameter name to "chi2"
param_entry = ttk.Entry(param_frame, width=50)
param_entry.insert(0, "chi2")
param_entry.pack(side=LEFT, padx=10)

# Plot button
plot_button = ttk.Button(root, text="Plot Chains", command=start_plotting, bootstyle=PRIMARY)
plot_button.pack(side=LEFT, padx=20, pady=20)

# Run the main loop
root.mainloop()
