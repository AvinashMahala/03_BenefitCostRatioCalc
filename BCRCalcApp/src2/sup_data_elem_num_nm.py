class Element:
    def __init__(self, nb_element, el_no, element_name, units):
        self.nb_element = nb_element
        self.el_no = el_no
        self.element_name = element_name
        self.units = units


class SupElementsMData:
    def __init__(self):
        self.headers = ["NB Element", "El. No.", "Element Name", "Units"]
        self.elements = {
            "109": Element("Superstructures", 109, "109-Prestressed Concrete Open Girder/Beam", "LENGTH (ft.)"),
            "110": Element("Superstructures", 110, "110-Reinforced Concrete Open Girder Beam", "LENGTH (ft.)"),
            "154": Element("Superstructures", 154, "154-Prestressed Concrete Floor Beam", "LENGTH (ft.)"),
            "155": Element("Superstructures", 155, "155-Reinforced Concrete Floor Beam", "LENGTH (ft.)"),
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