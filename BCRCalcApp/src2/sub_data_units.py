class SubUnitsDB:
    def __init__(self):
        # self.unitsList={'LF': 'LF', 'SF': 'SF', 'CF': 'CF', 'LS': 'LS',
        #  'EA': 'EA', 'SY': 'SY', 'CY': 'CY', 'LB': 'LB',
        #   'AC': 'AC', 'STA': 'STA', 'HR': 'HR', 'TON': 'TON',
        #    'MG': 'MG', 'MO': 'MO', 'CYC': 'CYC', 'GAL': 'GAL',
        #     'SQ': 'SQ', 'DAY': 'DAY', 'LMI': 'LMI', 'MI': 'MI',
        #      '$/D': '$/D', 'TF': 'TF', 'WK': 'WK', 'VF': 'VF', 'BAG': 'BAG'}
        self.unitsList={'LF': 'LF', 'SF': 'SF', 'EACH': 'EACH'}


    def getSubUnitsList(self):
        return self.unitsList


