class EcoProduct:
    """
    Representa un producto con su huella de CO2.

    Attributes:
        name          (str):   Nombre del producto.
        co2_footprint (float): Huella de CO2 del producto.
    """
    def __init__(self, name, co2_footprint):
        self.name          = name
        self.co2_footprint = co2_footprint

    def is_low_impact(self):
        return self.co2_footprint < 10


p1 = EcoProduct("Bamboo Toothbrush", 3)
print(p1.is_low_impact())  

p2 = EcoProduct("Plastic Bottle", 18)
print(p2.is_low_impact())  
