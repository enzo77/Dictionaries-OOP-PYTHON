import sqlite3
from contextlib import contextmanager
from typing import List, Tuple, Optional


# ============================================================================
# CUSTOM CONTEXT MANAGER
# ============================================================================

class TravelDatabase:
    """
    Context manager que gestiona de forma segura la conexión a SQLite.
    
    - Abre la conexión al entrar en el bloque with
    - Crea la tabla de trips si no existe
    - Hace commit si todo va bien
    - Hace rollback si ocurre una excepción
    - Cierra la conexión al salir
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
    
    def __enter__(self):
        """Abre la conexión y crea la tabla si es necesario."""
        self.connection = sqlite3.connect(self.db_path)
        self._create_table()
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión, hace commit o rollback según sea necesario."""
        if exc_type is None:
            # No hubo excepción: hacer commit
            self.connection.commit()
        else:
            # Hubo excepción: hacer rollback
            self.connection.rollback()
        
        self.connection.close()
        return False  # No suprimir excepciones
    
    def _create_table(self):
        """Crea la tabla de trips si no existe."""
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT NOT NULL,
                country TEXT NOT NULL,
                days INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)
        self.connection.commit()


# ============================================================================
# BASE REPOSITORY CLASS
# ============================================================================

class TravelRepository:
    """Clase base para el repositorio de viajes."""
    
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
    
    def add_trip(self, destination: str, country: str, days: int, price: float) -> None:
        """Añade un nuevo viaje a la base de datos."""
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO trips (destination, country, days, price) VALUES (?, ?, ?, ?)",
            (destination, country, days, price)
        )
        self.connection.commit()
    
    def get_all_trips(self) -> List[Tuple]:
        """Obtiene todos los viajes."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT destination, country, days, price FROM trips")
        return cursor.fetchall()


# ============================================================================
# MIXINS - COMPORTAMIENTO ADICIONAL
# ============================================================================

class TripSearchMixin:
    """
    Mixin que proporciona métodos de búsqueda de viajes.
    Requiere que la clase tenga self.connection.
    """
    
    def find_by_country(self, country: str) -> List[Tuple]:
        """Encuentra todos los viajes de un país específico."""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips WHERE country = ?",
            (country,)
        )
        return cursor.fetchall()
    
    def find_under_price(self, max_price: float) -> List[Tuple]:
        """Encuentra todos los viajes que cuestan menos que max_price."""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips WHERE price <= ?",
            (max_price,)
        )
        return cursor.fetchall()


class TripStatsMixin:
    """
    Mixin que proporciona métodos para calcular estadísticas de viajes.
    Requiere que la clase tenga self.connection.
    """
    
    def average_price(self) -> float:
        """Calcula el precio promedio de todos los viajes."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT AVG(price) FROM trips")
        result = cursor.fetchone()[0]
        return result if result is not None else 0.0
    
    def longest_trip(self) -> Optional[Tuple]:
        """Retorna el viaje más largo (mayor número de días)."""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips ORDER BY days DESC LIMIT 1"
        )
        return cursor.fetchone()


# ============================================================================
# CLASE CONCRETA - COMBINANDO TODO
# ============================================================================

class SQLiteTravelRepository(TravelRepository, TripSearchMixin, TripStatsMixin):
    """
    Repositorio completo de viajes que combina:
    - TravelRepository (base con operaciones CRUD básicas)
    - TripSearchMixin (búsquedas por país y precio)
    - TripStatsMixin (estadísticas de viajes)
    """
    pass


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Usar el context manager para gestionar la base de datos de forma segura
    with TravelDatabase("travel.db") as connection:
        repository = SQLiteTravelRepository(connection)
        
        # Añadir viajes
        print("Añadiendo viajes...")
        repository.add_trip("Kyoto", "Japan", 10, 1800.0)
        repository.add_trip("Rome", "Italy", 4, 650.0)
        repository.add_trip("Reykjavik", "Iceland", 6, 1400.0)
        print("✓ Viajes añadidos\n")
        
        # Pruebas de búsqueda
        print("Viajes en Italia:")
        print(repository.find_by_country("Italy"))
        print()
        
        print("Viajes que cuestan menos de 1500.0:")
        print(repository.find_under_price(1500.0))
        print()
        
        # Pruebas de estadísticas
        print("Precio promedio de los viajes:")
        print(repository.average_price())
        print()
        
        print("Viaje más largo:")
        print(repository.longest_trip())
