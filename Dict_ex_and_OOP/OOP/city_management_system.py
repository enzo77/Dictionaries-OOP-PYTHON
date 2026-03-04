class City:
    """
    Representa una ciudad con su información administrativa básica.

    Attributes:
        name       (str):   Nombre de la ciudad.
        population (int):   Población actual. Debe ser positiva.
        country    (str):   País al que pertenece.
        budget     (float): Presupuesto actual. No puede ser negativo.
    """

    def __init__(self, name, population, country, budget):
        """
        Crea una ciudad con su información básica.

        Args:
            name       (str):   Nombre de la ciudad.
            population (int):   Población inicial. Debe ser positiva.
            country    (str):   País al que pertenece.
            budget     (float): Presupuesto inicial. No puede ser negativo.

        Raises:
            ValueError: Si population no es positiva.
            ValueError: Si budget es negativo.
        """
        if population <= 0:
            raise ValueError("Population must be positive")
        if budget < 0:
            raise ValueError("Budget must not be negative")
        self.name       = name
        self.population = population
        self.country    = country
        self.budget     = budget

    def description(self):
        """
        Retorna una descripción completa de la ciudad.

        Returns:
            str: Descripción con nombre, país, población y presupuesto.
        """
        return f"{self.name} ({self.country}) - Population: {self.population}, Budget: {self.budget}"

    def grow_population(self, amount):
        """
        Aumenta la población de la ciudad.

        Args:
            amount (int): Cantidad a aumentar. Debe ser positiva.

        Raises:
            ValueError: Si amount no es positivo.
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.population += amount

    def spend_budget(self, amount):
        """
        Reduce el presupuesto de la ciudad.

        Args:
            amount (float): Cantidad a gastar. Debe ser positiva
                            y no superar el presupuesto actual.

        Raises:
            ValueError: Si amount no es positivo.
            ValueError: Si amount supera el presupuesto actual.
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.budget:
            raise ValueError("Insufficient budget")
        self.budget -= amount

    def is_megacity(self):
        """
        Verifica si la ciudad es una megaciudad.

        Returns:
            bool: True si population >= 10_000_000, False si no.
        """
        return self.population >= 10_000_000

    def get_population(self):
        """
        Retorna la población actual de la ciudad.

        Returns:
            int: Población actual.
        """
        return self.population

    def get_budget(self):
        """
        Retorna el presupuesto actual de la ciudad.

        Returns:
            float: Presupuesto actual.
        """
        return self.budget



c = City("Paris", 2148000, "France", 5_000_000)

print(c.description())  
print(c.get_population()) 
print(c.get_budget())     

c.grow_population(200000)
print(c.get_population())  

print(c.is_megacity())   

c.spend_budget(1_500_000)
print(c.get_budget())    

# Megaciudad
tokyo = City("Tokyo", 13_960_000, "Japan", 20_000_000)
print(tokyo.is_megacity()) 