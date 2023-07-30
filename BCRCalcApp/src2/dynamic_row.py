import tkinter as tk
from tkinter import ttk

class DynamicRow(ttk.Frame):
    def __init__(self, container, controller, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller

        # Named frames
        self.bridge_info_frame = ttk.LabelFrame(self, text="Bridge Information")
        self.condition_state_1_frame = ttk.LabelFrame(self, text="Condition State 1")
        self.condition_state_2_frame = ttk.LabelFrame(self, text="Condition State 2")
        self.condition_state_3_frame = ttk.LabelFrame(self, text="Condition State 3")
        self.condition_state_4_frame = ttk.LabelFrame(self, text="Condition State 4")
        self.actions_frame = ttk.LabelFrame(self, text="Actions")
        self.cost_info_frame = ttk.LabelFrame(self, text="Cost Information")

        # Position frames
        self.bridge_info_frame.grid(column=0, row=0)
        self.condition_state_1_frame.grid(column=1, row=0)
        self.condition_state_2_frame.grid(column=2, row=0)
        self.condition_state_3_frame.grid(column=3, row=0)
        self.condition_state_4_frame.grid(column=4, row=0)
        self.actions_frame.grid(column=5, row=0)
        self.cost_info_frame.grid(column=6, row=0)

        # Dynamic row data
        self.element_type_var = tk.StringVar()
        self.defect_var = tk.StringVar()
        self.bid_item_var = tk.StringVar()
        self.intervention_description_var = tk.StringVar()
        self.unit_of_measure_var = tk.StringVar()
        self.unit_price_var = tk.StringVar()
        self.quantity_var = tk.StringVar()

        # Add widgets to respective frames
        # Bridge Information
        bridge_info_label = ttk.Label(self.bridge_info_frame, text="Bridge UUID")
        bridge_info_label.pack()
        
        # Condition State 1
        condition_state_1_label = ttk.Label(self.condition_state_1_frame, text="Condition State 1")
        condition_state_1_label.pack()
        
        # Condition State 2
        condition_state_2_label = ttk.Label(self.condition_state_2_frame, text="Condition State 2")
        condition_state_2_label.pack()
        
        # Condition State 3
        condition_state_3_label = ttk.Label(self.condition_state_3_frame, text="Condition State 3")
        condition_state_3_label.pack()
        
        # Condition State 4
        condition_state_4_label = ttk.Label(self.condition_state_4_frame, text="Condition State 4")
        condition_state_4_label.pack()
        
        # Actions
        action_button = ttk.Button(self.actions_frame, text="Perform action")
        action_button.pack()
        
        # Cost Information
        cost_label = ttk.Label(self.cost_info_frame, text="Cost Information")
        cost_label.pack()

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
