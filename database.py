#This file will manage the database connection and operations.

import sqlite3

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

