class Meal:
    """
    Representa una comida con su nombre y calorías.

    Attributes:
        name     (str): Nombre de la comida.
        calories (int): Cantidad de calorías.
    """
    def __init__(self, name, calories):
        self.name     = name
        self.calories = calories
        
    def is_healthy(self):
    
        return self.calories < 500
    
m1 = Meal("Salad Bowl", 350)
print(m1.is_healthy()) 

m2 = Meal("Double Burger", 950)
print(m2.is_healthy()) 