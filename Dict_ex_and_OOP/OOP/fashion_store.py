class ClothingItem:
    def __init__(self, name, price):
        """
        Crea una nueva prenda con su nombre y precio original.

        Args:
            name  (str):   Nombre de la prenda.
            price (float): Precio original de la prenda.
        """
        self.name = name
        self.price = price
       
    def apply_discount(self, percent):
        """
        Aplica un descuento acumulativo al precio actual.

        Args:
            percent (float): Porcentaje de descuento entre 0 y 100.

        Raises:
            ValueError: Si percent es menor a 0 o mayor a 100.
        """
        if percent < 0 or percent > 100:
            raise ValueError("Percent must be between 0 and 100") ## raise detiene el programa
        self.price = self.price * (1 - percent / 100)
            
    def final_price(self):
        """
        Retorna el precio actual después de descuentos aplicados.

        Returns:
            float: Precio final de la prenda.
        """
        return self.price

        
    
item = ClothingItem("Jacket", 120)
item.apply_discount(10)
print(item.final_price())
