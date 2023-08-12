import re
import tkinter as tk
from tkinter import ttk
from steel_dynamic_row import SteelDynamicRow
# from database import Database
from tkinter import messagebox

class SteelTab(ttk.Frame):
    def __init__(self, container, controller, bridgeId, uuid, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller
        self.bridgeId=bridgeId
        self.uuid=uuid
        self.dynamic_rows = []
        self.calculation_form_area_canvas=None
        self.database = self.controller.database

        self.create_top_actions_area(0, 0, 1, 0.2)
        self.create_scrollable_canvas(0, 0.2, 0.98, 0.6)
        self.create_vertical_scroll(0.98, 0.2, 0.02, 0.6)
        self.create_horizontal_scroll(0,0.8,0.98,0.1)
        self.create_bottom_total_cost_area(0, 0.9, 1, 0.1)


    def create_top_actions_area(self, param_relx=0, param_rely=0, param_relwidth=1, param_relheight=0.2):
        # bridge_info_area Area (Left Frame)
        self.bridge_info_area = ttk.LabelFrame(self, text="Bridge Info Area", padding=10)
        self.bridge_info_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        label_caption_font = ("Arial", 16, "bold")
        label_value_font = ("Arial", 14, "normal")

        self.uuid_label_caption = ttk.Label(self.bridge_info_area, text="UUID", font=label_caption_font)
        self.uuid_label_caption.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.uuid_label_var = tk.StringVar(value=self.uuid)  # replace Placeholder with actual UUID
        self.uuid_label = ttk.Label(self.bridge_info_area, textvariable=self.uuid_label_var, font=label_value_font)
        self.uuid_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.bridgeId_label_caption = ttk.Label(self.bridge_info_area, text="BridgeID", font=label_caption_font)
        self.bridgeId_label_caption.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.bridgeId_label_var = tk.StringVar(value=self.bridgeId)  # replace Placeholder with actual bridgeId
        self.bridgeId_label = ttk.Label(self.bridge_info_area, textvariable=self.bridgeId_label_var, font=label_value_font)
        self.bridgeId_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Actions Area Frame for the "Add Row" button
        actions_area_frame = ttk.LabelFrame(self, text="Actions Area", padding=10)
        actions_area_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.add_row_button = ttk.Button(actions_area_frame, text="Add Row", command=self.add_row)
        self.add_row_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Set the background color to red using the style
        # style = ttk.Style(self)
        # style.configure('Background.TFrame', background='#e6e7e8')
        # self.bridge_info_area.configure(style='Background.TFrame')





    def create_scrollable_canvas(self,param_relx=0, param_rely=0.3, param_relwidth=1, param_relheight=0.7):
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
        # Final Cost Area with grid layout
        self.final_cost_area = ttk.LabelFrame(self, text="Final Cost Area")
        self.final_cost_area.place(relx=param_relx, rely=param_rely, relwidth=param_relwidth, relheight=param_relheight)

        # Calculate Final Cost button
        self.calculate_final_cost_button = ttk.Button(self.final_cost_area, text="Calculate Final", command=self.calculate_final_cost)
        self.calculate_final_cost_button.grid(row=0, column=0)

        # Final Cost Label
        self.final_cost_label_var = tk.StringVar()
        self.final_cost_label = ttk.Label(self.final_cost_area, textvariable=self.final_cost_label_var)
        self.final_cost_label.grid(row=0, column=1)

        # Store To DB button
        self.calculate_store_to_db_btn = ttk.Button(self.final_cost_area, text="Store To DB", command=self.store_to_db)
        self.calculate_store_to_db_btn.grid(row=0, column=2)

        # Reset button
        self.reset_button = ttk.Button(self.final_cost_area, text="Reset", command=self.reset_steel_tab)
        self.reset_button.grid(row=1, column=0, columnspan=3)

    def add_row(self):
        if len(self.dynamic_rows) >= 10:
            tk.messagebox.showerror("Error", "Cannot add more than 10 rows.")
            return

        row = SteelDynamicRow(self ,self.calculation_form_area, self.controller,self.bridgeId,self.uuid,)
        row.pack()
        self.dynamic_rows.append(row)
        self.on_canvas_configure(None)

    def reset_dynamic_rows(self):
        # Destroy all the dynamic rows and clear the list
        for row in self.dynamic_rows:
            row.destroy()
        self.dynamic_rows = []

    def reset_steel_tab(self):
        self.reset_dynamic_rows()
        self.final_cost_label_var.set("")

    def calculate_final_cost(self):
        final_cost=0
        for item in self.dynamic_rows:
            cost=0
            if(item.row_cost_entry.get()==""):
                cost=0
            else:
                cost=float(item.row_cost_entry.get().split(" ")[1])
            final_cost=final_cost+cost

        self.final_cost_label_var.set(f"Final Cost: $ {final_cost:.2f}")

    def is_valid_float(self,value):
    # Check if the value is a valid float in the format 'x.xx' or 'xx.xx'
        return bool(re.match(r'^\d+\.\d{2}$', value))

    def store_to_db(self):
        try:
            final_cost = self.final_cost_label_var.get().split(" ")[-1].strip()  # Use the last element after splitting

            # Check if final_cost is empty or invalid
            if not final_cost or not self.is_valid_float(final_cost):
                messagebox.showerror("Error", "Final cost is empty or not a valid float (e.g., 'x.xx' or 'xx.xx').")
                return

            final_cost = float(final_cost)  # Convert the final_cost to a float value

            # Check if the final_cost is 0
            if final_cost == 0:
                messagebox.showerror("Error", "Final cost cannot be $ 0.")
                return

            # Now you can store the final_cost to the database
            self.database.insert_bridge_steel_calc_hist(self.bridgeId, self.uuid, final_cost)
            messagebox.showinfo("Success", "Steel Final Cost stored to DB!")

        except ValueError:
            messagebox.showerror("Error", "Error processing the final cost. Please enter a valid float (e.g., 'x.xx' or 'xx.xx').")
        except IndexError:
            messagebox.showerror("Error", "Error processing the final cost. Please ensure it is in the correct format.")


    def on_canvas_configure(self, event):
        # Update the scroll region to reflect the size of the canvas content
        self.calculation_form_area_canvas.configure(scrollregion=self.calculation_form_area_canvas.bbox("all"))