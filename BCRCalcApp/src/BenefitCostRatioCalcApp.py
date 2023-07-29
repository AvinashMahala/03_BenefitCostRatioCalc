import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3

class DynamicDataEntryForm:
    def __init__(self, root, database_name):
        self.root = root
        self.database_name = database_name
        # self.root.title("Benefit Cost Ratio Calculator")
        
        # Create a labeled frame for the buttons
        button_frame = ttk.LabelFrame(self.root, text="Actions", padding=(5, 5))
        button_frame.pack(fill="x", padx=10, pady=5)

        add_button = ttk.Button(button_frame, text="Add Row", command=lambda: self.add_row(rows_frame))
        add_button.pack(side="left", padx=5)

        save_button = ttk.Button(button_frame, text="Save to Excel", command=self.save_to_excel)
        save_button.pack(side="left", padx=5)

        read_button = ttk.Button(button_frame, text="Read from Excel", command=self.read_from_excel)
        read_button.pack(side="left", padx=5)

        read_db_button = ttk.Button(button_frame, text="Read from Database", command=self.read_from_database)
        read_db_button.pack(side="left", padx=5)

        # Create a labeled frame for the dynamic rows
        rows_frame = ttk.LabelFrame(self.root, text="Dynamic Rows", padding=(5, 5))
        rows_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.rows = []
        self.add_row(rows_frame)
        

    def read_from_database(self):
            try:
                conn = sqlite3.connect(self.database_name)
                df = pd.read_sql_query("SELECT * FROM DeckElementNames", conn)
                conn.close()

                print("Data read from database:")
                print(df)
            except sqlite3.Error as e:
                print(f"Error while reading from database: {e}")

    def add_row(self, parent_frame):
        row_frame = ttk.Frame(parent_frame)
        row_frame.pack(pady=5)

        element_type_choices = ["Type A", "Type B", "Type C"]
        element_type_var = tk.StringVar(value=element_type_choices[0])  # Set default value
        element_type_dropdown = ttk.Combobox(row_frame, values=element_type_choices, width=15, textvariable=element_type_var)
        element_type_dropdown.grid(row=0, column=0, padx=5, pady=5)

        # Define the defect_dropdown before using it in the bind method
        defect_choices = []  # Will be populated based on selected element type
        defect_var = tk.StringVar(value=defect_choices)
        defect_dropdown = ttk.Combobox(row_frame, values=defect_choices, width=15, textvariable=defect_var, state="disabled")
        defect_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Bind the update_defect_choices method to the event of value change in element_type_dropdown
        element_type_dropdown.bind("<<ComboboxSelected>>", lambda event, etd=element_type_dropdown, dd=defect_dropdown: self.update_defect_choices(etd, dd))

        choices = ["Option 1", "Option 2", "Option 3"]
        dropdown = ttk.Combobox(row_frame, values=choices, width=15)
        dropdown.grid(row=0, column=2, padx=5, pady=5)

        delete_button = ttk.Button(row_frame, text="Delete", command=lambda: self.delete_row(row_frame))
        delete_button.grid(row=0, column=3, padx=5, pady=5)

        self.rows.append((element_type_dropdown, defect_dropdown, dropdown, delete_button))


    
    def create_condition_state_group(self, parent_frame, group_name):
        group_frame = ttk.LabelFrame(parent_frame, text=group_name)
        bid_item_choices = []  # Populate based on selected defect
        bid_item_dropdown = ttk.Combobox(group_frame, values=bid_item_choices, width=15, state="disabled")
        bid_item_dropdown.grid(row=0, column=1, padx=5, pady=5)

        intervention_description_var = tk.StringVar()  # Create StringVar for Intervention Description
        intervention_description_entry = ttk.Entry(group_frame, width=30, state="disabled", textvariable=intervention_description_var)
        intervention_description_entry.grid(row=1, column=1, padx=5, pady=5)

        unit_of_measure_var = tk.StringVar()  # Create StringVar for Unit of Measure
        unit_of_measure_entry = ttk.Entry(group_frame, width=10, state="disabled", textvariable=unit_of_measure_var)
        unit_of_measure_entry.grid(row=2, column=1, padx=5, pady=5)

        unit_price_var = tk.StringVar()  # Create StringVar for Unit Price
        unit_price_entry = ttk.Entry(group_frame, width=10, state="disabled", textvariable=unit_price_var)
        unit_price_entry.grid(row=3, column=1, padx=5, pady=5)

        quantity_var = tk.StringVar()  # Create StringVar for Quantity
        quantity_entry = ttk.Entry(group_frame, width=10, state="disabled", textvariable=quantity_var)
        quantity_entry.grid(row=4, column=1, padx=5, pady=5)

        bid_item_var = tk.StringVar()
        bid_item_dropdown.config(textvariable=bid_item_var)

        # Bind the on_bid_item_change method to the event of value change in bid_item_dropdown
        bid_item_dropdown.bind("<<ComboboxSelected>>", lambda event, bid_item_dropdown=bid_item_dropdown, intervention_description_entry=intervention_description_entry, unit_of_measure_entry=unit_of_measure_entry, unit_price_entry=unit_price_entry, quantity_entry=quantity_entry: self.on_bid_item_change(bid_item_dropdown, intervention_description_entry, unit_of_measure_entry, unit_price_entry, quantity_entry))


        # ... Add logic for generating values in the fields based on selections (similar to update_defect_choices and update_bid_item_choices)
        # Here's an example of how you can populate bid_item_choices for Condition State 2 Group
        if group_name == "Condition State 1 Group":
            defect_value = self.rows[-1][1].get()  # Get the selected value from the Defect dropdown
            # Example: If defect_value is "Type 1 Defect 1", populate bid_item_choices accordingly
            bid_item_choices = ["Type 1 Defect 1 BidItem 1", "Type 1 Defect 1 BidItem 2", "Type 1 Defect 1 BidItem 3"]
            bid_item_dropdown.config(values=bid_item_choices, state="readonly")
        return group_frame


    def on_bid_item_change(*args):
            # Get the selected value from the Defect dropdown
            defect_value = self.rows[-1][1].get()
            if defect_value:
                # Populate the fields based on the selected defect (similar to update_bid_item_choices)
                # Note: Here, we can implement the logic to fetch the data from the database based on the selected defect
                intervention_description_var.set("Sample Intervention Description")
                unit_of_measure_var.set("Sample UOM")
                unit_price_var.set("Sample Price")

                # Enable the Quantity entry
                quantity_entry.config(state="normal")
            else:
                # If no defect is selected, disable all fields and clear their values
                bid_item_var.set("")  # Clear the Bid Item dropdown selection
                bid_item_dropdown.config(state="disabled")

                intervention_description_var.set("")
                intervention_description_entry.config(state="disabled")

                unit_of_measure_var.set("")
                unit_of_measure_entry.config(state="disabled")

                unit_price_var.set("")
                unit_price_entry.config(state="disabled")

                quantity_var.set("")
                quantity_entry.config(state="disabled")

            bid_item_var.trace_add("write", on_bid_item_change)

            return group_frame
        

    def update_defect_choices(self, element_type_dropdown, defect_dropdown):
        # ... Update defect_choices based on element_type_dropdown selection (similar to the previous implementation)
        pass

    def update_bid_item_choices(self, defect_dropdown):
        # ... Update bid_item_choices based on defect_dropdown selection (similar to the previous implementation)
        pass

    def delete_row(self, row_frame):
        # Find the index of the row_frame in the list of rows and remove it
        for i, row in enumerate(self.rows):
            if row_frame == row[0].master:
                self.rows.pop(i)
                row_frame.destroy()
                break

    def save_to_excel(self):
        data = {
            "Label": [entry[0].get() for entry in self.rows],
            "Text": [entry[1].get() for entry in self.rows],
            "Dropdown": [entry[2].get() for entry in self.rows]
        }
        df = pd.DataFrame(data)
        file_path = "data_entry.xlsx"
        df.to_excel(file_path, index=False)
        print(f"Data saved to {file_path}")

    def read_from_excel(self):
        file_path = "data_entry.xlsx"
        df = pd.read_excel(file_path)
        print("Data read from Excel:")
        print(df)

if __name__ == "__main__":
    root = tk.Tk()
    app = DynamicDataEntryForm(root)
    root.mainloop()
