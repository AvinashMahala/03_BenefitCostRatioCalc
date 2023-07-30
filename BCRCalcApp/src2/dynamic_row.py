import tkinter as tk
from tkinter import ttk

class DynamicRow(ttk.Frame):
    def __init__(self, container, controller, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller

        self.element_type_var = tk.StringVar()
        self.defect_var = tk.StringVar()
        self.bid_item_var = tk.StringVar()
        self.intervention_description_var = tk.StringVar()
        self.unit_of_measure_var = tk.StringVar()
        self.unit_price_var = tk.StringVar()
        self.quantity_var = tk.StringVar()

        element_type_values = ['Element1', 'Element2', 'Element3']
        self.element_type_dropdown = ttk.Combobox(self, textvariable=self.element_type_var, values=element_type_values, state="readonly")
        self.element_type_dropdown.grid(column=0, row=0)
        self.element_type_dropdown.bind('<<ComboboxSelected>>', self.on_element_type_selected)

        self.defect_dropdown = ttk.Combobox(self, textvariable=self.defect_var, state='disabled')
        self.defect_dropdown.grid(column=1, row=0)
        self.defect_dropdown.bind('<<ComboboxSelected>>', self.on_defect_selected)

        self.bid_item_dropdown = ttk.Combobox(self, textvariable=self.bid_item_var, state='disabled')
        self.bid_item_dropdown.grid(column=2, row=0)
        self.bid_item_dropdown.bind('<<ComboboxSelected>>', self.on_bid_item_selected)

        self.intervention_description_entry = ttk.Entry(self, textvariable=self.intervention_description_var, state='readonly')
        self.intervention_description_entry.grid(column=3, row=0)

        self.unit_of_measure_entry = ttk.Entry(self, textvariable=self.unit_of_measure_var, state='readonly')
        self.unit_of_measure_entry.grid(column=4, row=0)

        self.unit_price_entry = ttk.Entry(self, textvariable=self.unit_price_var, state='readonly')
        self.unit_price_entry.grid(column=5, row=0)

        self.quantity_entry = ttk.Entry(self, textvariable=self.quantity_var, state='disabled')
        self.quantity_entry.grid(column=6, row=0)

    def on_element_type_selected(self, event):
        selected_option = self.element_type_var.get()

        defect_options = ['Defect1', 'Defect2', 'Defect3']  # Replace this with a function call to fetch options from the database
        self.defect_dropdown['values'] = defect_options
        self.defect_dropdown['state'] = 'readonly'

    def on_defect_selected(self, event):
        bid_item_options = ['Bid1', 'Bid2', 'Bid3']  # Replace this with a function call to fetch options from the database
        self.bid_item_dropdown['values'] = bid_item_options
        self.bid_item_dropdown['state'] = 'readonly'

    def on_bid_item_selected(self, event):
        bid_item = self.bid_item_var.get()

        description = 'Demo Description'  # Replace this with a function call to fetch description from the database
        self.intervention_description_var.set(description)

        unit_of_measure = 'Demo Unit'  # Replace this with a function call to fetch unit of measure from the database
        self.unit_of_measure_var.set(unit_of_measure)

        unit_price = '10.00'  # Replace this with a function call to fetch unit price from the database
        self.unit_price_var.set(unit_price)

        self.quantity_entry['state'] = 'normal'

    def calculate_cost(self):
        # Replace with your actual calculation logic
        quantity = int(self.quantity_var.get())
        unit_price = float(self.unit_price_var.get())
        cost = quantity * unit_price
        return cost
