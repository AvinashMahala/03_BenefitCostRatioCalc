import tkinter as tk
from tkinter import ttk
from ElementNumberNameMData import DeckElementsMData
from DeckDefectsMData import DefectDatabase
from DeckUnitsMData import DeckUnitsDB
from ConditionStateData import ConditionStateData
import sqlite3



def retrieve_data_by_bid_item_num(bid_item_num):
    # Connect to the SQLite database
    db_file = './BenefitCostRatioApp.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()


    try:
       
        table_name = 'BidItemPriceTxDot'
        
        # Execute the query with the provided bid_item_num
        query = "SELECT BidItemDesc, UnitOfMeas, AvgUnitPrice " \
            "FROM BidItemPriceTxDot " \
            "WHERE BidItemNum = ?;"
        
        # Execute the query
        cursor.execute(query, (bid_item_num,))
        
        # Fetch the data
        data = cursor.fetchone()
        # print(data)
        cs="None"
        if data:
            # Create and return a ConditionStateData object with the retrieved data
            bid_item_description, unit_of_measure, avg_unit_price = data
            cs=ConditionStateData(bid_item_num, bid_item_description, unit_of_measure, avg_unit_price)
        return cs
            
    except sqlite3.Error as e:
        print("Error reading data from the database:", e)

    finally:
        # Close the database connection
        conn.close()



class DynamicRow(ttk.Frame):
    def __init__(self, master, container, controller,bridgeId,uuid, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller
        self.master=master
        self.bridgeId=bridgeId
        self.uuid=uuid

        self.allDeckElemsData=DeckElementsMData()
        self.elemNumDrpDnValues=self.allDeckElemsData.get_elementsNumList()
        self.allDeckUnitsDict=DeckUnitsDB().getDeckUnitsList()

        self.allDeckDefectsData=DefectDatabase()
        self.defectsList=self.allDeckDefectsData.getOnlyDefectsList()
        self.DeckDefectsState1=self.allDeckDefectsData.getDefectListForState(1)
        self.DeckDefectsState2=self.allDeckDefectsData.getDefectListForState(2)
        self.DeckDefectsState3=self.allDeckDefectsData.getDefectListForState(3)
        self.DeckDefectsState4=self.allDeckDefectsData.getDefectListForState(4)
        #--------------------
        # Named frames
        self.bridge_info_frame = ttk.LabelFrame(self, text="Bridge Information")
        self.condition_state_1_frame = ttk.LabelFrame(self, text="Condition State 1")
        self.condition_state_2_frame = ttk.LabelFrame(self, text="Condition State 2")
        self.condition_state_3_frame = ttk.LabelFrame(self, text="Condition State 3")
        self.condition_state_4_frame = ttk.LabelFrame(self, text="Condition State 4")
        self.actions_frame = ttk.LabelFrame(self, text="Actions")
        self.cost_info_frame = ttk.LabelFrame(self, text="Cost Information")

        # Position frames
        self.bridge_info_frame.grid(column=0, row=0)
        self.condition_state_1_frame.grid(column=1, row=0)
        self.condition_state_2_frame.grid(column=2, row=0)
        self.condition_state_3_frame.grid(column=3, row=0)
        self.condition_state_4_frame.grid(column=4, row=0)
        self.actions_frame.grid(column=5, row=0)
        self.cost_info_frame.grid(column=6, row=0)

        # Dynamic row data
        self.element_type_var = tk.StringVar()
        self.defect_var = tk.StringVar()
        self.bid_item_var = tk.StringVar()
        self.intervention_description_var = tk.StringVar()
        self.unit_of_measure_var = tk.StringVar()
        self.unit_price_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        #--------------------
        # Bridge Information

        # Add widgets to respective frames
        # Bridge Information
        self.bridge_info_frame = ttk.LabelFrame(self, text="Bridge Information")
        self.bridge_info_frame.grid(column=0, row=0, padx=10, pady=10)
        # 1) 2 disabled text boxes displaying active bridge id and uuid.
        self.bridge_id_label = ttk.Label(self.bridge_info_frame, text="Bridge ID")
        self.bridge_id_var = tk.StringVar(value=self.bridgeId)  
        self.bridge_id_entry = ttk.Entry(self.bridge_info_frame, textvariable=self.bridge_id_var, state='disabled')

        self.bridge_uuid_label = ttk.Label(self.bridge_info_frame, text="Calculation UUID")
        self.bridge_uuid_var = tk.StringVar(value=self.uuid)
        self.bridge_uuid_entry = ttk.Entry(self.bridge_info_frame, textvariable=self.bridge_uuid_var, state='disabled')

        # 2) Input Box with label "Element Num" - It is a dropdown containing some values.
        self.element_num_var = tk.StringVar()
        self.element_num_label = ttk.Label(self.bridge_info_frame, text="Element Num")
        self.element_num_dropdown = ttk.Combobox(self.bridge_info_frame, textvariable=self.element_num_var, values=self.elemNumDrpDnValues, state="readonly")
        self.element_num_dropdown.bind('<<ComboboxSelected>>', self.on_element_num_selected)

        # 3) Input box with label "Element Type" - This is a input box which is autogenerated based on the "Element Num" value.
        self.element_type_var = tk.StringVar()
        self.element_type_label = ttk.Label(self.bridge_info_frame, text="Element Type")
        self.element_type_entry = ttk.Entry(self.bridge_info_frame, textvariable=self.element_type_var, state='disabled')

        # 4) Dropdown with label "Defect Name"
        self.defect_name_var = tk.StringVar()
        self.defect_name_label = ttk.Label(self.bridge_info_frame, text="Defect Name")
        self.defect_name_dropdown = ttk.Combobox(self.bridge_info_frame, textvariable=self.defect_name_var, values=self.defectsList, state="readonly")
        self.defect_name_dropdown.bind('<<ComboboxSelected>>', self.on_defect_name_selected)

        # 5) Disabled Input box with label "Total Quantity" autogenerated when a value in the dropdown "Defect Name" is selected.
        self.total_quantity_var = tk.StringVar()
        self.total_quantity_label = ttk.Label(self.bridge_info_frame, text="Total Quantity")
        self.total_quantity_entry = ttk.Entry(self.bridge_info_frame, textvariable=self.total_quantity_var, state='readonly')

        # 6) Disabled Input box with label "Units" autogenerated when a value in the dropdown "Defect Name" is selected.
        self.units_var = tk.StringVar()
        self.units_label = ttk.Label(self.bridge_info_frame, text="Units")
        # self.units_entry = ttk.Entry(self.bridge_info_frame, textvariable=self.units_var, state='disabled')
        
        self.units_dropdown = ttk.Combobox(self.bridge_info_frame, textvariable=self.units_var, values=list(self.allDeckUnitsDict.keys()), state="disabled")
        self.units_dropdown.bind('<<ComboboxSelected>>', self.on_units_dropdown_selected)



        # Grid layout
        self.bridge_id_label.grid(row=0,column=0)
        self.bridge_id_entry.grid(row=0, column=1)

        self.bridge_uuid_label.grid(row=1,column=0)
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
        
        # Condition State 1
        # Condition State 1 frame
        self.condition_state_1_frame = ttk.LabelFrame(self, text="Condition State 1")
        self.condition_state_1_frame.grid(column=1, row=0, padx=10, pady=10)

        # a) BidItem
        self.cs1_bid_item_var = tk.StringVar()
        self.cs1_bid_item_label = ttk.Label(self.condition_state_1_frame, text="BidItem")
        self.cs1_bid_item_dropdown = ttk.Combobox(self.condition_state_1_frame, textvariable=self.cs1_bid_item_var, state='readonly')
        self.cs1_bid_item_dropdown.bind('<<ComboboxSelected>>', self.on_bid_item_selected)

        # b) InterventionDescription
        self.cs1_intervention_description_var = tk.StringVar()
        self.cs1_intervention_description_label = ttk.Label(self.condition_state_1_frame, text="InterventionDescription")
        self.cs1_intervention_description_entry = ttk.Entry(self.condition_state_1_frame,textvariable=self.cs1_intervention_description_var, state='disabled')

			 
        # c) cs1_UnitOfMeasure
        self.cs1_unit_of_measure_var = tk.StringVar()
        self.cs1_unit_of_measure_label = ttk.Label(self.condition_state_1_frame, text="UnitOfMeasure")
        self.cs1_unit_of_measure_entry = ttk.Entry(self.condition_state_1_frame, textvariable=self.unit_of_measure_var, state='disabled')
			 
        # d) cs1_UnitPrice
        self.cs1_unit_price_var = tk.StringVar()
        self.cs1_unit_price_label = ttk.Label(self.condition_state_1_frame, text="UnitPrice")
        self.cs1_unit_price_entry = ttk.Entry(self.condition_state_1_frame, textvariable=self.unit_price_var, state='disabled')
			 
        # e) cs1_Quantity
        self.cs1_quantity_var = tk.StringVar()
        self.cs1_quantity_label = ttk.Label(self.condition_state_1_frame, text="Quantity")
        self.cs1_quantity_entry = ttk.Entry(self.condition_state_1_frame, textvariable=self.quantity_var, state='disabled')
			 
        # Grid layout for Condition State 1 frame
        self.cs1_bid_item_label.grid(row=0, column=0)
        self.cs1_bid_item_dropdown.grid(row=0, column=1)
        self.cs1_intervention_description_label.grid(row=1, column=0)
        self.cs1_intervention_description_entry.grid(row=1, column=1)
        self.cs1_unit_of_measure_label.grid(row=2, column=0)
        self.cs1_unit_of_measure_entry.grid(row=2, column=1)
        self.cs1_unit_price_label.grid(row=3, column=0)
        self.cs1_unit_price_entry.grid(row=3, column=1)
        self.cs1_quantity_label.grid(row=4, column=0)
        self.cs1_quantity_entry.grid(row=4, column=1)
        
        # Condition State 2
        self.condition_state_2_frame = ttk.LabelFrame(self, text="Condition State 2")
        self.condition_state_2_frame.grid(column=2, row=0, padx=10, pady=10)

        # a) BidItem
        self.bid_item_2_var = tk.StringVar()
        self.bid_item_2_label = ttk.Label(self.condition_state_2_frame, text="BidItem")
        self.bid_item_2_dropdown = ttk.Combobox(self.condition_state_2_frame, textvariable=self.bid_item_2_var, state='readonly')
        self.bid_item_2_dropdown.bind('<<ComboboxSelected>>', self.on_bid_item_2_selected)

        # b) InterventionDescription
        self.intervention_description_2_var = tk.StringVar()
        self.intervention_description_2_label = ttk.Label(self.condition_state_2_frame, text="InterventionDescription")
        self.intervention_description_2_entry = ttk.Entry(self.condition_state_2_frame, textvariable=self.intervention_description_2_var, state='disabled')

        # c) UnitOfMeasure
        self.unit_of_measure_2_var = tk.StringVar()
        self.unit_of_measure_2_label = ttk.Label(self.condition_state_2_frame, text="UnitOfMeasure")
        self.unit_of_measure_2_entry = ttk.Entry(self.condition_state_2_frame, textvariable=self.unit_of_measure_2_var, state='disabled')

        # d) UnitPrice
        self.unit_price_2_var = tk.StringVar()
        self.unit_price_2_label = ttk.Label(self.condition_state_2_frame, text="UnitPrice")
        self.unit_price_2_entry = ttk.Entry(self.condition_state_2_frame, textvariable=self.unit_price_2_var, state='disabled')

        # e) Quantity
        self.quantity_2_var = tk.StringVar()
        self.quantity_2_label = ttk.Label(self.condition_state_2_frame, text="Quantity")
        self.quantity_2_entry = ttk.Entry(self.condition_state_2_frame, textvariable=self.quantity_2_var, state='disabled')

        # Grid layout for Condition State 2 frame
        self.bid_item_2_label.grid(row=0, column=0)
        self.bid_item_2_dropdown.grid(row=0, column=1)
        self.intervention_description_2_label.grid(row=1, column=0)
        self.intervention_description_2_entry.grid(row=1, column=1)
        self.unit_of_measure_2_label.grid(row=2, column=0)
        self.unit_of_measure_2_entry.grid(row=2, column=1)
        self.unit_price_2_label.grid(row=3, column=0)
        self.unit_price_2_entry.grid(row=3, column=1)
        self.quantity_2_label.grid(row=4, column=0)
        self.quantity_2_entry.grid(row=4, column=1)

        
        # Condition State 3
        self.condition_state_3_frame = ttk.LabelFrame(self, text="Condition State 3")
        self.condition_state_3_frame.grid(column=3, row=0, padx=10, pady=10)

        # a) BidItem
        self.bid_item_3_var = tk.StringVar()
        self.bid_item_3_label = ttk.Label(self.condition_state_3_frame, text="BidItem")
        self.bid_item_3_dropdown = ttk.Combobox(self.condition_state_3_frame, textvariable=self.bid_item_3_var, state='disabled')
        self.bid_item_3_dropdown.bind('<<ComboboxSelected>>', self.on_bid_item_3_selected)

        # b) InterventionDescription
        self.intervention_description_3_var = tk.StringVar()
        self.intervention_description_3_label = ttk.Label(self.condition_state_3_frame, text="InterventionDescription")
        self.intervention_description_3_entry = ttk.Entry(self.condition_state_3_frame,textvariable=self.intervention_description_3_var, state='disabled')

        # c) UnitOfMeasure
        self.unit_of_measure_3_var = tk.StringVar()
        self.unit_of_measure_3_label = ttk.Label(self.condition_state_3_frame, text="UnitOfMeasure")
        self.unit_of_measure_3_entry = ttk.Entry(self.condition_state_3_frame, textvariable=self.unit_of_measure_3_var, state='disabled')

        # d) UnitPrice
        self.unit_price_3_var = tk.StringVar()
        self.unit_price_3_label = ttk.Label(self.condition_state_3_frame, text="UnitPrice")
        self.unit_price_3_entry = ttk.Entry(self.condition_state_3_frame, textvariable=self.unit_price_3_var, state='disabled')

        # e) Quantity
        self.quantity_3_var = tk.StringVar()
        self.quantity_3_label = ttk.Label(self.condition_state_3_frame, text="Quantity")
        self.quantity_3_entry = ttk.Entry(self.condition_state_3_frame, textvariable=self.quantity_3_var, state='disabled')

        # Grid layout for Condition State 3 frame
        self.bid_item_3_label.grid(row=0, column=0)
        self.bid_item_3_dropdown.grid(row=0, column=1)
        self.intervention_description_3_label.grid(row=1, column=0)
        self.intervention_description_3_entry.grid(row=1, column=1)
        self.unit_of_measure_3_label.grid(row=2, column=0)
        self.unit_of_measure_3_entry.grid(row=2, column=1)
        self.unit_price_3_label.grid(row=3, column=0)
        self.unit_price_3_entry.grid(row=3, column=1)
        self.quantity_3_label.grid(row=4, column=0)
        self.quantity_3_entry.grid(row=4, column=1)

        
        
        # Condition State 4
        self.condition_state_4_frame = ttk.LabelFrame(self, text="Condition State 4")
        self.condition_state_4_frame.grid(column=4, row=0, padx=10, pady=10)

        # a) BidItem
        self.bid_item_4_var = tk.StringVar()
        self.bid_item_4_label = ttk.Label(self.condition_state_4_frame, text="BidItem")
        self.bid_item_4_dropdown = ttk.Combobox(self.condition_state_4_frame, textvariable=self.bid_item_4_var, state='disabled')
        self.bid_item_4_dropdown.bind('<<ComboboxSelected>>', self.on_bid_item_4_selected)

        # b) InterventionDescription
        self.intervention_description_4_var = tk.StringVar()
        self.intervention_description_4_label = ttk.Label(self.condition_state_4_frame, text="InterventionDescription")
        self.intervention_description_4_entry = ttk.Entry(self.condition_state_4_frame,textvariable=self.intervention_description_4_var, state='disabled')

        # c) UnitOfMeasure
        self.unit_of_measure_4_var = tk.StringVar()
        self.unit_of_measure_4_label = ttk.Label(self.condition_state_4_frame, text="UnitOfMeasure")
        self.unit_of_measure_4_entry = ttk.Entry(self.condition_state_4_frame, textvariable=self.unit_of_measure_4_var, state='disabled')

        # d) UnitPrice
        self.unit_price_4_var = tk.StringVar()
        self.unit_price_4_label = ttk.Label(self.condition_state_4_frame, text="UnitPrice")
        self.unit_price_4_entry = ttk.Entry(self.condition_state_4_frame, textvariable=self.unit_price_4_var, state='disabled')

        # e) Quantity
        self.quantity_4_var = tk.StringVar()
        self.quantity_4_label = ttk.Label(self.condition_state_4_frame, text="Quantity")
        self.quantity_4_entry = ttk.Entry(self.condition_state_4_frame, textvariable=self.quantity_4_var, state='disabled')

        # Grid layout for Condition State 4 frame
        self.bid_item_4_label.grid(row=0, column=0)
        self.bid_item_4_dropdown.grid(row=0, column=1)
        self.intervention_description_4_label.grid(row=1, column=0)
        self.intervention_description_4_entry.grid(row=1, column=1)
        self.unit_of_measure_4_label.grid(row=2, column=0)
        self.unit_of_measure_4_entry.grid(row=2, column=1)
        self.unit_price_4_label.grid(row=3, column=0)
        self.unit_price_4_entry.grid(row=3, column=1)
        self.quantity_4_label.grid(row=4, column=0)
        self.quantity_4_entry.grid(row=4, column=1)

        
        # Actions
        # In the DynamicRow class, add this to the __init__ method where the button is created:
        remove_row_button = ttk.Button(self.actions_frame, text="REMOVE ROW", command=self.remove_row)
        remove_row_button.pack()


        calculate_button = ttk.Button(self.actions_frame, text="Calculate", command=self.calculate_cost)
        calculate_button.pack()

        
        # Cost Information
        cost_label = ttk.Label(self.cost_info_frame, text="Cost Information")
        cost_label.pack()

    def remove_row(self):
        # Get the parent container (the notebook tab)
        parent_container = self.master.master
        pp=self.master.master.master

        # Check if this dynamic row is the last row, and there are more than one rows
        if len(pp.dynamic_rows) > 1 and pp.dynamic_rows[-1] == self:
            # Destroy this dynamic row widget
            self.destroy()
            # Remove this dynamic row instance from the list
            pp.dynamic_rows.pop()

            # Update the grid layout of the parent container (the notebook tab)
            # to reorganize the remaining rows
            for i, row in enumerate(pp.dynamic_rows):
                row.grid(row=i, column=0, padx=5, pady=5)

            # If you want to perform any other actions after removing the row, do it here
        else:
            # If this is the only row, do not remove it
            print("Cannot remove the last row.")


    def calculate_cost(self):
        # Replace with your actual calculation logic
        try:
            quantity = int(self.quantity_var.get())
            unit_price = float(self.unit_price_var.get())
            cost = quantity * unit_price
            print("Total Cost:", cost)  # You can display the result in a label or any other way you prefer
        except ValueError:
            print("Invalid quantity or unit price")


    # def on_bid_item_selected(self, event):
    #     selected_bid_item = self.bid_item_var.get()

    #     # You should replace the following lines with actual calls to your data source
    #     # to fetch the corresponding data

    #     cs=retrieve_data_by_bid_item_num(selected_bid_item)
    #     self.cs1_quantity_entry['state'] = 'normal'  # enable Quantity entry

    #     self.intervention_description_var.set(f'Description for {selected_bid_item}')
    #     self.unit_of_measure_var.set(f'Unit for {selected_bid_item}')
    #     self.unit_price_var.set(f'Price for {selected_bid_item}')

        

    def on_bid_item_2_selected(self, event):
        selected_bid_item = self.bid_item_2_var.get()
        # print(selected_bid_item)
        cs=retrieve_data_by_bid_item_num(selected_bid_item)
        # print(cs)

        description = cs.bid_item_description  # Replace this with a function call to fetch description from the database
        self.intervention_description_2_var.set(description)

        unit_of_measure = cs.unit_of_measure  # Replace this with a function call to fetch unit of measure from the database
        self.unit_of_measure_2_var.set(unit_of_measure)

        unit_price = cs.avg_unit_price  # Replace this with a function call to fetch unit price from the database
        self.unit_price_2_var.set(unit_price)

        self.quantity_2_entry['state'] = 'normal'

    def on_bid_item_3_selected(self, event):
        selected_bid_item = self.bid_item_3_var.get()
        # print(selected_bid_item)
        cs=retrieve_data_by_bid_item_num(selected_bid_item)
        # print(cs)

        description = cs.bid_item_description  # Replace this with a function call to fetch description from the database
        self.intervention_description_3_var.set(description)

        unit_of_measure = cs.unit_of_measure  # Replace this with a function call to fetch unit of measure from the database
        self.unit_of_measure_3_var.set(unit_of_measure)

        unit_price = cs.avg_unit_price  # Replace this with a function call to fetch unit price from the database
        self.unit_price_3_var.set(unit_price)

        self.quantity_3_entry['state'] = 'normal'
    
    def on_bid_item_4_selected(self, event):
        selected_bid_item = self.bid_item_4_var.get()
        # print(selected_bid_item)
        cs=retrieve_data_by_bid_item_num(selected_bid_item)
        # print(cs)

        description = cs.bid_item_description  # Replace this with a function call to fetch description from the database
        self.intervention_description_4_var.set(description)

        unit_of_measure = cs.unit_of_measure  # Replace this with a function call to fetch unit of measure from the database
        self.unit_of_measure_4_var.set(unit_of_measure)

        unit_price = cs.avg_unit_price  # Replace this with a function call to fetch unit price from the database
        self.unit_price_4_var.set(unit_price)

        self.quantity_4_entry['state'] = 'normal'

    def on_element_num_selected(self, event):
        selected_option = self.element_num_var.get()
        self.element_type_entry.delete(0, 'end')

        if selected_option == 'Others':
            self.element_type_entry['state'] = 'normal'
            self.element_type_entry.delete(0, 'end')
            
        else:
            self.element_type_var=self.allDeckElemsData.get_element(selected_option).element_name
            self.element_type_entry['state'] = 'normal'
            self.element_type_entry.insert(0, self.element_type_var)
            self.element_type_entry['state'] = 'disabled'

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
        self.set_condition_state_One_Fields(selected_defect_name)
        self.set_condition_state_Two_Fields(selected_defect_name)
        self.set_condition_state_Three_Fields(selected_defect_name)
        self.set_condition_state_Four_Fields(selected_defect_name)

    def set_condition_state_One_Fields(self,selected_defect_name):
        defect_bid_items_str=self.DeckDefectsState1[selected_defect_name]
        # self.cs1_bid_item_var=""
        if(defect_bid_items_str=="None"):
            self.cs1_bid_item_dropdown['values']=["None"]
            # self.cs1_bid_item_var="None"
            self.cs1_bid_item_dropdown['state']='readonly'
            
        else:
            valuesList=defect_bid_items_str.split(",")
            self.cs1_bid_item_dropdown['state']='readonly'
            self.cs1_bid_item_dropdown['values']=valuesList


    def set_condition_state_Two_Fields(self,selected_defect_name):
        defect_bid_items_str=self.DeckDefectsState2[selected_defect_name]
        # self.bid_item_2_var=""
        if(defect_bid_items_str=="None"):
            self.bid_item_2_dropdown['values']=["None"]
            # self.bid_item_2_var="None"
            self.bid_item_2_dropdown['state']='readonly'
            
        else:
            valuesList=defect_bid_items_str.split(",")
            self.bid_item_2_dropdown['state']='readonly'
            self.bid_item_2_dropdown['values']=valuesList

    def set_condition_state_Three_Fields(self,selected_defect_name):
        defect_bid_items_str=self.DeckDefectsState3[selected_defect_name]
        # self.bid_item_3_var=""
        if(defect_bid_items_str=="None"):
            self.bid_item_3_dropdown['values']=["None"]
            # self.bid_item_3_var="None"
            self.bid_item_3_dropdown['state']='readonly'
            
        else:
            valuesList=defect_bid_items_str.split(",")
            self.bid_item_3_dropdown['state']='readonly'
            self.bid_item_3_dropdown['values']=valuesList

    def set_condition_state_Four_Fields(self,selected_defect_name):
        defect_bid_items_str=self.DeckDefectsState4[selected_defect_name]
        # self.bid_item_4_var=""
        if(defect_bid_items_str=="None"):
            self.bid_item_4_dropdown['values']=["None"]
            # self.bid_item_4_var="None"
            self.bid_item_4_dropdown['state']='readonly'
            
        else:
            valuesList=defect_bid_items_str.split(",")
            self.bid_item_4_dropdown['state']='readonly'
            self.bid_item_4_dropdown['values']=valuesList


    def on_element_type_selected(self, event):
        selected_option = self.element_type_var.get()

        defect_options = ['Defect1', 'Defect2', 'Defect3']  # Replace this with a function call to fetch options from the database
        self.defect_dropdown['values'] = defect_options
        self.defect_dropdown['state'] = 'readonly'

    def on_defect_selected(self, event):
        bid_item_options = ['Bid1', 'Bid2', 'Bid3']  # Replace this with a function call to fetch options from the database
        self.bid_item_dropdown['values'] = bid_item_options
        self.bid_item_dropdown['state'] = 'readonly'

    def on_units_dropdown_selected(self, event):
        pass

    def on_bid_item_selected(self, event):
        selected_bid_item = self.cs1_bid_item_var.get()
        print(selected_bid_item)
        cs=retrieve_data_by_bid_item_num(selected_bid_item)
        print(cs)

        description = cs.bid_item_description  # Replace this with a function call to fetch description from the database
        self.cs1_intervention_description_entry.insert(tk.END, description)
        self.cs1_intervention_description_var.set(description)

        unit_of_measure = cs.unit_of_measure  # Replace this with a function call to fetch unit of measure from the database
        self.unit_of_measure_var.set(unit_of_measure)

        unit_price = cs.avg_unit_price  # Replace this with a function call to fetch unit price from the database
        self.unit_price_var.set(unit_price)

        self.cs1_quantity_entry['state'] = 'normal'

    def calculate_cost(self):
        # Replace with your actual calculation logic
        quantity = int(self.quantity_var.get())
        unit_price = float(self.unit_price_var.get())
        cost = quantity * unit_price
        return cost
