import tkinter as tk
from tkinter import ttk
from dynamic_row import DynamicRow

class DeckTab(ttk.Frame):
    def __init__(self, container, controller, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller

        self.actions_area = ttk.LabelFrame(self, text="Actions Area")
        self.actions_area.pack(fill="both", expand=True)
        
        self.uuid_label_var = tk.StringVar(value="UUID: Placeholder")  # replace Placeholder with actual UUID
        self.uuid_label = ttk.Label(self.actions_area, textvariable=self.uuid_label_var)
        self.uuid_label.pack()

        self.add_row_button = ttk.Button(self.actions_area, text="Add Row", command=self.add_row)
        self.add_row_button.pack()
        
        self.calculation_form_area = ttk.LabelFrame(self, text="Calculation Form Area")
        self.calculation_form_area.pack(fill="both", expand=True)

        self.final_cost_area = ttk.LabelFrame(self, text="Final Cost Area")
        self.final_cost_area.pack(fill="both", expand=True)

        self.calculate_final_cost_button = ttk.Button(self.final_cost_area, text="Calculate Final", command=self.calculate_final_cost)
        self.calculate_final_cost_button.pack()

        self.final_cost_label_var = tk.StringVar()
        self.final_cost_label = ttk.Label(self.final_cost_area, textvariable=self.final_cost_label_var)
        self.final_cost_label.pack()

        self.dynamic_rows = []
        for _ in range(1):  # replace with the actual number of rows you want
            self.add_row()

    def add_row(self):
        if len(self.dynamic_rows) >= 10:
            tk.messagebox.showerror("Error", "Cannot add more than 10 rows.")
            return

        row = DynamicRow(self.calculation_form_area, self.controller)
        row.pack()
        self.dynamic_rows.append(row)

    def calculate_final_cost(self):
        final_cost = sum(row.calculate_cost() for row in self.dynamic_rows)
        self.final_cost_label_var.set(f"Final Cost: {final_cost}")
