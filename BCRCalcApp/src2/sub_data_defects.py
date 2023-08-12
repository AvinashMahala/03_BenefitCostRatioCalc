class SubDefectsData:
    def __init__(self):
        self.defectsList = [
            "Delamination / Spall / Patched Area (1080)",
            "Exposed Rebar (1090)",
            "Efflorescence / Rust Staining (1120)",
            "Cracking* (1130)",
            "Abrasion / Wear (1190)",
            "Distortion (1900)",
            "Settlement (4000)",
            "Scour (6000)",
            "Damage (7000)",
            "None"
        ]

        self.defect_data_state1 = {
            "Delamination / Spall / Patched Area (1080)": "None,427-6002",
            "Exposed Rebar (1090)": "None",
            "Efflorescence / Rust Staining (1120)": "427-6002,427-6003,427-6005",
            "Cracking* (1130)": "780-6001,780-6005,780-6010",
            "Abrasion / Wear (1190)": "None",
            "Distortion (1900)": "None",
            "Settlement (4000)": "None",
            "Scour (6000)": "None",
            "Damage (7000)": "None",
            "None": "None,427-6002"
        }

        self.defect_data_state2 = {
            "Delamination / Spall / Patched Area (1080)": "429-6001,429-6002",
            "Exposed Rebar (1090)": "431-6002,429-6007",
            "Efflorescence / Rust Staining (1120)": "427-6002,427-6003",
            "Cracking* (1130)": "780-6003,780-6004",
            "Abrasion / Wear (1190)": "439-6013,439-6002",
            "Distortion (1900)": "None",
            "Settlement (4000)": "495-6001,495-6002",
            "Scour (6000)": "None",
            "Damage (7000)": "None"
        }

        self.defect_data_state3 = {
            "Delamination / Spall / Patched Area (1080)": "429-6009,429-6007,429-6008",
            "Exposed Rebar (1090)": "431-6002,431-6003,429-6007,429-6010,429-6011,429-6013,429-6009",
            "Efflorescence / Rust Staining (1120)": "427-6004,427-6006,427-6007,429-6007,429-6008",
            "Cracking* (1130)": "429-6009,429-6010,429-6011,429-6013,786-6002,429-6007,429-6008",
            "Abrasion / Wear (1190)": "429-6009,429-6010,429-6011,429-6013,786-6002,429-6007,429-6008",
            "Distortion (1900)": "429-6009,429-6010,429-6011,429-6013,786-6002",
            "Settlement (4000)": "495-6001,495-6002,786-6002,429-6007,429-6008",
            "Scour (6000)": "429-6009,429-6010,429-6011,429-6013,786-6002,429-6007,429-6008",
            "Damage (7000)": "429-6009,429-6010,429-6011,429-6013,786-6002,429-6007,429-6008"
        }

        self.defect_data_state4 = {
            "Delamination / Spall / Patched Area (1080)": "429-6013,420-6038,420-6039,420-6040,420-6042,420-6043,420-6044,420-6045,786-6002,429-6013,420-6037",
            "Exposed Rebar (1090)": "429-6013,786-6001,786-6002,788-6003,788-6004,422-6001,422-6002,429-6018",
            "Efflorescence / Rust Staining (1120)": "429-6013,427-6006,427-6007,422-6001,427-6004",
            "Cracking* (1130)": "429-6013,420-6037,420-6038,420-6039,420-6040,420-6042,786-6002",
            "Abrasion / Wear (1190)": "429-6013,420-6038,420-6039,420-6040,420-6042,420-6043,420-6044,420-6045,786-6002,420-6037",
            "Distortion (1900)": "429-6013,420-6038,420-6039,420-6040,420-6042,420-6043,420-6044,420-6045,786-6002,420-6037",
            "Settlement (4000)": "429-6013,420-6038,420-6039,420-6040,420-6042,420-6043,420-6044,420-6045,786-6002,420-6037",
            "Scour (6000)": "429-6013,420-6038,420-6039,420-6040,420-6042,420-6043,420-6044,420-6045,786-6002,420-6037",
            "Damage (7000)": "429-6013,420-6038,420-6039,420-6040,420-6042,420-6043,420-6044,420-6045,786-6002,420-6037"
        }

    def getOnlyDefectsList(self):
        return self.defectsList

    def getDefectListForState(self, state):
        if state == 1:
            return self.defect_data_state1
        elif state == 2:
            return self.defect_data_state2
        elif state == 3:
            return self.defect_data_state3
        elif state == 4:
            return self.defect_data_state4
        else:
            return None
