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

        self.calculation_button = ttk.Button(self.homepage_area, text="Generate Unique Calculation", command=self.generate_calculation, width=30)
        self.calculation_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        # Adjust the height of the button by adding padding to the text
        self.calculation_button.config(padding=(0, 15))

        # Set the background color to red using the style
        # style = ttk.Style(self)
        # style.configure('Background.TFrame', background='#e6e7e8')
        # self.homepage_area.configure(style='Background.TFrame')


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


