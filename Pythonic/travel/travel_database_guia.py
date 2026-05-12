"""
GUÍA COMPLETA: SQLite Travel Database con Context Manager y Mixins
====================================================================

Este archivo contiene explicaciones detalladas y ejemplos avanzados.
"""

import sqlite3
from typing import List, Tuple, Optional


# ============================================================================
# 1. ENTENDIENDO EL CONTEXT MANAGER
# ============================================================================

class TravelDatabase:
    """
    Un context manager es una clase que implementa dos métodos:
    
    __enter__: Se ejecuta cuando entras en el bloque 'with'
    __exit__: Se ejecuta cuando sales del bloque 'with'
    
    Esto permite gestionar recursos de forma segura (abrir/cerrar conexiones).
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
    
    def __enter__(self):
        """
        1. Abre la conexión a SQLite
        2. Crea la tabla si no existe
        3. Retorna la conexión para usarla en el bloque with
        """
        print(f"[__enter__] Abriendo conexión a {self.db_path}")
        self.connection = sqlite3.connect(self.db_path)
        self._create_table()
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Se ejecuta siempre al salir del bloque with, incluso si hay excepciones.
        
        Parámetros:
        - exc_type: Tipo de excepción (None si no hay)
        - exc_val: Valor de la excepción
        - exc_tb: Traceback de la excepción
        
        Comportamiento:
        - Si exc_type es None: No hubo excepción → hacer COMMIT
        - Si exc_type no es None: Hubo excepción → hacer ROLLBACK
        """
        if exc_type is None:
            print("[__exit__] ✓ Sin errores. Haciendo COMMIT")
            self.connection.commit()
        else:
            print(f"[__exit__] ✗ Error detectado: {exc_type.__name__}. Haciendo ROLLBACK")
            self.connection.rollback()
        
        print("[__exit__] Cerrando conexión")
        self.connection.close()
        
        # Retornar False significa que NO suprimimos la excepción
        # (se propagará al código que llamó el with)
        return False
    
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
        print("[_create_table] Tabla 'trips' lista")


# ============================================================================
# 2. ENTENDIENDO LOS MIXINS
# ============================================================================

"""
Un Mixin es una clase que proporciona funcionalidad OPCIONAL a otras clases.
Características:
- No se usa directamente (no instancias un Mixin)
- Se hereda junto con otras clases
- Añade métodos sin obligar a usar herencia profunda
- Útil para composición horizontal de comportamiento

Ventajas sobre herencia simple:
❌ Herencia simple:
    class Repository(SearchMixin):        # Si necesitas Stats, ¿dónde lo pones?
    class StatsRepository(SearchMixin):   # Duplicación

✓ Mixins múltiples:
    class FullRepository(Repository, SearchMixin, StatsMixin):
    # Limpio, flexible, sin duplicación
"""

class TravelRepository:
    """Clase base: operaciones CRUD fundamentales."""
    
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
    
    def add_trip(self, destination: str, country: str, days: int, price: float) -> None:
        """Inserta un nuevo viaje."""
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
    
    def delete_trip(self, destination: str) -> None:
        """Elimina un viaje por destino."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM trips WHERE destination = ?", (destination,))
        self.connection.commit()


class TripSearchMixin:
    """
    Mixin 1: Métodos de búsqueda
    
    Nota: Asume que la clase que lo hereda tiene self.connection
    """
    
    def find_by_country(self, country: str) -> List[Tuple]:
        """
        Busca viajes por país.
        
        Ejemplo:
            results = repo.find_by_country("Japan")
            # Retorna: [('Kyoto', 'Japan', 10, 1800.0), ...]
        """
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips WHERE country = ?",
            (country,)
        )
        return cursor.fetchall()
    
    def find_under_price(self, max_price: float) -> List[Tuple]:
        """
        Busca viajes que cuestan menos que un precio máximo.
        
        Ejemplo:
            results = repo.find_under_price(1500.0)
            # Retorna: [('Rome', 'Italy', 4, 650.0), ...]
        """
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips WHERE price <= ? ORDER BY price",
            (max_price,)
        )
        return cursor.fetchall()
    
    def find_by_duration_range(self, min_days: int, max_days: int) -> List[Tuple]:
        """Bonificación: busca viajes por rango de duración."""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips WHERE days BETWEEN ? AND ?",
            (min_days, max_days)
        )
        return cursor.fetchall()


class TripStatsMixin:
    """
    Mixin 2: Métodos de estadísticas
    
    Nota: También asume que la clase que lo hereda tiene self.connection
    """
    
    def average_price(self) -> float:
        """
        Calcula el precio promedio.
        
        Ejemplo:
            avg = repo.average_price()
            # Retorna: 1283.3333333333333
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT AVG(price) FROM trips")
        result = cursor.fetchone()[0]
        return result if result is not None else 0.0
    
    def longest_trip(self) -> Optional[Tuple]:
        """
        Encuentra el viaje más largo.
        
        Ejemplo:
            trip = repo.longest_trip()
            # Retorna: ('Kyoto', 'Japan', 10, 1800.0)
        """
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips ORDER BY days DESC LIMIT 1"
        )
        return cursor.fetchone()
    
    def shortest_trip(self) -> Optional[Tuple]:
        """Bonificación: encuentra el viaje más corto."""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips ORDER BY days ASC LIMIT 1"
        )
        return cursor.fetchone()
    
    def total_cost(self) -> float:
        """Bonificación: calcula el costo total de todos los viajes."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(price) FROM trips")
        result = cursor.fetchone()[0]
        return result if result is not None else 0.0
    
    def average_days(self) -> float:
        """Bonificación: calcula la duración promedio."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT AVG(days) FROM trips")
        result = cursor.fetchone()[0]
        return result if result is not None else 0.0


# ============================================================================
# 3. CLASE CONCRETA - COMBINANDO COMPONENTES
# ============================================================================

class SQLiteTravelRepository(TravelRepository, TripSearchMixin, TripStatsMixin):
    """
    Repositorio completo que hereda de:
    1. TravelRepository (base con CRUD)
    2. TripSearchMixin (búsquedas)
    3. TripStatsMixin (estadísticas)
    
    MRO (Method Resolution Order):
    SQLiteTravelRepository → TravelRepository → TripSearchMixin → TripStatsMixin → object
    
    Esto significa que si una clase padre tiene un método, se usa el primero en el MRO.
    """
    
    def get_summary(self) -> str:
        """Método adicional: resumen de la base de datos."""
        trips = self.get_all_trips()
        if not trips:
            return "No hay viajes registrados"
        
        return f"""
╔════════════════════════════════════════════╗
║         RESUMEN DE VIAJES                  ║
╠════════════════════════════════════════════╣
║ Total de viajes: {len(trips):2d}                      ║
║ Precio promedio: ${self.average_price():.2f}                  ║
║ Duración promedio: {self.average_days():.1f} días            ║
║ Costo total: ${self.total_cost():.2f}                     ║
║ Viaje más largo: {self.longest_trip()[0]:15s}          ║
║ Viaje más corto: {self.shortest_trip()[0]:15s}         ║
╚════════════════════════════════════════════╝
        """.strip()


# ============================================================================
# 4. EJEMPLOS DE USO
# ============================================================================

def ejemplo_basico():
    """Ejemplo básico: operaciones CRUD."""
    print("\n" + "="*60)
    print("EJEMPLO 1: Operaciones Básicas (CRUD)")
    print("="*60)
    
    with TravelDatabase(":memory:") as conn:
        repo = SQLiteTravelRepository(conn)
        
        # CREATE
        repo.add_trip("Kyoto", "Japan", 10, 1800.0)
        repo.add_trip("Rome", "Italy", 4, 650.0)
        repo.add_trip("Barcelona", "Spain", 5, 900.0)
        
        # READ
        print("\nTodos los viajes:")
        for trip in repo.get_all_trips():
            print(f"  {trip}")


def ejemplo_busquedas():
    """Ejemplo 2: Búsquedas usando TripSearchMixin."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Búsquedas")
    print("="*60)
    
    with TravelDatabase(":memory:") as conn:
        repo = SQLiteTravelRepository(conn)
        
        repo.add_trip("Kyoto", "Japan", 10, 1800.0)
        repo.add_trip("Rome", "Italy", 4, 650.0)
        repo.add_trip("Reykjavik", "Iceland", 6, 1400.0)
        repo.add_trip("Barcelona", "Spain", 5, 900.0)
        
        print("\nViajes en Italia:")
        print(repo.find_by_country("Italy"))
        
        print("\nViajes que cuestan menos de $1200:")
        print(repo.find_under_price(1200.0))
        
        print("\nViajes de 4-7 días:")
        print(repo.find_by_duration_range(4, 7))


def ejemplo_estadisticas():
    """Ejemplo 3: Estadísticas usando TripStatsMixin."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Estadísticas")
    print("="*60)
    
    with TravelDatabase(":memory:") as conn:
        repo = SQLiteTravelRepository(conn)
        
        repo.add_trip("Kyoto", "Japan", 10, 1800.0)
        repo.add_trip("Rome", "Italy", 4, 650.0)
        repo.add_trip("Reykjavik", "Iceland", 6, 1400.0)
        
        print(f"\nPrecio promedio: ${repo.average_price():.2f}")
        print(f"Duración promedio: {repo.average_days():.1f} días")
        print(f"Costo total: ${repo.total_cost():.2f}")
        print(f"Viaje más largo: {repo.longest_trip()}")
        print(f"Viaje más corto: {repo.shortest_trip()}")


def ejemplo_manejo_errores():
    """Ejemplo 4: Manejo de errores con el context manager."""
    print("\n" + "="*60)
    print("EJEMPLO 4: Manejo de Errores")
    print("="*60)
    
    print("\n--- Intento 1: Operación exitosa ---")
    try:
        with TravelDatabase(":memory:") as conn:
            repo = SQLiteTravelRepository(conn)
            repo.add_trip("Paris", "France", 3, 500.0)
            print("Viaje añadido correctamente")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n--- Intento 2: Operación con excepción ---")
    try:
        with TravelDatabase(":memory:") as conn:
            repo = SQLiteTravelRepository(conn)
            repo.add_trip("London", "UK", 5, 800.0)
            # Simular un error
            raise ValueError("¡Algo salió mal!")
            print("Esta línea no se ejecutará")
    except ValueError as e:
        print(f"Error capturado: {e}")


def ejemplo_resumen():
    """Ejemplo 5: Resumen completo."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Resumen Completo")
    print("="*60)
    
    with TravelDatabase(":memory:") as conn:
        repo = SQLiteTravelRepository(conn)
        
        viajes = [
            ("Kyoto", "Japan", 10, 1800.0),
            ("Rome", "Italy", 4, 650.0),
            ("Reykjavik", "Iceland", 6, 1400.0),
            ("Barcelona", "Spain", 5, 900.0),
            ("Sydney", "Australia", 12, 2500.0),
        ]
        
        for dest, country, days, price in viajes:
            repo.add_trip(dest, country, days, price)
        
        print(repo.get_summary())


# ============================================================================
# EJECUTAR EJEMPLOS
# ============================================================================

if __name__ == "__main__":
    ejemplo_basico()
    ejemplo_busquedas()
    ejemplo_estadisticas()
    ejemplo_manejo_errores()
    ejemplo_resumen()
    
    print("\n" + "="*60)
    print("✓ Todos los ejemplos completados")
    print("="*60)
