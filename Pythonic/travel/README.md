# Travel Database - Ejercicio Completo

## 📋 Descripción

Este ejercicio implementa un sistema de gestión de viajes usando:
- **Context Managers** para gestionar de forma segura conexiones a SQLite
- **Mixins** para añadir comportamiento opcional sin herencia profunda
- **SQLite** para persistencia de datos

## 📁 Archivos Incluidos

### 1. `travel_database.py` ⭐
**Solución limpia y completa lista para producción**
- Implementación principal del ejercicio
- Código profesional y bien comentado
- Ejecutable directamente para ver el ejemplo del enunciado

```bash
python travel_database.py
```

**Salida esperada:**
```
Viajes en Italia:
[('Rome', 'Italy', 4, 650.0)]

Viajes que cuestan menos de 1500.0:
[('Rome', 'Italy', 4, 650.0), ('Reykjavik', 'Iceland', 6, 1400.0)]

Precio promedio de los viajes:
1283.3333333333333

Viaje más largo:
('Kyoto', 'Japan', 10, 1800.0)
```

### 2. `travel_database_guia.py`
**Versión con explicaciones extendidas**
- Comentarios detallados en cada clase
- 5 ejemplos completos de uso
- Manejo de errores con context manager
- Salida con debugging para ver el flujo

```bash
python travel_database_guia.py
```

**Ejemplos incluidos:**
1. Operaciones CRUD básicas
2. Búsquedas (por país, por precio)
3. Estadísticas (promedio, más largo)
4. Manejo de errores
5. Resumen completo

### 3. `travel_database_tests.py`
**Suite completa de pruebas unitarias**
- 20 pruebas de diferentes aspectos
- Cobertura de context manager, mixins, búsquedas y estadísticas
- Prueba del ejemplo exacto del enunciado
- ✅ Todas las pruebas pasan

```bash
python travel_database_tests.py
```

**Resultado:** ✅ 20/20 pruebas exitosas

### 4. `travel_database_conceptos.txt`
**Explicaciones teóricas visuales**
- Diagramas ASCII
- Flujos de ejecución
- Comparativas (herencia vs mixins)
- MRO (Method Resolution Order)
- Seguridad SQL (SQL Injection)
- Transacciones (COMMIT vs ROLLBACK)

## 🎯 Conceptos Clave

### Context Manager (`TravelDatabase`)

```python
with TravelDatabase("travel.db") as connection:
    # __enter__:
    # ✓ Abre conexión SQLite
    # ✓ Crea tabla si no existe
    
    repository = SQLiteTravelRepository(connection)
    # ... operaciones ...
    
    # __exit__:
    # ✓ Si sin errores → COMMIT
    # ✓ Si hay errores → ROLLBACK
    # ✓ Siempre cierra la conexión
```

**Ventajas:**
- Garantiza cierre seguro de recursos
- Manejo automático de transacciones
- Código limpio y seguro

### Mixins (Comportamiento Opcional)

```python
class SQLiteTravelRepository(
    TravelRepository,      # Base: CRUD
    TripSearchMixin,       # Búsquedas
    TripStatsMixin         # Estadísticas
):
    pass
```

**Ventajas:**
- Flexibilidad sin jerarquías profundas
- Reutilización de código
- Separación clara de responsabilidades

### Estructura de la BD

```
trips table:
┌─────┬─────────────┬─────────┬──────┬────────┐
│ ID  │ DESTINATION │ COUNTRY │ DAYS │ PRICE  │
├─────┼─────────────┼─────────┼──────┼────────┤
│  1  │    Kyoto    │  Japan  │  10  │ 1800.0 │
│  2  │    Rome     │  Italy  │   4  │  650.0 │
│  3  │ Reykjavik   │ Iceland │   6  │ 1400.0 │
└─────┴─────────────┴─────────┴──────┴────────┘
```

## 🚀 Cómo Usar

### Instalación
```bash
# No requiere instalación, solo Python 3.6+
# (sqlite3 viene incluido en Python)
```

### Uso Básico
```python
from travel_database import TravelDatabase, SQLiteTravelRepository

with TravelDatabase("travel.db") as connection:
    repository = SQLiteTravelRepository(connection)
    
    # Agregar viajes
    repository.add_trip("Kyoto", "Japan", 10, 1800.0)
    repository.add_trip("Rome", "Italy", 4, 650.0)
    
    # Buscar
    print(repository.find_by_country("Japan"))
    print(repository.find_under_price(1500.0))
    
    # Estadísticas
    print(repository.average_price())
    print(repository.longest_trip())
```

### Métodos Disponibles

#### Clase Base (CRUD)
- `add_trip(destination, country, days, price)` - Añadir viaje
- `get_all_trips()` - Obtener todos los viajes

#### TripSearchMixin (Búsquedas)
- `find_by_country(country)` - Buscar por país
- `find_under_price(max_price)` - Buscar por precio máximo

#### TripStatsMixin (Estadísticas)
- `average_price()` - Precio promedio
- `longest_trip()` - Viaje más largo

## 🧪 Pruebas

Ejecutar todas las pruebas:
```bash
python travel_database_tests.py
```

Las pruebas cubren:
- ✅ Context manager (crear tabla, commit, rollback)
- ✅ Operaciones CRUD
- ✅ Búsquedas por país y precio
- ✅ Estadísticas
- ✅ Casos límite (listas vacías, sin resultados)
- ✅ Ejemplo exacto del enunciado

## 📊 Ejemplo Completo

```python
with TravelDatabase("travel.db") as connection:
    repository = SQLiteTravelRepository(connection)

    # Agregar viajes
    repository.add_trip("Kyoto", "Japan", 10, 1800.0)
    repository.add_trip("Rome", "Italy", 4, 650.0)
    repository.add_trip("Reykjavik", "Iceland", 6, 1400.0)

    # Búsquedas
    print(repository.find_by_country("Italy"))
    # [('Rome', 'Italy', 4, 650.0)]
    
    print(repository.find_under_price(1500.0))
    # [('Rome', 'Italy', 4, 650.0), ('Reykjavik', 'Iceland', 6, 1400.0)]

    # Estadísticas
    print(repository.average_price())
    # 1283.3333333333333
    
    print(repository.longest_trip())
    # ('Kyoto', 'Japan', 10, 1800.0)
```

## 🔐 Seguridad

### Protección contra SQL Injection
```python
# ❌ INSEGURO
cursor.execute(f"SELECT * FROM trips WHERE country = '{country}'")

# ✅ SEGURO
cursor.execute("SELECT * FROM trips WHERE country = ?", (country,))
```

Todos los queries en este proyecto usan parámetros seguros.

### Transacciones ACID
- ✅ **Atomicity**: Operaciones se hacen toda o nada
- ✅ **Consistency**: BD siempre en estado válido
- ✅ **Isolation**: Operaciones no se interfieren
- ✅ **Durability**: Datos persisten con COMMIT

## 💡 Aprendizajes Clave

1. **Context Managers**: Gestión automática de recursos
2. **Mixins**: Composición flexible de comportamiento
3. **SQLite**: Uso de transacciones y queries paramétricos
4. **CRUD**: Patrones de acceso a datos
5. **Pruebas**: Importancia de cobertura unitaria

## 📚 Recursos Adicionales

- [PEP 343 - Context Managers](https://www.python.org/dev/peps/pep-0343/)
- [SQLite Documentation](https://sqlite.org/lang.html)
- [Python sqlite3 Module](https://docs.python.org/3/library/sqlite3.html)

## ✨ Mejoras Opcionales

Posibles extensiones del proyecto:

1. **Más mixins:**
   - `TripSortMixin`: Ordenamiento flexible
   - `TripFilterMixin`: Filtros complejos
   - `TripExportMixin`: Exportar a CSV/JSON

2. **Validación:**
   - Validar precios positivos
   - Validar duración válida
   - Validar campos no vacíos

3. **Funcionalidad:**
   - Actualizar viajes existentes
   - Eliminar viajes
   - Búsquedas más complejas

4. **Persistencia:**
   - Usar archivo en disco
   - Migraciones de schema
   - Backups automáticos

## 📄 Licencia

Este es un ejercicio educativo. Úsalo libremente para aprender.

---

**Creado con ❤️ para aprender Context Managers y Mixins en Python**
