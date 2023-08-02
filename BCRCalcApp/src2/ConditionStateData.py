class ConditionStateData:
    def __init__(self, bid_item_num, bid_item_description, unit_of_measure, avg_unit_price):
        self.bid_item_num = bid_item_num
        self.bid_item_description = bid_item_description
        self.unit_of_measure = unit_of_measure
        self.avg_unit_price = avg_unit_price

    def __str__(self):
        return f"Condition State Data: Bid Item Num={self.bid_item_num}, " \
               f"Bid Item Description={self.bid_item_description}, " \
               f"Unit of Measure={self.unit_of_measure}, " \
               f"Avg Unit Price={self.avg_unit_price}"
