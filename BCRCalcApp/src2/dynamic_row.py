import tkinter as tk
from tkinter import ttk

class BridgeInfoFrame(ttk.Frame):
    def __init__(self, container, controller,bridgeId,uuid, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller
        self.frame = ttk.LabelFrame(self, text="Bridge Information")
        self.frame.grid(column=0, row=0, padx=10, pady=10)
        self.bridgeId=bridgeId
        self.uuid=uuid

        self.entries = {
            "bridge_id": {"value": self.bridgeId, "state": "disabled"},
            "bridge_uuid": {"value": self.uuid, "state": "disabled"},
            "element_num": {"value": "", "options": ['Option 1', 'Option 2', 'Others'], "callback": self.on_element_num_selected},
            "element_type": {"value": "", "state": "disabled"},
            "defect_name": {"value": "", "options": ['Defect 1', 'Defect 2'], "callback": self.on_defect_name_selected},
            "total_quantity": {"value": "", "state": "disabled"},
            "units": {"value": "", "state": "disabled"},
        }

        self.labels = {}
        self.vars = {}
        self.widgets = {}

        for i, (key, value) in enumerate(self.entries.items()):
            self.labels[key] = ttk.Label(self.frame, text=key.replace("_", " ").title())
            self.vars[key] = tk.StringVar(value=value.get("value", ""))
            if "options" in value:
                self.widgets[key] = ttk.Combobox(self.frame, textvariable=self.vars[key], values=value["options"], state=value.get("state", "readonly"))
                if "callback" in value:
                    self.widgets[key].bind('<<ComboboxSelected>>', value["callback"])
            else:
                self.widgets[key] = ttk.Entry(self.frame, textvariable=self.vars[key], state=value.get("state", "normal"))
            self.labels[key].grid(row=i, column=0)
            self.widgets[key].grid(row=i, column=1)

    def on_element_num_selected(self, event):
        pass

    def on_defect_name_selected(self, event):
        pass

class DynamicRow(ttk.Frame):
    def __init__(self, container, controller,bridgeId,uuid, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.container = container
        self.controller = controller
        self.bridgeId=bridgeId
        self.uuid=uuid

        #--------------------
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
        #--------------------
        # Bridge Information
        self.BIF=BridgeInfoFrame(self.container,self.controller,self.bridgeId,self.uuid,)
        
        
        # Condition State 1
        # Condition State 1 frame
        self.condition_state_1_frame = ttk.LabelFrame(self, text="Condition State 1")
        self.condition_state_1_frame.grid(column=1, row=0, padx=10, pady=10)

        # a) BidItem
        self.cs1_bid_item_var = tk.StringVar()
        self.cs1_bid_item_label = ttk.Label(self.condition_state_1_frame, text="BidItem")
        self.cs1_bid_item_dropdown = ttk.Combobox(self.condition_state_1_frame, textvariable=self.bid_item_var, state='disabled')
        self.cs1_bid_item_dropdown.bind('<<ComboboxSelected>>', self.on_bid_item_selected)

        # b) InterventionDescription
        self.cs1_intervention_description_var = tk.StringVar()
        self.cs1_intervention_description_label = ttk.Label(self.condition_state_1_frame, text="InterventionDescription")
        self.cs1_intervention_description_entry = ttk.Entry(self.condition_state_1_frame, textvariable=self.intervention_description_var, state='disabled')
			 
        # c) cs1_UnitOfMeasure
        self.cs1_unit_of_measure_var = tk.StringVar()
        self.cs1_unit_of_measure_label = ttk.Label(self.condition_state_1_frame, text="UnitOfMeasure")
        self.cs1_unit_of_measure_entry = ttk.Entry(self.condition_state_1_frame, textvariable=self.unit_of_measure_var, state='disabled')
			 
        # d) cs1_UnitPrice
        self.cs1_unit_price_var = tk.StringVar()
        self.cs1_unit_price_label = ttk.Label(self.condition_state_1_frame, text="UnitPrice")
        self.cs1_unit_price_entry = ttk.Entry(self.condition_state_1_frame, textvariable=self.unit_price_var, state='disabled')
			 
        # e) cs1_Quantity
        self.cs1_quantity_var = tk.StringVar()
        self.cs1_quantity_label = ttk.Label(self.condition_state_1_frame, text="Quantity")
        self.cs1_quantity_entry = ttk.Entry(self.condition_state_1_frame, textvariable=self.quantity_var, state='disabled')
			 
        # Grid layout for Condition State 1 frame
        self.cs1_bid_item_label.grid(row=0, column=0)
        self.cs1_bid_item_dropdown.grid(row=0, column=1)
        self.cs1_intervention_description_label.grid(row=1, column=0)
        self.cs1_intervention_description_entry.grid(row=1, column=1)
        self.cs1_unit_of_measure_label.grid(row=2, column=0)
        self.cs1_unit_of_measure_entry.grid(row=2, column=1)
        self.cs1_unit_price_label.grid(row=3, column=0)
        self.cs1_unit_price_entry.grid(row=3, column=1)
        self.cs1_quantity_label.grid(row=4, column=0)
        self.cs1_quantity_entry.grid(row=4, column=1)
        
        # Condition State 2
        self.condition_state_2_frame = ttk.LabelFrame(self, text="Condition State 2")
        self.condition_state_2_frame.grid(column=2, row=0, padx=10, pady=10)

        # a) BidItem
        self.bid_item_2_var = tk.StringVar()
        self.bid_item_2_label = ttk.Label(self.condition_state_2_frame, text="BidItem")
        self.bid_item_2_dropdown = ttk.Combobox(self.condition_state_2_frame, textvariable=self.bid_item_2_var, state='disabled')
        self.bid_item_2_dropdown.bind('<<ComboboxSelected>>', self.on_bid_item_2_selected)

        # b) InterventionDescription
        self.intervention_description_2_var = tk.StringVar()
        self.intervention_description_2_label = ttk.Label(self.condition_state_2_frame, text="InterventionDescription")
        self.intervention_description_2_entry = ttk.Entry(self.condition_state_2_frame, textvariable=self.intervention_description_2_var, state='disabled')

        # c) UnitOfMeasure
        self.unit_of_measure_2_var = tk.StringVar()
        self.unit_of_measure_2_label = ttk.Label(self.condition_state_2_frame, text="UnitOfMeasure")
        self.unit_of_measure_2_entry = ttk.Entry(self.condition_state_2_frame, textvariable=self.unit_of_measure_2_var, state='disabled')

        # d) UnitPrice
        self.unit_price_2_var = tk.StringVar()
        self.unit_price_2_label = ttk.Label(self.condition_state_2_frame, text="UnitPrice")
        self.unit_price_2_entry = ttk.Entry(self.condition_state_2_frame, textvariable=self.unit_price_2_var, state='disabled')

        # e) Quantity
        self.quantity_2_var = tk.StringVar()
        self.quantity_2_label = ttk.Label(self.condition_state_2_frame, text="Quantity")
        self.quantity_2_entry = ttk.Entry(self.condition_state_2_frame, textvariable=self.quantity_2_var, state='disabled')

        # Grid layout for Condition State 2 frame
        self.bid_item_2_label.grid(row=0, column=0)
        self.bid_item_2_dropdown.grid(row=0, column=1)
        self.intervention_description_2_label.grid(row=1, column=0)
        self.intervention_description_2_entry.grid(row=1, column=1)
        self.unit_of_measure_2_label.grid(row=2, column=0)
        self.unit_of_measure_2_entry.grid(row=2, column=1)
        self.unit_price_2_label.grid(row=3, column=0)
        self.unit_price_2_entry.grid(row=3, column=1)
        self.quantity_2_label.grid(row=4, column=0)
        self.quantity_2_entry.grid(row=4, column=1)

        
        # Condition State 3
        self.condition_state_3_frame = ttk.LabelFrame(self, text="Condition State 3")
        self.condition_state_3_frame.grid(column=3, row=0, padx=10, pady=10)

        # a) BidItem
        self.bid_item_3_var = tk.StringVar()
        self.bid_item_3_label = ttk.Label(self.condition_state_3_frame, text="BidItem")
        self.bid_item_3_dropdown = ttk.Combobox(self.condition_state_3_frame, textvariable=self.bid_item_3_var, state='disabled')
        self.bid_item_3_dropdown.bind('<<ComboboxSelected>>', self.on_bid_item_3_selected)

        # b) InterventionDescription
        self.intervention_description_3_var = tk.StringVar()
        self.intervention_description_3_label = ttk.Label(self.condition_state_3_frame, text="InterventionDescription")
        self.intervention_description_3_entry = ttk.Entry(self.condition_state_3_frame, textvariable=self.intervention_description_3_var, state='disabled')

        # c) UnitOfMeasure
        self.unit_of_measure_3_var = tk.StringVar()
        self.unit_of_measure_3_label = ttk.Label(self.condition_state_3_frame, text="UnitOfMeasure")
        self.unit_of_measure_3_entry = ttk.Entry(self.condition_state_3_frame, textvariable=self.unit_of_measure_3_var, state='disabled')

        # d) UnitPrice
        self.unit_price_3_var = tk.StringVar()
        self.unit_price_3_label = ttk.Label(self.condition_state_3_frame, text="UnitPrice")
        self.unit_price_3_entry = ttk.Entry(self.condition_state_3_frame, textvariable=self.unit_price_3_var, state='disabled')

        # e) Quantity
        self.quantity_3_var = tk.StringVar()
        self.quantity_3_label = ttk.Label(self.condition_state_3_frame, text="Quantity")
        self.quantity_3_entry = ttk.Entry(self.condition_state_3_frame, textvariable=self.quantity_3_var, state='disabled')

        # Grid layout for Condition State 3 frame
        self.bid_item_3_label.grid(row=0, column=0)
        self.bid_item_3_dropdown.grid(row=0, column=1)
        self.intervention_description_3_label.grid(row=1, column=0)
        self.intervention_description_3_entry.grid(row=1, column=1)
        self.unit_of_measure_3_label.grid(row=2, column=0)
        self.unit_of_measure_3_entry.grid(row=2, column=1)
        self.unit_price_3_label.grid(row=3, column=0)
        self.unit_price_3_entry.grid(row=3, column=1)
        self.quantity_3_label.grid(row=4, column=0)
        self.quantity_3_entry.grid(row=4, column=1)

        
        
        # Condition State 4
        self.condition_state_4_frame = ttk.LabelFrame(self, text="Condition State 4")
        self.condition_state_4_frame.grid(column=4, row=0, padx=10, pady=10)

        # a) BidItem
        self.bid_item_4_var = tk.StringVar()
        self.bid_item_4_label = ttk.Label(self.condition_state_4_frame, text="BidItem")
        self.bid_item_4_dropdown = ttk.Combobox(self.condition_state_4_frame, textvariable=self.bid_item_4_var, state='disabled')
        self.bid_item_4_dropdown.bind('<<ComboboxSelected>>', self.on_bid_item_4_selected)

        # b) InterventionDescription
        self.intervention_description_4_var = tk.StringVar()
        self.intervention_description_4_label = ttk.Label(self.condition_state_4_frame, text="InterventionDescription")
        self.intervention_description_4_entry = ttk.Entry(self.condition_state_4_frame, textvariable=self.intervention_description_4_var, state='disabled')

        # c) UnitOfMeasure
        self.unit_of_measure_4_var = tk.StringVar()
        self.unit_of_measure_4_label = ttk.Label(self.condition_state_4_frame, text="UnitOfMeasure")
        self.unit_of_measure_4_entry = ttk.Entry(self.condition_state_4_frame, textvariable=self.unit_of_measure_4_var, state='disabled')

        # d) UnitPrice
        self.unit_price_4_var = tk.StringVar()
        self.unit_price_4_label = ttk.Label(self.condition_state_4_frame, text="UnitPrice")
        self.unit_price_4_entry = ttk.Entry(self.condition_state_4_frame, textvariable=self.unit_price_4_var, state='disabled')

        # e) Quantity
        self.quantity_4_var = tk.StringVar()
        self.quantity_4_label = ttk.Label(self.condition_state_4_frame, text="Quantity")
        self.quantity_4_entry = ttk.Entry(self.condition_state_4_frame, textvariable=self.quantity_4_var, state='disabled')

        # Grid layout for Condition State 4 frame
        self.bid_item_4_label.grid(row=0, column=0)
        self.bid_item_4_dropdown.grid(row=0, column=1)
        self.intervention_description_4_label.grid(row=1, column=0)
        self.intervention_description_4_entry.grid(row=1, column=1)
        self.unit_of_measure_4_label.grid(row=2, column=0)
        self.unit_of_measure_4_entry.grid(row=2, column=1)
        self.unit_price_4_label.grid(row=3, column=0)
        self.unit_price_4_entry.grid(row=3, column=1)
        self.quantity_4_label.grid(row=4, column=0)
        self.quantity_4_entry.grid(row=4, column=1)

        
        # Actions
        # In the DynamicRow class, add this to the __init__ method where the button is created:
        remove_row_button = ttk.Button(self.actions_frame, text="REMOVE ROW", command=self.remove_row)
        remove_row_button.pack()


        calculate_button = ttk.Button(self.actions_frame, text="Calculate", command=self.calculate_cost)
        calculate_button.pack()

        
        # Cost Information
        cost_label = ttk.Label(self.cost_info_frame, text="Cost Information")
        cost_label.pack()

    def remove_row(self):
        # Get the parent container (the notebook tab)
        parent_container = self.master.master
        pp=self.master.master.master

        # Check if this dynamic row is the last row, and there are more than one rows
        if len(pp.dynamic_rows) > 1 and pp.dynamic_rows[-1] == self:
            # Destroy this dynamic row widget
            self.destroy()
            # Remove this dynamic row instance from the list
            pp.dynamic_rows.pop()

            # Update the grid layout of the parent container (the notebook tab)
            # to reorganize the remaining rows
            for i, row in enumerate(pp.dynamic_rows):
                row.grid(row=i, column=0, padx=5, pady=5)

            # If you want to perform any other actions after removing the row, do it here
        else:
            # If this is the only row, do not remove it
            print("Cannot remove the last row.")


    def calculate_cost(self):
        # Replace with your actual calculation logic
        try:
            quantity = int(self.quantity_var.get())
            unit_price = float(self.unit_price_var.get())
            cost = quantity * unit_price
            print("Total Cost:", cost)  # You can display the result in a label or any other way you prefer
        except ValueError:
            print("Invalid quantity or unit price")


    def on_bid_item_selected(self, event):
        selected_bid_item = self.bid_item_var.get()

        # You should replace the following lines with actual calls to your data source
        # to fetch the corresponding data
        self.intervention_description_var.set(f'Description for {selected_bid_item}')
        self.unit_of_measure_var.set(f'Unit for {selected_bid_item}')
        self.unit_price_var.set(f'Price for {selected_bid_item}')

        self.quantity_entry['state'] = 'normal'  # enable Quantity entry

    def on_bid_item_2_selected(self, event):
        selected_bid_item = self.bid_item_2_var.get()

        # You should replace the following lines with actual calls to your data source
        # to fetch the corresponding data
        self.intervention_description_2_var.set(f'Description for {selected_bid_item}')
        self.unit_of_measure_2_var.set(f'Unit for {selected_bid_item}')
        self.unit_price_2_var.set(f'Price for {selected_bid_item}')

        self.quantity_2_entry['state'] = 'normal'  # enable Quantity entry

    def on_bid_item_3_selected(self, event):
        selected_bid_item = self.bid_item_3_var.get()

        # You should replace the following lines with actual calls to your data source
        # to fetch the corresponding data
        self.intervention_description_3_var.set(f'Description for {selected_bid_item}')
        self.unit_of_measure_3_var.set(f'Unit for {selected_bid_item}')
        self.unit_price_3_var.set(f'Price for {selected_bid_item}')

        self.quantity_3_entry['state'] = 'normal'  # enable Quantity entry
    
    def on_bid_item_4_selected(self, event):
        selected_bid_item = self.bid_item_4_var.get()

        # You should replace the following lines with actual calls to your data source
        # to fetch the corresponding data
        self.intervention_description_4_var.set(f'Description for {selected_bid_item}')
        self.unit_of_measure_4_var.set(f'Unit for {selected_bid_item}')
        self.unit_price_4_var.set(f'Price for {selected_bid_item}')

        self.quantity_4_entry['state'] = 'normal'  # enable Quantity entry

    def on_element_num_selected(self, event):
        selected_option = self.element_num_var.get()
        if selected_option == 'Others':
            self.element_type_entry['state'] = 'normal'
        else:
            self.element_type_entry['state'] = 'disabled'

    def on_defect_name_selected(self, event):
        self.total_quantity_var.set('Some value')  # replace with actual value
        self.units_var.set('Some value')  # replace with actual value

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
