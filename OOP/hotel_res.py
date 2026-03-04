class HotelRoom:
    """
    Representa una habitación de hotel con su capacidad y precio.

    Attributes:
        number          (int):   Número de la habitación.
        capacity        (int):   Capacidad máxima de huéspedes.
        price_per_night (float): Precio por noche.
        is_available    (bool):  Disponibilidad, empieza en True.
        current_guests  (int):   Huéspedes actuales, empieza en 0.
    """

    def __init__(self, number, capacity, price_per_night):
        """
        Crea una habitación con número, capacidad y precio por noche.

        Args:
            number          (int):   Número de la habitación.
            capacity        (int):   Capacidad máxima de huéspedes.
            price_per_night (float): Precio por noche.
        """
        self.number          = number
        self.capacity        = capacity
        self.price_per_night = price_per_night
        self.is_available    = True
        self.current_guests  = 0

    def book(self, guests):
        """
        Reserva la habitación con el número de huéspedes indicado.

        Args:
            guests (int): Número de huéspedes. Debe ser positivo
                          y no superar la capacidad.

        Raises:
            ValueError: Si guests no es positivo.
            ValueError: Si guests supera la capacidad.
            ValueError: Si la habitación ya está ocupada.
        """
        if guests <= 0:
            raise ValueError("Guests must be positive")
        if guests > self.capacity:
            raise ValueError("Exceeds room capacity")
        if not self.is_available:
            raise ValueError("Room already occupied")
        self.current_guests = guests
        self.is_available   = False

    def release(self):
        """
        Libera la habitación y resetea los huéspedes a 0.
        """
        self.current_guests = 0
        self.is_available   = True

    def status(self):
        """
        Retorna el estado actual de la habitación.

        Returns:
            str: 'Available' o 'Occupied (X guests)'.
        """
        if self.is_available:
            return "Available"
        return f"Occupied ({self.current_guests} guests)"

    def total_price(self, nights):

        if nights <= 0:
            raise ValueError("Nights must be positive")
        return self.price_per_night * nights


# Sesión de ejemplo
room = HotelRoom(101, 2, 80)

print(room.status()) 

room.book(2)
print(room.status())       

print(room.total_price(3)) 

room.release()
print(room.status())    