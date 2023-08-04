class Element:
    def __init__(self, nb_element, el_no, element_name, units):
        self.nb_element = nb_element
        self.el_no = el_no
        self.element_name = element_name
        self.units = units


class DeckElementsMData:
    def __init__(self):
        self.headers = ["NB Element", "El. No.", "Element Name", "Units"]
        self.elements = {
            "12": Element("Decks_Slabs", 12, "12-Reinforced Concrete Deck", "AREA (s. ft.)"),
            "13": Element("Decks_Slabs", 13, "13-Prestressed Concrete Deck", "AREA (s. ft.)"),
            "16": Element("Decks_Slabs", 16, "16-Reinforced Concrete Top Flange", "AREA (s. ft.)"),
            "38": Element("Decks_Slabs", 38, "38-Reinforced Concrete Slab", "AREA (s. ft.)"),
            "42": Element("Decks_Slabs", 42, "42-DeckA", "AREA (s. ft.)"),
            "510": Element("Decks_Slabs", 510, "510-Wearing Surfaces(Deck)", "AREA (s. ft.)"),
            "Others":Element("Decks_Slabs", "0", "Others", "NA"),
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


# # Example usage:
# elements = ElementsDataset()
# print(elements.get_headers())  # ['NB Element', 'El. No.', 'Element Name', 'Units']
# element = elements.get_element(13)
# print(f"{element.nb_element}, {element.el_no}, {element.element_name}, {element.units}")  
# # 'Decks / Slabs', 13, '13-Prestressed Concrete Deck', 'AREA (s. ft.)'
