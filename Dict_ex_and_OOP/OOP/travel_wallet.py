class TravelWallet:
    """
    Representa una billetera de viaje con saldo y operaciones básicas.

    Attributes:
        _balance (float): Saldo actual de la billetera.
    """
    def __init__(self , initial_balance):
        self._balance = initial_balance
    
    def add_money(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount
    
    def spend_money(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient balance")
        self._balance -= amount
    
    def get_balance(self):
        """
        Retorna el saldo actual de la billetera.

        Returns:
            float: Saldo actual.
        """
        return self._balance
    
    
    
w = TravelWallet(200)
w.add_money(50)
w.spend_money(500)
print(w.get_balance())