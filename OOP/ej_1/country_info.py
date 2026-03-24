class Country:
    """
    Representa un país con su nombre y población.

    Attributes:
        name       (str): Nombre del país.
        population (int): Población del país.
    """

    def __init__(self, name, population):
        """
        Crea un país con su nombre y población.

        Args:
            name       (str): Nombre del país.
            population (int): Población del país.
        """
        self.name       = name
        self.population = population

    def is_large(self):
        """
        Verifica si el país es grande por población.

        Returns:
            bool: True si population > 50_000_000, False si no.
        """
        return self.population > 50_000_000


c1 = Country("Spain", 47000000)
print(c1.is_large())  

c2 = Country("Germany", 83000000)
print(c2.is_large())  
