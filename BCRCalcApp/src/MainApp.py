import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
from BenefitCostRatioCalcApp import DynamicDataEntryForm
from DataLoader import DataLoaderForm

DATABASE_NAME = "AppMetaData.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS DeckElementNames (
                    rowId INTEGER PRIMARY KEY AUTOINCREMENT,
                    ElemNumber NUMERIC,
                    ElementName TEXT,
                    Units TEXT,
                    Description TEXT
                )''')


    # Dummy data for initialization
    dummy_data = [
        (10001, 12
, "Element 1", "Unit 1", "Description 1"),
        (10002, 2, "Element 2", "Unit 2", "Description 2"),
        (10003, 3, "Element 3", "Unit 3", "Description 3")
    ]

    c.executemany('INSERT INTO DeckElementNames (rowId, ElemNumber, ElementName, Units, Description) VALUES (?, ?, ?, ?, ?)', dummy_data)




    conn.commit()
    conn.close()

class TabbedMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Benefit Cost Ratio Calculator")

        # Initialize the database
        # initialize_database()

        # Custom style for the notebook
        self.style = ttk.Style()
        self.style.configure('Custom.TNotebook', tabposition='n', background='lightgray')
        self.style.map('Custom.TNotebook.Tab', foreground=[('selected', 'black'), ('!selected', 'gray')])

        self.notebook = ttk.Notebook(root, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)

        self.create_tab("Data Loader")
        self.create_tab("Deck")
        self.create_tab("SuperStructure")
        self.create_tab("SubStructure")

    def create_tab(self, tab_title):
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=tab_title)

        if tab_title == "Deck":
            deck_form = DynamicDataEntryForm(tab_frame, database_name=DATABASE_NAME)
            # deck_form.pack(fill='both', expand=True)
        if tab_title == "Data Loader":
            data_loader_form = DataLoaderForm(tab_frame, database_name=DATABASE_NAME)
            data_loader_form.pack(fill='both', expand=True)

        work_area_label = ttk.Label(tab_frame, text=f"This is the {tab_title} work area.", font=("Arial", 14))
        work_area_label.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = TabbedMenuApp(root)
    root.mainloop()
