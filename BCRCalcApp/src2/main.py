#This file will contain the Application class, which is responsible for managing the overall application.

import tkinter as tk
from tkinter import ttk
from database import Database
from tkinter import messagebox
from homepage import Homepage
from deck import DeckTab
from steel import Steel
from superstructure import Superstructure
from substructure import Substructure
from final_result import FinalResult
from benefit_cost_ratio import BenefitCostRatio

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Creating the database
        self.database = Database()

        # Setting up the notebook (tab manager)
        self.notebook = ttk.Notebook(self)
        self.homepage = Homepage(self, self.notebook)
        self.notebook.add(self.homepage, text="Homepage")
        self.notebook.pack(fill="both", expand=True)

        # Initially disable other tabs
        self.deck = None
        self.steel = None
        self.superstructure = None
        self.substructure = None
        self.final_result = None
        self.benefit_cost_ratio = None

    def activate_tabs(self, bridge_id, uuid):
        self.deck_tab = DeckTab(self.notebook, self)
        self.notebook.add(self.deck_tab, text="Deck")

        # Repeat the above steps for the other tabs

    def show_msg(self, msg):
        messagebox.showinfo("Message", msg)

if __name__ == "__main__":
    app = Application()
    app.mainloop()

