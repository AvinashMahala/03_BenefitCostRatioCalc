class DeckDefectsData:
    def __init__(self):
        self.defectsList=[
            "Delamination / Spall / Patched Area (1080)",
            "Exposed Rebar (1090)",
            "Efflorescence / Rust Staining (1120)",
            "Cracking* (1130)",
            "Abrasion / Wear (1190)",
            "Distortion (1900)",
            "Settlement (4000)",
            "Damage (7000)",
            "None"
        ]

        self.defect_data_state1 = {
            "Delamination / Spall / Patched Area (1080)": "None",
            "Exposed Rebar (1090)":"None",
            "Efflorescence / Rust Staining (1120)":"427-6002,427-6003",
            "Cracking* (1130)":"780-6006,780-6007",
            "Abrasion / Wear (1190)":"439-6013",
            "Distortion (1900)":"None",
            "Settlement (4000)":"None",
            "Damage (7000)":"None",
            "None":"None"
        }
        self.defect_data_state2 = {
            "Delamination / Spall / Patched Area (1080)": "429-6002,700-6001,429-6007",
            "Exposed Rebar (1090)":"429-6002,700-6001",
            "Efflorescence / Rust Staining (1120)":"427-6002,427-6003,427-6005",
            "Cracking* (1130)":"780-6006,780-6007",
            "Abrasion / Wear (1190)":"439-6013,439-6002",
            "Distortion (1900)":"429-6009",
            "Settlement (4000)":"None",
            "Damage (7000)":"429-6009",
            "None":"None"
        }
        
        self.defect_data_state3 ={
            "Delamination / Spall / Patched Area (1080)": "429-6003,429-6004,429-6007,720-6001",
            "Exposed Rebar (1090)":"429-6003,429-6004,720-6001",
            "Efflorescence / Rust Staining (1120)":"427-6004,427-6006,427-6007",
            "Cracking* (1130)":"429-6003,780-6010,429-6004",
            "Abrasion / Wear (1190)":"439-6003,439-6007,439-6013",
            "Distortion (1900)":"429-6003,429-6004,720-6001",
            "Settlement (4000)":"495-6001,495-6002",
            "Damage (7000)":"429-6003,429-6004,720-6001",
            "None":"None"
        }
        self.defect_data_state4 = {
            "Delamination / Spall / Patched Area (1080)": "429-6005,429-6006",
            "Exposed Rebar (1090)":"429-6005,429-6006",
            "Efflorescence / Rust Staining (1120)":"429-6005,429-6006",
            "Cracking* (1130)":"429-6005,429-6006",
            "Abrasion / Wear (1190)":"429-6005,429-6006",
            "Distortion (1900)":"429-6005,429-6006",
            "Settlement (4000)":"429-6005,429-6006",
            "Damage (7000)":"429-6005,429-6006",
            "None":"None"
        }

    def getOnlyDefectsList(self):
        return self.defectsList
        
  
    def getDefectListForState(self,state):
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


