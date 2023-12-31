import tkinter as tk
from tkinter import ttk
from sup_data_elem_num_nm import SupElementsMData
from sup_data_defects import SupDefectsData
from sup_data_units import SupUnitsDB
from sup_data_cs import SupConditionStateData
from sup_data_cs import retrieve_data_by_bid_item_num
import sqlite3
from tkinter import messagebox
from sup_validations import validate_total_quantity

class SupDynamicRow(ttk.Frame):
    def __init__(self, master, container, controller, bridgeId, uuid, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller
        self.master = master
        self.bridgeId = bridgeId
        self.uuid = uuid

        self.allSupElemsData = SupElementsMData()
        self.elemNumDrpDnValues = self.allSupElemsData.get_elementsNumList()
        self.allSupUnitsDict = SupUnitsDB().getSupUnitsList()
        self.allSupDefectsData = SupDefectsData()
        self.defectsList = self.allSupDefectsData.getOnlyDefectsList()

        self.SupDefectsState1=self.allSupDefectsData.getDefectListForState(1)
        self.SupDefectsState2=self.allSupDefectsData.getDefectListForState(2)
        self.SupDefectsState3=self.allSupDefectsData.getDefectListForState(3)
        self.SupDefectsState4=self.allSupDefectsData.getDefectListForState(4)

        self.init_ui()

    def init_ui(self):
        self.create_named_frames()
        self.create_bridge_information_widgets()
        self.create_condition_state_frames()
        self.create_actions_widgets()
        self.create_cost_information_widgets()

    def create_named_frames(self):
        self.bridge_info_frame = ttk.LabelFrame(self, text="Bridge Information")
        self.condition_state_frames = []
        for i in range(1, 5):
            self.condition_state_frames.append(ttk.LabelFrame(self, text=f"Condition State {i}"))
        self.actions_frame = ttk.LabelFrame(self, text="Actions")
        self.cost_info_frame = ttk.LabelFrame(self, text="Cost Information")

        # Position frames
        self.bridge_info_frame.grid(column=0, row=0)
        for i, frame in enumerate(self.condition_state_frames):
            frame.grid(column=i + 1, row=0)
        self.actions_frame.grid(column=5, row=0)
        self.cost_info_frame.grid(column=6, row=0)

    def create_bridge_information_widgets(self):
        # Bridge Information
        self.bridge_id_label = ttk.Label(self.bridge_info_frame, text="Bridge ID")
        self.bridge_id_var = tk.StringVar(value=self.bridgeId)
        self.bridge_id_entry = ttk.Entry(self.bridge_info_frame, textvariable=self.bridge_id_var, state='disabled')

        self.bridge_uuid_label = ttk.Label(self.bridge_info_frame, text="Calculation UUID")
        self.bridge_uuid_var = tk.StringVar(value=self.uuid)
        self.bridge_uuid_entry = ttk.Entry(self.bridge_info_frame, textvariable=self.bridge_uuid_var, state='disabled')

        self.element_num_var = tk.StringVar()
        self.element_num_label = ttk.Label(self.bridge_info_frame, text="Element Num")
        self.element_num_dropdown = ttk.Combobox(self.bridge_info_frame, textvariable=self.element_num_var, values=self.elemNumDrpDnValues, state="readonly")
        self.element_num_dropdown.bind('<<ComboboxSelected>>', self.on_element_num_selected)

        self.element_type_var = tk.StringVar()
        self.element_type_label = ttk.Label(self.bridge_info_frame, text="Element Type")
        self.element_type_entry = ttk.Entry(self.bridge_info_frame, textvariable=self.element_type_var, state='disabled')

        self.defect_name_var = tk.StringVar()
        self.defect_name_label = ttk.Label(self.bridge_info_frame, text="Defect Name")
        self.defect_name_dropdown = ttk.Combobox(self.bridge_info_frame, textvariable=self.defect_name_var, values=self.defectsList, state="readonly")
        self.defect_name_dropdown.bind('<<ComboboxSelected>>', self.on_defect_name_selected)

        self.total_quantity_var = tk.StringVar()
        self.total_quantity_var.trace_add('write', self.on_total_quantity_change)
        self.total_quantity_label = ttk.Label(self.bridge_info_frame, text="Total Quantity")
        self.total_quantity_entry = ttk.Entry(self.bridge_info_frame, textvariable=self.total_quantity_var, state='readonly')

        self.units_var = tk.StringVar()
        self.units_label = ttk.Label(self.bridge_info_frame, text="Units")
        self.units_dropdown = ttk.Combobox(self.bridge_info_frame, textvariable=self.units_var, values=list(self.allSupUnitsDict.keys()), state="disabled")
        self.units_dropdown.bind('<<ComboboxSelected>>', self.on_units_dropdown_selected)

        # Grid layout for Bridge Information
        self.bridge_id_label.grid(row=0, column=0)
        self.bridge_id_entry.grid(row=0, column=1)

        self.bridge_uuid_label.grid(row=1, column=0)
        self.bridge_uuid_entry.grid(row=1, column=1)

        self.element_num_label.grid(row=2, column=0)
        self.element_num_dropdown.grid(row=2, column=1)

        self.element_type_label.grid(row=3, column=0)
        self.element_type_entry.grid(row=3, column=1)

        self.defect_name_label.grid(row=4, column=0)
        self.defect_name_dropdown.grid(row=4, column=1)

        self.total_quantity_label.grid(row=5, column=0)
        self.total_quantity_entry.grid(row=5, column=1)

        self.units_label.grid(row=6, column=0)
        self.units_dropdown.grid(row=6, column=1)

    def create_condition_state_frames(self):
        for i, frame in enumerate(self.condition_state_frames):
            self.condition_state_frames[i].bid_item_var = tk.StringVar()
            self.condition_state_frames[i].intervention_description_var = tk.StringVar()
            self.condition_state_frames[i].unit_of_measure_var = tk.StringVar()
            self.condition_state_frames[i].unit_price_var = tk.StringVar()
            self.condition_state_frames[i].quantity_var = tk.StringVar()
            # Set up trace for quantity_var with index i
            self.condition_state_frames[i].quantity_var.trace_add('write', lambda *args, i=i: self.on_cs_quantity_change(i))

            self.condition_state_frames[i].bid_item_label = ttk.Label(frame, text="BidItem")
            self.condition_state_frames[i].bid_item_dropdown = ttk.Combobox(frame, textvariable=self.condition_state_frames[i].bid_item_var, state='readonly')
            
            self.condition_state_frames[i].intervention_description_label = ttk.Label(frame, text="InterventionDescription")
            self.condition_state_frames[i].intervention_description_entry = ttk.Entry(frame, textvariable=self.condition_state_frames[i].intervention_description_var, state='disabled')

            self.condition_state_frames[i].unit_of_measure_label = ttk.Label(frame, text="UnitOfMeasure")
            self.condition_state_frames[i].unit_of_measure_entry = ttk.Entry(frame, textvariable=self.condition_state_frames[i].unit_of_measure_var, state='disabled')

            self.condition_state_frames[i].unit_price_label = ttk.Label(frame, text="UnitPrice")
            self.condition_state_frames[i].unit_price_entry = ttk.Entry(frame, textvariable=self.condition_state_frames[i].unit_price_var, state='disabled')

            self.condition_state_frames[i].quantity_label = ttk.Label(frame, text="Quantity")
            self.condition_state_frames[i].quantity_entry = ttk.Entry(frame, textvariable=self.condition_state_frames[i].quantity_var, state='readonly')
            

            self.condition_state_frames[i].sub_calc_btn = ttk.Button(frame, text="Calculate", command=lambda i=i: self.sub_total_calculate(i))

            self.condition_state_frames[i].sub_total_entry_var = tk.StringVar()
            self.condition_state_frames[i].sub_total_entry = ttk.Entry(frame, textvariable=self.condition_state_frames[i].sub_total_entry_var, state='readonly')

            # Grid layout for Condition State frames
            self.condition_state_frames[i].bid_item_label.grid(row=0, column=0)
            self.condition_state_frames[i].bid_item_dropdown.grid(row=0, column=1)

            self.condition_state_frames[i].intervention_description_label.grid(row=1, column=0)
            self.condition_state_frames[i].intervention_description_entry.grid(row=1, column=1)

            self.condition_state_frames[i].unit_of_measure_label.grid(row=2, column=0)
            self.condition_state_frames[i].unit_of_measure_entry.grid(row=2, column=1)

            self.condition_state_frames[i].unit_price_label.grid(row=3, column=0)
            self.condition_state_frames[i].unit_price_entry.grid(row=3, column=1)

            self.condition_state_frames[i].quantity_label.grid(row=4, column=0)
            self.condition_state_frames[i].quantity_entry.grid(row=4, column=1)

            self.condition_state_frames[i].sub_calc_btn.grid(row=5, column=0)
            self.condition_state_frames[i].sub_total_entry.grid(row=5, column=1)
            # Attach ComboboxSelected event for each condition state
            self.condition_state_frames[i].bid_item_dropdown.bind('<<ComboboxSelected>>', lambda event, index=i: self.on_bid_item_selected(event, index))


    #------------Methods---------------
    #########################################################################
    def create_actions_widgets(self):
        # remove_row_button = ttk.Button(self.actions_frame, text="REMOVE ROW", command=self.remove_row)
        # remove_row_button.pack()

        self.calculate_button = ttk.Button(self.actions_frame, text="Calculate", command=self.calculate_cost)
        self.calculate_button.pack()
    #########################################################################
    def create_cost_information_widgets(self):
        self.cost_label = ttk.Label(self.cost_info_frame, text="Total Row Cost")
        self.cost_label.pack()

        self.row_cost_entry_var = tk.StringVar()
        self.row_cost_entry = ttk.Entry(self.cost_info_frame, textvariable=self.row_cost_entry_var, state="readonly")
        self.row_cost_entry.pack()
    #########################################################################
    def remove_row(self):
        # Get the parent container (the notebook tab)
        parent_container = self.master.master

        # Check if this dynamic row is the last row, and there are more than one rows
        if len(parent_container.dynamic_rows) > 1 and parent_container.dynamic_rows[-1] == self:
            # Destroy this dynamic row widget
            self.destroy()
            # Remove this dynamic row instance from the list
            parent_container.dynamic_rows.pop()
            # Update the grid layout of the parent container (the notebook tab)
            # to reorganize the remaining rows
            for i, row in enumerate(parent_container.dynamic_rows):
                row.grid(row=i, column=0, padx=5, pady=5)
            # If you want to perform any other actions after removing the row, do it here
        else:
            # If this is the only row, do not remove it
            print("Cannot remove the last row.")
    ##################################################################
    def calculate_cost(self):
        try:
            if len(self.condition_state_frames) > 0:
                q1 = float(self.condition_state_frames[0].sub_total_entry.get().split(" ")[1])
                q2 = float(self.condition_state_frames[1].sub_total_entry.get().split(" ")[1])
                q3 = float(self.condition_state_frames[2].sub_total_entry.get().split(" ")[1])
                q4 = float(self.condition_state_frames[3].sub_total_entry.get().split(" ")[1])
                row_total = q1 + q2 + q3 + q4
                self.row_cost_entry_var.set(f"$ {row_total:.2f}")
            else:
                messagebox.showerror("Error", "No condition state frames found.")
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Calculate Condition Frames Sub Total Cost First!")
    ##################################################################

    def on_total_quantity_change(self, *args):
        value = self.total_quantity_var.get()
        if not validate_total_quantity(value):
            self.total_quantity_var.set("")  # Clear the invalid entry
    
    def on_cs_quantity_change(self, index):
        value = self.condition_state_frames[index].quantity_var.get()
        if not validate_total_quantity(value):
            self.condition_state_frames[index].quantity_var.set("")  # Clear the invalid entry
    ##################################################################
    def on_element_num_selected(self, event):
        selected_option = self.element_num_var.get()
        self.element_type_entry.delete(0, 'end')
        if selected_option == 'Others':
            self.element_type_entry['state'] = 'normal'
            self.element_type_entry.delete(0, 'end') 
        else:
            self.element_type_var=self.allSupElemsData.get_element(selected_option).element_name
            self.element_type_entry['state'] = 'normal'
            self.element_type_entry.insert(0, self.element_type_var)
            self.element_type_entry['state'] = 'disabled'
    ##################################################################
    def on_defect_name_selected(self, event):
        selected_defect_name = self.defect_name_var.get().strip()
        if(selected_defect_name!="None"):
            self.total_quantity_entry['state']='normal'
            self.units_dropdown['state']='readonly'
        else:
            self.total_quantity_var.set('')
            self.units_var.set('')
            self.total_quantity_entry['state']='readonly'
            self.units_dropdown['state']='disabled'
        
        self.set_cs_fields(1,selected_defect_name)
        self.set_cs_fields(2,selected_defect_name)
        self.set_cs_fields(3,selected_defect_name)
        self.set_cs_fields(4,selected_defect_name)
    ##################################################################
    def on_element_type_selected(self, event):
        selected_option = self.element_type_var.get()
        defect_options = ['Defect1', 'Defect2', 'Defect3']  # Replace this with a function call to fetch options from the database
        self.defect_dropdown['values'] = defect_options
        self.defect_dropdown['state'] = 'readonly'
    #########################################################################
    def on_defect_selected(self, event):
        bid_item_options = ['Bid1', 'Bid2', 'Bid3']  # Replace this with a function call to fetch options from the database
        self.bid_item_dropdown['values'] = bid_item_options
        self.bid_item_dropdown['state'] = 'readonly'
    #########################################################################
    def on_units_dropdown_selected(self, event):
        pass
    #########################################################################
    def get_defect_bid_items_str(self, cs_index, selected_defect_name):
        if cs_index == 1:
            return self.SupDefectsState1[selected_defect_name]
        elif cs_index == 2:
            return self.SupDefectsState2[selected_defect_name]
        elif cs_index == 3:
            return self.SupDefectsState3[selected_defect_name]
        elif cs_index == 4:
            return self.SupDefectsState4[selected_defect_name]
        else:
            return "None"
    #########################################################################        
    def set_cs_fields(self, cs_index, selected_defect_name):
        defect_bid_items_str = self.get_defect_bid_items_str(cs_index, selected_defect_name)

        if defect_bid_items_str == "None":
            self.condition_state_frames[cs_index - 1].bid_item_dropdown['values'] = ["None"]
            self.condition_state_frames[cs_index - 1].bid_item_dropdown['state'] = 'readonly'
        else:
            valuesList = defect_bid_items_str.split(",")
            self.condition_state_frames[cs_index - 1].bid_item_dropdown['state'] = 'readonly'
            self.condition_state_frames[cs_index - 1].bid_item_dropdown['values'] = valuesList
    #########################################################################
    def on_bid_item_selected(self, event, index):
        selected_bid_item_var = self.condition_state_frames[index].bid_item_var
        selected_bid_item = selected_bid_item_var.get()
        cs = retrieve_data_by_bid_item_num(selected_bid_item)
        description = cs.bid_item_description
        unit_of_measure = cs.unit_of_measure
        unit_price = cs.avg_unit_price
        
        intervention_description_var = self.condition_state_frames[index].intervention_description_var
        unit_of_measure_var = self.condition_state_frames[index].unit_of_measure_var
        unit_price_var = self.condition_state_frames[index].unit_price_var
        quantity_entry = self.condition_state_frames[index].quantity_entry
        # Add more conditions for other condition states as needed

        intervention_description_var.set(description)
        unit_of_measure_var.set(unit_of_measure)
        unit_price_var.set(unit_price)
        quantity_entry['state'] = 'normal'
    #########################################################################
    def sub_total_calculate(self, index):
        if 0 <= index < len(self.condition_state_frames):
            try:
                quantity_entry = self.condition_state_frames[index].quantity_entry
                unit_price_entry = self.condition_state_frames[index].unit_price_entry
                sub_total_var = self.condition_state_frames[index].sub_total_entry_var
                quantity = int(quantity_entry.get())
                unit_price = float(unit_price_entry.get())
                cost = quantity * unit_price
                sub_total_var.set("$ {:.2f}".format(cost))
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity or unit price")
        else:
            print("Invalid index: Index out of range")