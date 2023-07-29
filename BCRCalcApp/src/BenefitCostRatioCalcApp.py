import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3

class DynamicDataEntryForm:
    def __init__(self, root, database_name):
        self.root = root
        # self.root.title("Benefit Cost Ratio Calculator")
        self.database_name = database_name
        
        self.rows = []
        self.add_row()

        add_button = ttk.Button(root, text="Add Row", command=self.add_row)
        add_button.pack(pady=5)

        save_button = ttk.Button(root, text="Save to Excel", command=self.save_to_excel)
        save_button.pack(pady=5)

        read_button = ttk.Button(root, text="Read from Excel", command=self.read_from_excel)
        read_button.pack(pady=5)

        read_db_button = ttk.Button(root, text="Read from Database", command=self.read_from_database)
        read_db_button.pack(pady=5)

    def read_from_database(self):
            try:
                conn = sqlite3.connect(self.database_name)
                df = pd.read_sql_query("SELECT * FROM DeckElementNames", conn)
                conn.close()

                print("Data read from database:")
                print(df)
            except sqlite3.Error as e:
                print(f"Error while reading from database: {e}")

    def add_row(self):
        row_frame = ttk.Frame(self.root)
        row_frame.pack(pady=5)

        label_entry = ttk.Entry(row_frame, width=15)
        label_entry.grid(row=0, column=0, padx=5, pady=5)

        text_entry = ttk.Entry(row_frame, width=30)
        text_entry.grid(row=0, column=1, padx=5, pady=5)

        choices = ["Option 1", "Option 2", "Option 3"]
        dropdown = ttk.Combobox(row_frame, values=choices, width=15)
        dropdown.grid(row=0, column=2, padx=5, pady=5)

        delete_button = ttk.Button(row_frame, text="Delete", command=lambda: self.delete_row(row_frame))
        delete_button.grid(row=0, column=3, padx=5, pady=5)

        self.rows.append((label_entry, text_entry, dropdown, delete_button))

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
