import tkinter as tk
from tkinter import ttk
import pandas as pd
from BenefitCostRatioCalcApp import DynamicDataEntryForm

class TabbedMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabbed Menu Example")

        # Custom style for the notebook
        self.style = ttk.Style()
        self.style.configure('Custom.TNotebook', tabposition='n', background='lightgray')
        self.style.map('Custom.TNotebook.Tab', foreground=[('selected', 'black'), ('!selected', 'gray')])

        self.notebook = ttk.Notebook(root, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)

        self.create_tab("Deck")
        self.create_tab("SuperStructure")
        self.create_tab("SubStructure")

    def create_tab(self, tab_title):
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=tab_title)

        if tab_title == "Deck":
            deck_form = DynamicDataEntryForm(tab_frame)
            # deck_form.pack(fill='both', expand=True)

        work_area_label = ttk.Label(tab_frame, text=f"This is the {tab_title} work area.", font=("Arial", 14))
        work_area_label.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = TabbedMenuApp(root)
    root.mainloop()
