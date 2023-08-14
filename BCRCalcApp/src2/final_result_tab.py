import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class FinalResultTab(ttk.Frame):
    def __init__(self, container, controller, bridge_id, uuid, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.controller = controller
        self.bridge_id = bridge_id
        self.uuid = uuid

        self.total_cost=0


        # Left work area
        left_frame = ttk.LabelFrame(self, text="UUID Area")
        left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        tk.Label(left_frame, text="UUID").pack(pady=10)
        self.uuid_entry = tk.Entry(left_frame)
        self.uuid_entry.pack(pady=10)
        retrieve_btn = tk.Button(left_frame, text="Retrieve Final Cost", command=self.retrieve_final_cost)
        retrieve_btn.pack(pady=10)

        # Right work area (Grid Headers)
        right_frame = ttk.LabelFrame(self, text="Final Costs Area")
        right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        tk.Label(right_frame, text="Bridge ID").grid(row=0, column=0)
        tk.Label(right_frame, text="Elements").grid(row=0, column=1)
        tk.Label(right_frame, text="Final Cost").grid(row=0, column=2)
        tk.Label(right_frame, text="Total Maintenance Cost").grid(row=0, column=3)

        # Display the Bridge ID once
        tk.Label(right_frame, text=str(self.bridge_id)).grid(row=1, column=0, rowspan=4, sticky="n")
        
        # Insert data (example values)
        data = [
            ("Deck", "$0"),
            ("Superstructure", "$0"),
            ("Steel", "$0"),
            ("Substructure", "$0")
        ]

        self.final_costs = []

        for index, (element, cost) in enumerate(data, start=1):
            tk.Label(right_frame, text=element).grid(row=index, column=1)
            
            # Create Entry widget to hold and retrieve final costs
            final_cost_entry = tk.Entry(right_frame)
            final_cost_entry.grid(row=index, column=2)
            final_cost_entry.insert(0, cost)
            self.final_costs.append(final_cost_entry)
            
            if element == "Deck":
                self.total_maintenance_label = tk.Label(right_frame, text="")
                self.total_maintenance_label.grid(row=index, column=3)

        # Button to calculate total
        self.calculate_btn = tk.Button(right_frame, text="Calculate Total", command=self.calculate_total)
        self.calculate_btn.grid(row=5, column=2)

        self.create_detailed_grid()

    def fetch_bridge_id(self, uuid_value):
        # Connect to the SQLite database
        connection = sqlite3.connect('BenefitCostRatioApp.db')
        cursor = connection.cursor()

        # Fetch bridge_id from CalculationMetaData table
        cursor.execute('SELECT bridge_id FROM CalculationMetaData WHERE uuid = ?', (uuid_value,))
        bridge_id = cursor.fetchone()

        # Close the connection
        connection.close()

        return bridge_id[0] if bridge_id else None

    def retrieve_final_cost(self):
        uuid_value = self.uuid_entry.get().strip()  # Get UUID from entry
        if not uuid_value:
            # Display an error message if UUID is not provided
            tk.messagebox.showerror("Error", "Please provide a UUID!")
            return

         # Fetch and update the bridge ID
        bridge_id = self.fetch_bridge_id(uuid_value)
        if bridge_id:
            self.entries[0].delete(0, tk.END)
            self.entries[0].insert(0, bridge_id)
        else:
            messagebox.showerror("Error", "No bridge ID found for the given UUID.")

        costs = self.fetch_costs(uuid_value)  # Fetch the costs

        # Assuming costs is a dictionary with keys: Deck, Superstructure, Steel, Substructure
        for entry, key in zip(self.final_costs, ["Deck", "Superstructure", "Steel", "Substructure"]):
            cost_value = costs.get(key, "N/A")
            entry.delete(0, tk.END)  # Clear the entry
            entry.insert(0, "${:,.2f}".format(cost_value))
        





    def fetch_costs(self, uuid_value):
        connection = sqlite3.connect('BenefitCostRatioApp.db')
        cursor = connection.cursor()

        # Dictionaries to store the costs
        costs = {
            "Deck": 0,
            "Steel": 0,
            "Substructure": 0,
            "Superstructure": 0
        }

        tables = {
            "Deck": "BridgeDeckCalcHist",
            "Steel": "BridgeSteelCalcHist",
            "Substructure": "BridgeSubCalcHist",
            "Superstructure": "BridgeSupCalcHist"
        }

        for element, table in tables.items():
            cursor.execute(f"SELECT final_cost FROM {table} WHERE uuid = ?", (uuid_value,))
            
            rows = cursor.fetchall()
            total_cost = sum(row[0] for row in rows)
            
            costs[element] = total_cost  

        # Close the connection
        connection.close()

        return costs

    def calculate_total(self):
        total = 0
        for entry in self.final_costs:
            try:
                # Convert the string into a format suitable for floating point operations
                cost = float(entry.get().replace('$', '').replace(',', ''))
                total += cost
            except ValueError:
                # Handle case where the entry doesn't have a valid float value
                pass
        # Format and display the total in the Total Maintenance Cost label
        self.total_cost=total
        formatted_total = "${:,.2f}".format(total)
        self.total_maintenance_label.config(text=formatted_total)

    def create_detailed_grid(self):
        detailed_frame = ttk.LabelFrame(self, text="Detailed Information")
        detailed_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        headers = [
            "Bridge ID", "ADT", "Detour Length (mi)", "ADT_TRk", "ADT w/o TRK", "Personal purpose ADT",
            "Business purpose ADT", "$ Value of Travel Time Saving (VTTS)/Day", "Vehicle operating cost/ Day",
            "Emission Costs", "Total benefit/day", "Total benefit/ year", "Maintenance cost","BCR"
        ]

        # Sample data
        data_row = [
            "180570G01155010", "18238.00", "1.00", "3.00", "18235.00", "16083.27", "2151.73",
            "6089.00", "8391.00", "612.00", "15093.00", "5373022.00", "54268920.96", "24.84"
        ]

        self.entries = []

        for idx, (header, item) in enumerate(zip(headers, data_row)):
            # Position calculation
            row = idx // 3
            col = (idx % 3) * 2  # we multiply by 2 to account for the alternating header and data columns

            tk.Label(detailed_frame, text=header).grid(row=row, column=col, padx=5, pady=5)

            if header == "Maintenance cost":
                self.maintenance_cost_entry = tk.Entry(detailed_frame)
                self.maintenance_cost_entry.grid(row=row, column=col + 1, padx=5, pady=5)
                self.maintenance_cost_entry.insert(0, item)
                self.entries.append(self.maintenance_cost_entry)

                # Button to repopulate the maintenance cost
                repopulate_btn = tk.Button(detailed_frame, text="Repopulate", command=self.repopulate_maintenance_cost)
                repopulate_btn.grid(row=row, column=col + 2, padx=5, pady=5)
            else:
                entry = tk.Entry(detailed_frame)
                entry.grid(row=row, column=col + 1, padx=5, pady=5)
                entry.insert(0, item)
                self.entries.append(entry)

        rows_required_for_data = len(headers) // 3
        self.calculate_bcr_btn = tk.Button(detailed_frame, text="Calculate BCR", command=self.calculate_bcr)
        self.calculate_bcr_btn.grid(row=rows_required_for_data, columnspan=6, pady=20, padx=10)

    def repopulate_maintenance_cost(self):
        # Assuming the total cost value is stored in a variable named 'total_cost'
        # This variable should be updated whenever the sum is calculated in the right work area.
        self.maintenance_cost_entry.delete(0, tk.END)  # Clear the current value
        self.maintenance_cost_entry.insert(0, str(self.total_cost))  # Populate with the updated value

    def calculate_bcr(self):
        # Your logic to calculate BCR goes here
        # For now, we are just setting a placeholder value
        bcr_value = 1.25
        self.entries[-1].delete(0, tk.END)  # Clear previous BCR value if exists
        self.entries[-1].insert(0, str(bcr_value))
