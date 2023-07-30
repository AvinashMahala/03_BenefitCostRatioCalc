#This file will manage the database connection and operations.

import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("BenefitCostRatioApp.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS CalculationMetaData
                            (bridge_id text, uuid text)
                            """)
        self.conn.commit()

    def insert_calculation_metadata(self, bridge_id, uuid):
        self.cursor.execute("""INSERT INTO CalculationMetaData VALUES (?, ?)""", (bridge_id, uuid))
        self.conn.commit()

