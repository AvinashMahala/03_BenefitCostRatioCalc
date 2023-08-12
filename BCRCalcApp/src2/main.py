import tkinter as tk
from tkinter import ttk
from database import Database
from tkinter import messagebox
from homepage import Homepage
from deck_tab import DeckTab
from steel_tab import SteelTab
from sub_tab import SubTab
from sup_tab import SupTab
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
        self.uuid=self.homepage.uuid
        self.bridgeId=self.homepage.bridgeId
        self.notebook.add(self.homepage, text="Homepage")
        self.notebook.pack(fill="both", expand=True)

        # Initially disable other tabs
        self.deck = None
        self.steel = None
        self.superstructure = None
        self.substructure = None
        self.final_result = None
        self.benefit_cost_ratio = None

        # Set the background color to red using the style
        # style = ttk.Style(self)
        # style.configure('Background.TFrame', background='#62c6dc')
        # self.homepage.configure(style='Background.TFrame')

    def activate_tabs(self, bridge_id, uuid):
        self.deck_tab = DeckTab(self.notebook, self,bridge_id,uuid)
        self.steel_tab = SteelTab(self.notebook, self,bridge_id,uuid)
        self.sub_tab = SubTab(self.notebook, self,bridge_id,uuid)
        self.sup_tab = SupTab(self.notebook, self,bridge_id,uuid)

        self.notebook.add(self.deck_tab, text="Deck")
        self.notebook.add(self.steel_tab, text="Steel")
        self.notebook.add(self.sub_tab, text="SubStructure")
        self.notebook.add(self.sup_tab, text="SuperStructure")
        # Set the currently displayed tab to the newly added tab
        self.notebook.select(self.deck_tab)
        

        # Repeat the above steps for the other tabs

    def show_msg(self, msg):
        messagebox.showinfo("Message", msg)

if __name__ == "__main__":
    app = Application()
    app.title("Benefit Cost Ratio Application")
    app.geometry('1200x600')  # Set default width (800) and height (600)
    app['background']='#856ff8'  # Set the background color for the root window

    app.mainloop()

