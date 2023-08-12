class Element:
    def __init__(self, nb_element, el_no, element_name, units):
        self.nb_element = nb_element
        self.el_no = el_no
        self.element_name = element_name
        self.units = units


class SteelElementsMData:
    def __init__(self):
        self.headers = ["NB Element", "El. No.", "Element Name", "Units"]
        self.elements = {
            "107": Element("Sup_Steel", 107, "107-Steel Open Girder/Beam", "LENGTH (ft.)"),
            "164": Element("Sup_Steel", 164, "164-Secondary Steel member", "Each"),
            "152": Element("Sup_Steel", 152, "152-Steel Floor Beam", "LENGTH (ft.)"),
            "515": Element("Sup_Steel", 515, "515-Steel Protective coating", "Sq.Ft"),
            "202": Element("Sup_Steel", 202, "202-Steel Column", "Each"),
            "219": Element("Sup_Steel", 219, "219-Steel Abutment", "LENGTH ft."),
            "231": Element("Sup_Steel", 231, "231-Steel Pier Cap", "LENGTH (ft.)"),
            "Others":Element("Sup_Steel", "0", "Others", "NA"),
        }

    def get_element(self, el_no):
        return self.elements.get(el_no, None)

    def get_elementsNumList(self):
        return list(self.elements.keys())

    def get_elementNamesList(self):
        return list(self.elements.values())
    
    def get_all_element_names(self):
        return [element.element_name for element in self.elements.values()]

    def get_headers(self):
        return self.headers
