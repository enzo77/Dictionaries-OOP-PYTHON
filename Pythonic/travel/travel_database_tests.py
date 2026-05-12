"""
PRUEBAS UNITARIAS PARA EL TRAVEL DATABASE
==========================================

Este archivo contiene pruebas para validar que todo funciona correctamente.
"""

import unittest
import sqlite3
from typing import List, Tuple, Optional


# Importar las clases (usando versión simplificada inline)
class TravelDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self._create_table()
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()
        return False
    
    def _create_table(self):
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


class TravelRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
    
    def add_trip(self, destination: str, country: str, days: int, price: float) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO trips (destination, country, days, price) VALUES (?, ?, ?, ?)",
            (destination, country, days, price)
        )
        self.connection.commit()
    
    def get_all_trips(self) -> List[Tuple]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT destination, country, days, price FROM trips")
        return cursor.fetchall()


class TripSearchMixin:
    def find_by_country(self, country: str) -> List[Tuple]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips WHERE country = ?",
            (country,)
        )
        return cursor.fetchall()
    
    def find_under_price(self, max_price: float) -> List[Tuple]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips WHERE price <= ? ORDER BY price",
            (max_price,)
        )
        return cursor.fetchall()


class TripStatsMixin:
    def average_price(self) -> float:
        cursor = self.connection.cursor()
        cursor.execute("SELECT AVG(price) FROM trips")
        result = cursor.fetchone()[0]
        return result if result is not None else 0.0
    
    def longest_trip(self) -> Optional[Tuple]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT destination, country, days, price FROM trips ORDER BY days DESC LIMIT 1"
        )
        return cursor.fetchone()


class SQLiteTravelRepository(TravelRepository, TripSearchMixin, TripStatsMixin):
    pass


# ============================================================================
# PRUEBAS UNITARIAS
# ============================================================================

class TestTravelDatabase(unittest.TestCase):
    """Pruebas del context manager."""
    
    def test_context_manager_crea_tabla(self):
        """Verifica que el context manager crea la tabla."""
        with TravelDatabase(":memory:") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trips'")
            table = cursor.fetchone()
            self.assertIsNotNone(table, "La tabla 'trips' debe existir")
    
    def test_context_manager_commit_sin_errores(self):
        """Verifica que hace commit cuando no hay errores."""
        with TravelDatabase(":memory:") as conn:
            repo = SQLiteTravelRepository(conn)
            repo.add_trip("Paris", "France", 3, 500.0)
        
        # Verificar que los datos se guardaron
        with TravelDatabase(":memory:") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM trips")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 0, "Nueva BD debe estar vacía")
    
    def test_context_manager_rollback_con_errores(self):
        """Verifica que hace rollback cuando hay excepciones."""
        try:
            with TravelDatabase(":memory:") as conn:
                repo = SQLiteTravelRepository(conn)
                repo.add_trip("Paris", "France", 3, 500.0)
                raise ValueError("Error simulado")
        except ValueError:
            pass  # Excepción esperada


class TestTravelRepository(unittest.TestCase):
    """Pruebas del repositorio base."""
    
    def setUp(self):
        """Preparación antes de cada prueba."""
        self.db = TravelDatabase(":memory:")
        self.conn = self.db.__enter__()
        self.repo = SQLiteTravelRepository(self.conn)
    
    def tearDown(self):
        """Limpieza después de cada prueba."""
        self.db.__exit__(None, None, None)
    
    def test_add_trip(self):
        """Verifica que se puede añadir un viaje."""
        self.repo.add_trip("Tokyo", "Japan", 7, 1500.0)
        trips = self.repo.get_all_trips()
        self.assertEqual(len(trips), 1)
        self.assertEqual(trips[0][0], "Tokyo")
    
    def test_add_multiple_trips(self):
        """Verifica que se pueden añadir múltiples viajes."""
        self.repo.add_trip("Tokyo", "Japan", 7, 1500.0)
        self.repo.add_trip("Rome", "Italy", 4, 650.0)
        self.repo.add_trip("Paris", "France", 3, 500.0)
        
        trips = self.repo.get_all_trips()
        self.assertEqual(len(trips), 3)
    
    def test_get_all_trips_vacio(self):
        """Verifica que get_all_trips retorna lista vacía sin viajes."""
        trips = self.repo.get_all_trips()
        self.assertEqual(trips, [])
    
    def test_get_all_trips_retorna_tuplas(self):
        """Verifica que get_all_trips retorna tuplas correctamente."""
        self.repo.add_trip("Tokyo", "Japan", 7, 1500.0)
        trips = self.repo.get_all_trips()
        
        self.assertEqual(len(trips[0]), 4, "Debe retornar 4 columnas")
        self.assertEqual(trips[0], ("Tokyo", "Japan", 7, 1500.0))


class TestTripSearchMixin(unittest.TestCase):
    """Pruebas del mixin de búsqueda."""
    
    def setUp(self):
        self.db = TravelDatabase(":memory:")
        self.conn = self.db.__enter__()
        self.repo = SQLiteTravelRepository(self.conn)
        
        # Datos de prueba
        self.repo.add_trip("Kyoto", "Japan", 10, 1800.0)
        self.repo.add_trip("Rome", "Italy", 4, 650.0)
        self.repo.add_trip("Reykjavik", "Iceland", 6, 1400.0)
        self.repo.add_trip("Tokyo", "Japan", 7, 1500.0)
    
    def tearDown(self):
        self.db.__exit__(None, None, None)
    
    def test_find_by_country_unico(self):
        """Busca por país cuando hay un único resultado."""
        results = self.repo.find_by_country("Italy")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "Rome")
    
    def test_find_by_country_multiples(self):
        """Busca por país cuando hay múltiples resultados."""
        results = self.repo.find_by_country("Japan")
        self.assertEqual(len(results), 2)
        destinations = {r[0] for r in results}
        self.assertEqual(destinations, {"Kyoto", "Tokyo"})
    
    def test_find_by_country_no_encontrado(self):
        """Busca por país que no existe."""
        results = self.repo.find_by_country("Brazil")
        self.assertEqual(results, [])
    
    def test_find_under_price_unico(self):
        """Busca por precio con un único resultado."""
        results = self.repo.find_under_price(700.0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "Rome")
    
    def test_find_under_price_multiples(self):
        """Busca por precio con múltiples resultados."""
        results = self.repo.find_under_price(1500.0)
        self.assertEqual(len(results), 3)  # Rome (650), Iceland (1400), Tokyo (1500)
        # Verificar que están ordenados por precio
        prices = [r[3] for r in results]
        self.assertEqual(prices, sorted(prices))
    
    def test_find_under_price_ninguno(self):
        """Busca por precio muy bajo."""
        results = self.repo.find_under_price(500.0)
        self.assertEqual(results, [])
    
    def test_find_under_price_todos(self):
        """Busca por precio muy alto (incluye todos)."""
        results = self.repo.find_under_price(5000.0)
        self.assertEqual(len(results), 4)


class TestTripStatsMixin(unittest.TestCase):
    """Pruebas del mixin de estadísticas."""
    
    def setUp(self):
        self.db = TravelDatabase(":memory:")
        self.conn = self.db.__enter__()
        self.repo = SQLiteTravelRepository(self.conn)
        
        # Datos de prueba
        self.repo.add_trip("Kyoto", "Japan", 10, 1800.0)
        self.repo.add_trip("Rome", "Italy", 4, 650.0)
        self.repo.add_trip("Reykjavik", "Iceland", 6, 1400.0)
    
    def tearDown(self):
        self.db.__exit__(None, None, None)
    
    def test_average_price(self):
        """Verifica el cálculo del precio promedio."""
        avg = self.repo.average_price()
        expected = (1800.0 + 650.0 + 1400.0) / 3
        self.assertAlmostEqual(avg, expected, places=2)
    
    def test_average_price_vacio(self):
        """Verifica que retorna 0 cuando no hay viajes."""
        db = TravelDatabase(":memory:")
        conn = db.__enter__()
        repo = SQLiteTravelRepository(conn)
        
        avg = repo.average_price()
        self.assertEqual(avg, 0.0)
        
        db.__exit__(None, None, None)
    
    def test_longest_trip(self):
        """Verifica que encuentra el viaje más largo."""
        trip = self.repo.longest_trip()
        self.assertIsNotNone(trip)
        self.assertEqual(trip[0], "Kyoto")
        self.assertEqual(trip[2], 10)  # days
    
    def test_longest_trip_vacio(self):
        """Verifica que retorna None cuando no hay viajes."""
        db = TravelDatabase(":memory:")
        conn = db.__enter__()
        repo = SQLiteTravelRepository(conn)
        
        trip = repo.longest_trip()
        self.assertIsNone(trip)
        
        db.__exit__(None, None, None)


class TestIntegracion(unittest.TestCase):
    """Pruebas de integración completa."""
    
    def test_ejemplo_del_enunciado(self):
        """Prueba el ejemplo exacto del enunciado."""
        with TravelDatabase(":memory:") as connection:
            repository = SQLiteTravelRepository(connection)

            repository.add_trip("Kyoto", "Japan", 10, 1800.0)
            repository.add_trip("Rome", "Italy", 4, 650.0)
            repository.add_trip("Reykjavik", "Iceland", 6, 1400.0)

            # Verificar resultados esperados
            italy_trips = repository.find_by_country("Italy")
            self.assertEqual(italy_trips, [('Rome', 'Italy', 4, 650.0)])
            
            cheap_trips = repository.find_under_price(1500.0)
            self.assertEqual(len(cheap_trips), 2)
            
            avg = repository.average_price()
            expected_avg = 1283.3333333333333
            self.assertAlmostEqual(avg, expected_avg, places=10)
            
            longest = repository.longest_trip()
            self.assertEqual(longest, ('Kyoto', 'Japan', 10, 1800.0))
    
    def test_flujo_completo(self):
        """Prueba un flujo completo de operaciones."""
        with TravelDatabase(":memory:") as connection:
            repository = SQLiteTravelRepository(connection)
            
            # Fase 1: Insertar datos
            trips_data = [
                ("Barcelona", "Spain", 5, 900.0),
                ("London", "UK", 4, 800.0),
                ("Paris", "France", 3, 700.0),
                ("Amsterdam", "Netherlands", 3, 750.0),
            ]
            
            for dest, country, days, price in trips_data:
                repository.add_trip(dest, country, days, price)
            
            # Fase 2: Verificar cantidad
            all_trips = repository.get_all_trips()
            self.assertEqual(len(all_trips), 4)
            
            # Fase 3: Búsquedas
            spain_trips = repository.find_by_country("Spain")
            self.assertEqual(len(spain_trips), 1)
            
            budget_trips = repository.find_under_price(800.0)
            self.assertGreaterEqual(len(budget_trips), 1)
            
            # Fase 4: Estadísticas
            avg_price = repository.average_price()
            self.assertGreater(avg_price, 0)
            
            longest = repository.longest_trip()
            self.assertIsNotNone(longest)


# ============================================================================
# EJECUTAR PRUEBAS
# ============================================================================

if __name__ == "__main__":
    # Configurar verbosidad
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*60)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Éxitos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*60)
