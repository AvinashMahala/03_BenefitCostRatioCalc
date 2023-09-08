import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import openpyxl
import sqlite3
from tkinter import messagebox
import sqlite3
from database import Database

class UploadExcelTab(ttk.Frame):
    def __init__(self, container, controller, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.controller = controller

        self.create_widgets()

        self.database = Database()

        self.connection = sqlite3.connect('BenefitCostRatioApp.db')
        

        tk.Label(self, text="Upload Excel File").pack(pady=10)

        # Button to open file dialog for Excel file selection
        self.upload_button = tk.Button(self, text="Browse Excel File", command=self.upload_excel_file)
        self.upload_button.pack(pady=10)

        # Button to trigger the upload and parsing process
        self.parse_button = tk.Button(self, text="Upload and Parse", command=self.parse_excel)
        self.parse_button.pack(pady=10)

        # Status label to display upload and parsing status
        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)

        # Variable to store the selected Excel file path
        self.excel_file_path = None

    def create_widgets(self):
        # Create your widgets for the Upload Excel Tab
        
        # Create the "Truncate Table" button
        self.truncate_button = tk.Button(self, text="Truncate Table", command=self.truncate_table)
        self.truncate_button.pack(pady=10)

    def truncate_table(self):
        # Specify the table name you want to truncate (e.g., "BidItemPriceTxDot")
        table_name = "BidItemPriceTxDot"

        # Display a confirmation dialog
        confirmed = messagebox.askyesno("Confirm Truncate", f"Are you sure you want to truncate table '{table_name}'?")
        
        if confirmed:
            # Call the truncate_table method from your Database class
            self.database.truncate_table(table_name)

    def upload_excel_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.excel_file_path = file_path
            self.status_label.config(text="Excel file selected: " + file_path)


    def add_none_row(self,bid_item_num,bid_item_desc,unit_of_meas,avg_unit_price):
        # Specify the values for the new row
        self.bid_item_num = bid_item_num
        self.bid_item_desc = bid_item_desc
        self.unit_of_meas = unit_of_meas
        self.avg_unit_price = avg_unit_price

        # Call the insert_row method to add the row
        if self.database.insert_row(self.bid_item_num, self.bid_item_desc, self.unit_of_meas, self.avg_unit_price):
            messagebox.showinfo("None Row Added", "The row has been successfully added.")
        else:
            messagebox.showerror("Error", "An error occurred while adding None row.")

    def parse_excel(self):
        if self.excel_file_path:
            try:
                # Open the Excel file
                workbook = openpyxl.load_workbook(self.excel_file_path)
                worksheet = workbook.active

                # Define column indices for data extraction
                bid_item_column = 1  # Column A
                description_column = 2  # Column B
                unit_measure_column = 3  # Column C
                avg_price_column = 4  # Column F

                # Initialize a list to store parsed data
                parsed_data = []

                # Iterate through rows and extract data
                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    bid_item = row[bid_item_column - 1]
                    description = row[description_column - 1]
                    unit_measure = row[unit_measure_column - 1]
                    avg_price = row[avg_price_column - 1]

                    parsed_data.append((bid_item, description, unit_measure, avg_price))

                # Insert parsed data into the SQLite database
                self.insert_data_into_database(parsed_data)

                self.status_label.config(text="Excel data uploaded and parsed successfully.")
                self.add_none_row("0","None","NA",0)



            except Exception as e:
                self.status_label.config(text="Error: " + str(e))
        else:
            self.status_label.config(text="Please select an Excel file first.")

    def insert_data_into_database(self, data):
        # Connect to the SQLite database
        connection = self.connection
        cursor = connection.cursor()

        # Define the SQL statement for data insertion
        insert_sql = "INSERT INTO BidItemPriceTxDot (BidItemNum, BidItemDesc, UnitOfMeas, AvgUnitPrice) VALUES (?, ?, ?, ?)"

        try:
            # Execute the insertion for each row of data
            cursor.executemany(insert_sql, data)

            # Commit the transaction
            connection.commit()

        except Exception as e:
            connection.rollback()
            raise e
