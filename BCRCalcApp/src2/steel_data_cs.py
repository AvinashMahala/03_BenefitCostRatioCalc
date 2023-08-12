import sqlite3

class SteelConditionStateData:
    def __init__(self, bid_item_num, bid_item_description, unit_of_measure, avg_unit_price):
        self.bid_item_num = bid_item_num
        self.bid_item_description = bid_item_description
        self.unit_of_measure = unit_of_measure
        self.avg_unit_price = avg_unit_price

def retrieve_data_by_bid_item_num(bid_item_num):
    try:
        # Connect to the SQLite database
        db_file = './BenefitCostRatioApp.db'
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            
            # Execute the query with the provided bid_item_num
            query = "SELECT BidItemDesc, UnitOfMeas, AvgUnitPrice " \
                    "FROM BidItemPriceTxDot " \
                    "WHERE BidItemNum = ?;"
            
            # Execute the query
            cursor.execute(query, (bid_item_num,))
            
            # Fetch the data
            data = cursor.fetchone()
            
            if data:
                # Create and return a SteelConditionStateData object with the retrieved data
                bid_item_description, unit_of_measure, avg_unit_price = data
                return SteelConditionStateData(bid_item_num, bid_item_description, unit_of_measure, avg_unit_price)
            else:
                return None
            
    except sqlite3.Error as e:
        print("Error reading data from the database:", e)
        return None
