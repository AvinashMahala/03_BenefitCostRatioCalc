#This file will contain the Homepage class.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import uuid

class Homepage(ttk.Frame):
    def __init__(self, master=None, notebook=None):
        super().__init__(master)
        self.notebook = notebook
        self.create_widgets()
        self.uuid=""
        self.bridgeId=""

    def create_widgets(self):
        self.homepage_area = ttk.LabelFrame(self, text="HomePage Area", padding=10)
        self.homepage_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        label_font = ("Arial", 12, "bold")
        entry_font = ("Arial", 12)
        button_font = ("Arial", 12, "bold")

        self.bridgeId_label_var = tk.StringVar(value="Input Bridge ID")
        self.bridgeId_label = ttk.Label(self.homepage_area, textvariable=self.bridgeId_label_var, font=label_font)
        self.bridgeId_label.grid(row=0, column=0, padx=5, pady=5)

        self.bridge_id_entry = ttk.Entry(self.homepage_area, font=entry_font)
        self.bridge_id_entry.grid(row=1, column=0, padx=5, pady=5)

        self.calculation_button = ttk.Button(self.homepage_area, text="Generate Unique Calculation", command=self.generate_calculation)
        self.calculation_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        # # Define a custom style for the button
        # self.style = ttk.Style()
        # self.style.configure("Accent.TButton",
        #                     foreground="white",
        #                     background="#32a852",  # A nice green color
        #                     font=button_font,
        #                     padding=10,
        #                     width=20)

        # Set a border for the button to make it more visible
        # self.style.map("Accent.TButton",
        #             foreground=[('pressed', 'white'), ('active', 'white')],
        #             background=[('pressed', '#22893d'), ('active', '#22893d')],
        #             relief=[('pressed', 'sunken'), ('!pressed', 'raised')])





    def generate_calculation(self):
        bridge_id = self.bridge_id_entry.get().strip()
        
        # Check if bridge_id is empty after stripping white spaces
        if not bridge_id:
            self.master.show_msg("Error: Bridge ID cannot be empty or spaces only.")
            return

        unique_id = str(uuid.uuid4())
        self.uuid=unique_id
        self.bridgeId=bridge_id
        self.master.database.insert_calculation_metadata(bridge_id, unique_id)
        self.master.activate_tabs(bridge_id, unique_id)
        self.master.show_msg(f"Successfully stored the Bridge ID: {bridge_id} and UUID: {unique_id}")


