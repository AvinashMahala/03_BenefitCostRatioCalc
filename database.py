#This file will manage the database connection and operations.

import sqlite3
from tkinter import messagebox

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("BenefitCostRatioApp.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS CalculationMetaData
                            (bridge_id text, uuid text)
                            """)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS BridgeDeckCalcHist
                            (bridge_id text, uuid text, final_cost real)
                            """)
        self.conn.commit()

    def insert_calculation_metadata(self, bridge_id, uuid):
        self.cursor.execute("""INSERT INTO CalculationMetaData VALUES (?, ?)""", (bridge_id, uuid))
        self.conn.commit()

    def insert_bridge_deck_calc_hist(self, bridge_id, uuid, final_cost):
        self.cursor.execute("""INSERT INTO BridgeDeckCalcHist VALUES (?, ?, ?)""", (bridge_id, uuid, final_cost))
        self.conn.commit()

    def insert_bridge_steel_calc_hist(self, bridge_id, uuid, final_cost):
        self.cursor.execute("""INSERT INTO BridgeSteelCalcHist VALUES (?, ?, ?)""", (bridge_id, uuid, final_cost))
        self.conn.commit()

    def insert_bridge_sup_calc_hist(self, bridge_id, uuid, final_cost):
        self.cursor.execute("""INSERT INTO BridgeSupCalcHist VALUES (?, ?, ?)""", (bridge_id, uuid, final_cost))
        self.conn.commit()

    def insert_bridge_sub_calc_hist(self, bridge_id, uuid, final_cost):
        self.cursor.execute("""INSERT INTO BridgeSubCalcHist VALUES (?, ?, ?)""", (bridge_id, uuid, final_cost))
        self.conn.commit()
    
    # Define a method to insert a row with specified values
    def insert_row(self, bid_item_num, bid_item_desc, unit_of_meas, avg_unit_price):
        query = "INSERT INTO BidItemPriceTxDot (BidItemNum, BidItemDesc, UnitOfMeas, AvgUnitPrice) VALUES (?, ?, ?, ?)"
        values = (bid_item_num, bid_item_desc, unit_of_meas, avg_unit_price)

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting row: {e}")
            return False

    def truncate_table(self, table_name):
        try:
            # Display a confirmation dialog
            confirmed = messagebox.askyesno("Confirm Truncate", f"Are you sure you want to truncate table '{table_name}'?")
            
            if confirmed:
                # Execute the SQL statement to truncate the table
                truncate_sql = f"DELETE FROM {table_name}"
                self.cursor.execute(truncate_sql)
                self.conn.commit()
                messagebox.showinfo("Success", f"Table '{table_name}' truncated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

