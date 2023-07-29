import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
from tkinter import filedialog

class DataLoaderForm(ttk.Frame):
    def __init__(self, parent, database_name):
        super().__init__(parent)
        self.database_name = database_name

        label = ttk.Label(self, text="Data Loader", font=("Arial", 14))
        label.pack(pady=10)

        browse_button = ttk.Button(self, text="Browse Excel File", command=self.browse_excel_file)
        browse_button.pack(pady=5)

    def browse_excel_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if file_path:
            self.load_data_from_excel(file_path)

    def load_data_from_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            print(df)
            self.push_to_database(df)
            print("Data loaded from Excel and pushed to database successfully.")
        except Exception as e:
            print(f"Error loading data from Excel: {e}")

    def push_to_database(self, data_df):
        try:
            conn = sqlite3.connect(self.database_name)
            data_df.to_sql("DeckElementNames", conn, if_exists="append", index=False)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error pushing data to database: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataLoaderForm(root, "AppMetaData.db")
    app.pack()
    root.mainloop()
