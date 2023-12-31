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

        self.clear_fields()

        

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
            "Bridge ID*", "ADT*", "Detour Length (mi)*", "ADT_TRk*", "ADT w/o TRK", "Personal purpose ADT",
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
                repopulate_btn.grid(row=row+1, column=col + 1, padx=5, pady=5)
            else:
                entry = tk.Entry(detailed_frame)
                entry.grid(row=row, column=col + 1, padx=5, pady=5)
                entry.insert(0, item)
                self.entries.append(entry)

        rows_required_for_data = len(headers) // 3
        self.calculate_bcr_btn = tk.Button(detailed_frame, text="Calculate BCR", command=self.calculate_bcr)
        self.calculate_bcr_btn.grid(row=rows_required_for_data, column=col + 1, columnspan=8, pady=20, padx=10)

        # Button to clear all fields
        clear_btn = tk.Button(detailed_frame, text="Clear All Fields", command=self.clear_fields)
        clear_btn.grid(row=rows_required_for_data + 1, column=0, columnspan=8, pady=20, padx=10)

        # Button to calculate fields
        self.calculate_fields_btn = tk.Button(detailed_frame, text="Calculate Fields", command=self.calculate_fields)
        self.calculate_fields_btn.grid(row=rows_required_for_data + 2, column=col + 1, columnspan=8, pady=20, padx=10)


    def calculate_fields(self):
        # Get values from the Entry fields
        adt_value = self.entries[1].get()
        detour_length_value = self.entries[2].get()
        adt_trk_value = self.entries[3].get()

        # Check if any of the required fields are missing
        if not all([adt_value, detour_length_value, adt_trk_value]):
            tk.messagebox.showerror("Error", "Please enter values for ADT, Detour Length, and ADT_TRk.")
            return

        adt_wo_trk = float(adt_value) - float(adt_trk_value)
        personal_purpose_adt = adt_wo_trk * 0.882
        business_purpose_adt = adt_wo_trk * 0.118

        vtts_per_day = (float(adt_trk_value) * 1 * 32.4 +
                        personal_purpose_adt * 1.67 * 17 +
                        business_purpose_adt * 1.67 * 31.9) * (float(detour_length_value) / 75)

        vehicle_operating_cost_per_day = (float(adt_trk_value) * 1.01 +
                                          adt_wo_trk * 0.46) * float(detour_length_value)

        emission_costs_per_day = (0.143 * 16800 + 0.008 * 810500 + 400 * 57 + 0.0418 * 45100) * \
                                 float(adt_value) * float(detour_length_value) / 1000000

        total_benefit_per_day = vtts_per_day + vehicle_operating_cost_per_day + emission_costs_per_day
        total_benefit_per_year = total_benefit_per_day * 356

        maintenance_cost = float(self.maintenance_cost_entry.get())
        bcr_value = total_benefit_per_year / maintenance_cost

        # Update the Entry fields with calculated values
        self.entries[4].delete(0, tk.END)
        self.entries[4].insert(0, "${:.2f}".format(adt_wo_trk))

        self.entries[5].delete(0, tk.END)
        self.entries[5].insert(0, "${:.2f}".format(personal_purpose_adt))

        self.entries[6].delete(0, tk.END)
        self.entries[6].insert(0, "${:.2f}".format(business_purpose_adt))

        self.entries[7].delete(0, tk.END)
        self.entries[7].insert(0, "${:.2f}".format(vtts_per_day))

        self.entries[8].delete(0, tk.END)
        self.entries[8].insert(0, "${:.2f}".format(vehicle_operating_cost_per_day))

        self.entries[9].delete(0, tk.END)
        self.entries[9].insert(0, "${:.2f}".format(emission_costs_per_day))

        self.entries[10].delete(0, tk.END)
        self.entries[10].insert(0, "${:.2f}".format(total_benefit_per_day))

        self.entries[11].delete(0, tk.END)
        self.entries[11].insert(0, "${:.2f}".format(total_benefit_per_year))

        self.entries[13].delete(0, tk.END)
        self.entries[13].insert(0, "{:.2f}".format(bcr_value))


    def clear_fields(self):
        # Clear Entry fields in UUID Area
        self.uuid_entry.delete(0, tk.END)

        # Clear Entry fields in Final Costs Area
        for entry in self.final_costs:
            entry.delete(0, tk.END)

        # Clear Entry fields in Detailed Information Area
        for entry in self.entries:
            entry.delete(0, tk.END)

        # Clear the Total Maintenance Cost label
        self.total_maintenance_label.config(text="")

        # Clear the Maintenance Cost Entry
        self.maintenance_cost_entry.delete(0, tk.END)

        # Clear the BCR Entry
        self.entries[-1].delete(0, tk.END)


    def repopulate_maintenance_cost(self):
        # Assuming the total cost value is stored in a variable named 'total_cost'
        # This variable should be updated whenever the sum is calculated in the right work area.
        self.maintenance_cost_entry.delete(0, tk.END)  # Clear the current value
        self.maintenance_cost_entry.insert(0, str(self.total_cost))  # Populate with the updated value

    def calculate_bcr(self):
        # Get the Total Benefit per Year and Maintenance Cost from the respective Entry fields
        try:
            total_benefit_per_year = float(self.entries[11].get().replace('$', '').replace(',', ''))
            maintenance_cost = float(self.maintenance_cost_entry.get())
            
            # Calculate BCR
            if maintenance_cost != 0:
                bcr_value = total_benefit_per_year / maintenance_cost
            else:
                bcr_value = 0.0

            # Update the BCR Entry field
            self.entries[-1].delete(0, tk.END)
            self.entries[-1].insert(0, "{:.2f}".format(bcr_value))
        except ValueError:
            # Handle the case where the input values are not valid floats
            self.controller.show_msg("Error: Please enter valid numeric values for Total Benefit and Maintenance Cost.")

