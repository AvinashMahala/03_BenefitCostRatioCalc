import tkinter as tk
from tkinter import ttk
from dynamic_row import DynamicRow


class DeckTab(ttk.Frame):
    def __init__(self, container, controller, bridgeId, uuid, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller
        self.bridgeId=bridgeId
        self.uuid=uuid
        self.dynamic_rows = []
        self.calculation_form_area_canvas=None

        self.create_top_actions_area(0, 0, 1, 0.2)
        self.create_scrollable_canvas(0, 0.2, 0.98, 0.6)
        self.create_vertical_scroll(0.98, 0.2, 0.02, 0.6)
        self.create_horizontal_scroll(0,0.8,0.98,0.1)
        # for _ in range(1):  # replace with the actual number of rows you want
        #     self.add_row()

        self.create_bottom_total_cost_area(0, 0.9, 1, 0.1)


    def create_top_actions_area(self, param_relx=0, param_rely=0, param_relwidth=1, param_relheight=0.2):
        self.actions_area = ttk.LabelFrame(self, text="Actions Area")
        self.actions_area.place(relx=param_relx, rely=param_rely, relwidth=param_relwidth, relheight=param_relheight)

        self.uuid_label_caption = ttk.Label(self.actions_area, text="UUID")
        self.uuid_label_caption.pack()
        self.uuid_label_var = tk.StringVar(value=self.uuid)  # replace Placeholder with actual UUID
        self.uuid_label = ttk.Label(self.actions_area, textvariable=self.uuid_label_var)
        self.uuid_label.pack()

        self.bridgeId_label_caption = ttk.Label(self.actions_area, text="BridgeID")
        self.bridgeId_label_caption.pack()
        self.bridgeId_label_var = tk.StringVar(value=self.bridgeId)  # replace Placeholder with actual bridgeId
        self.bridgeId_label = ttk.Label(self.actions_area, textvariable=self.bridgeId_label_var)
        self.bridgeId_label.pack()

        self.add_row_button = ttk.Button(self.actions_area, text="Add Row", command=self.add_row)
        self.add_row_button.pack()

    def create_scrollable_canvas(self,param_relx=0, param_rely=0.1, param_relwidth=1, param_relheight=0.7):
        # Create a Canvas for the Calculation Form Area
        self.calculation_form_area_canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.calculation_form_area_canvas.place(relx=param_relx, rely=param_rely, relwidth=param_relwidth, relheight=param_relheight)

        # Create a Frame inside the Canvas
        self.calculation_form_area = ttk.Frame(self.calculation_form_area_canvas, width=1)
        self.calculation_form_area_window = self.calculation_form_area_canvas.create_window((0, 0), window=self.calculation_form_area, anchor='nw')

        # Bind canvas resize to update the scrollable area
        self.bind("<Configure>", self.on_canvas_configure)

    def create_horizontal_scroll(self, parax_relx=0,param_rely=0.1, param_relwidth=1,param_relheight=0.1):
        # Create Horizontal Scrollbar and add it to the Calculation Form Area Canvas
        self.horizontal_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.calculation_form_area_canvas.xview)
        self.horizontal_scrollbar.place(relx=parax_relx, rely=param_rely, relwidth=param_relwidth, relheight=param_relheight)
        self.calculation_form_area_canvas.configure(xscrollcommand=self.horizontal_scrollbar.set)

    def create_vertical_scroll(self, parax_relx=0, param_rely=0.1, param_relwidth=0.1, param_relheight=1):
        # Create Vertical Scrollbar and add it to the Calculation Form Area Canvas
        self.vertical_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.calculation_form_area_canvas.yview)
        self.vertical_scrollbar.place(relx=parax_relx, rely=param_rely, relwidth=param_relwidth, relheight=param_relheight)
        self.calculation_form_area_canvas.configure(yscrollcommand=self.vertical_scrollbar.set)


    def create_bottom_total_cost_area(self,param_relx=0, param_rely=0.9, param_relwidth=1, param_relheight=0.1):
        self.final_cost_area = ttk.LabelFrame(self, text="Final Cost Area")
        self.final_cost_area.place(relx=param_relx, rely=param_rely, relwidth=param_relwidth, relheight=param_relheight)

        self.calculate_final_cost_button = ttk.Button(self.final_cost_area, text="Calculate Final", command=self.calculate_final_cost)
        self.calculate_final_cost_button.pack()

        self.final_cost_label_var = tk.StringVar()
        self.final_cost_label = ttk.Label(self.final_cost_area, textvariable=self.final_cost_label_var)
        self.final_cost_label.pack()

    def add_row(self):
        if len(self.dynamic_rows) >= 10:
            tk.messagebox.showerror("Error", "Cannot add more than 10 rows.")
            return

        row = DynamicRow(self ,self.calculation_form_area, self.controller,self.bridgeId,self.uuid,)
        row.pack()
        self.dynamic_rows.append(row)

    def calculate_final_cost(self):
        final_cost = sum(row.calculate_cost() for row in self.dynamic_rows)
        self.final_cost_label_var.set(f"Final Cost: {final_cost}")


    def on_canvas_configure(self, event):
        # Update the scroll region to reflect the size of the canvas content
        self.calculation_form_area_canvas.configure(scrollregion=self.calculation_form_area_canvas.bbox("all"))