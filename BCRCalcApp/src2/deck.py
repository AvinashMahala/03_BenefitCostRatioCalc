import tkinter as tk
from tkinter import ttk
from dynamic_row import DynamicRow

class DeckTab(ttk.Frame):
    def __init__(self, container, controller, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller

        self.actions_area = ttk.LabelFrame(self, text="Actions Area")
        self.actions_area.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.uuid_label_var = tk.StringVar(value="UUID: Placeholder")  # replace Placeholder with actual UUID
        self.uuid_label = ttk.Label(self.actions_area, textvariable=self.uuid_label_var)
        self.uuid_label.pack()

        self.add_row_button = ttk.Button(self.actions_area, text="Add Row", command=self.add_row)
        self.add_row_button.pack()

        # Create a Canvas for the Calculation Form Area
        self.calculation_form_area_canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.calculation_form_area_canvas.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)

        # Create a Scrollbar and add it to the Calculation Form Area Canvas
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.calculation_form_area_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the Canvas to use the Scrollbar
        self.calculation_form_area_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a Frame inside the Canvas
        self.calculation_form_area = ttk.LabelFrame(self.calculation_form_area_canvas, text="Calculation Form Area")
        self.calculation_form_area_window = self.calculation_form_area_canvas.create_window((0,0), window=self.calculation_form_area, anchor='nw')
        
        # Configure the Canvas to adjust the scroll region whenever the size of the inner Frame changes
        self.calculation_form_area.bind("<Configure>", self.on_frame_configure)

        self.dynamic_rows = []
        for _ in range(1):  # replace with the actual number of rows you want
            self.add_row()

        self.final_cost_area = ttk.LabelFrame(self, text="Final Cost Area")
        self.final_cost_area.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

        self.calculate_final_cost_button = ttk.Button(self.final_cost_area, text="Calculate Final", command=self.calculate_final_cost)
        self.calculate_final_cost_button.pack()

        self.final_cost_label_var = tk.StringVar()
        self.final_cost_label = ttk.Label(self.final_cost_area, textvariable=self.final_cost_label_var)
        self.final_cost_label.pack()

    def add_row(self):
        if len(self.dynamic_rows) >= 10:
            tk.messagebox.showerror("Error", "Cannot add more than 10 rows.")
            return

        row = DynamicRow(self.calculation_form_area, self.controller)
        row.pack()
        self.dynamic_rows.append(row)

    def calculate_final_cost(self):
        final_cost = sum(row.calculate_cost() for row in self.dynamic_rows)
        self.final_cost_label_var.set(f"Final Cost: {final_cost}")

    def on_frame_configure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.calculation_form_area_canvas.configure(scrollregion=self.calculation_form_area_canvas.bbox("all"))
        # Update the width of the calculation_form_area
        self.calculation_form_area_canvas.itemconfig(self.calculation_form_area_window, width=self.calculation_form_area_canvas.winfo_width())
