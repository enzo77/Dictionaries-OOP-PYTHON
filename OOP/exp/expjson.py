import json
from pathlib import Path

# ── Base de datos JSON ────────────────────────────────────────────────────────

class DatabaseJSON:
    """Lee y escribe registros en un archivo JSON local."""

    def __init__(self, filepath: str, tabla: str):
        self.filepath = Path(filepath)
        self.tabla = tabla

    def _cargar(self) -> dict:
        if not self.filepath.exists():
            return {self.tabla: []}
        with open(self.filepath, encoding="utf-8") as f:
            return json.load(f)

    def _guardar(self, data: dict):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def leer_todos(self) -> list:
        return self._cargar().get(self.tabla, [])

    def agregar(self, registro: dict):
        data = self._cargar()
        registros = data.setdefault(self.tabla, [])
        nuevo_id = max((r["id"] for r in registros), default=0) + 1
        registro["id"] = nuevo_id
        registros.append(registro)
        self._guardar(data)
        return registro

    def actualizar(self, id_: int, campos: dict):
        data = self._cargar()
        for r in data.get(self.tabla, []):
            if r["id"] == id_:
                r.update(campos)
                break
        self._guardar(data)

    def eliminar(self, id_: int):
        data = self._cargar()
        data[self.tabla] = [r for r in data.get(self.tabla, []) if r["id"] != id_]
        self._guardar(data)


# ── Patrón Exportador (Template Method + Mixins) ──────────────────────────────

class Exportador:
    def exportar(self, datos):
        # template method — define el orden
        datos = self.validar(datos)
        datos = self.transformar(datos)
        return self.serializar(datos)

    def validar(self, datos): return datos
    def transformar(self, datos): return datos
    def serializar(self, datos): return str(datos)

class FiltroVaciosMixin:
    def validar(self, datos):
        datos = [d for d in datos if d]
        return super().validar(datos)

class UpperMixin:
    def transformar(self, datos):
        datos = [d.upper() for d in datos]
        return super().transformar(datos)

class JSONMixin:
    def serializar(self, datos):
        return json.dumps(datos)


class PDFMixin:
    """Serializa una lista de dicts a un PDF con fpdf2."""

    PDF_OUTPUT = "export.pdf"

    def serializar(self, datos):
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Exportacion de Productos", ln=True, align="C")
        pdf.ln(4)

        if datos:
            headers = list(datos[0].keys())
            col_w = 190 // len(headers)
            pdf.set_font("Helvetica", "B", 10)
            for h in headers:
                pdf.cell(col_w, 8, str(h).capitalize(), border=1)
            pdf.ln()
            pdf.set_font("Helvetica", size=9)
            for row in datos:
                for h in headers:
                    pdf.cell(col_w, 7, str(row.get(h, "")), border=1)
                pdf.ln()

        pdf.output(self.PDF_OUTPUT)
        return f"PDF generado: {self.PDF_OUTPUT}"


class ExportadorCSV(FiltroVaciosMixin, UpperMixin, Exportador):
    pass

class ExportadorJSON(FiltroVaciosMixin, UpperMixin, JSONMixin, Exportador):
    pass

class ExportadorPDF(PDFMixin, Exportador):
    """Exporta directamente una lista de dicts a PDF (sin filtros de texto)."""
    pass


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    DB_PATH = Path(__file__).parent / "db.json"
    db = DatabaseJSON(DB_PATH, "productos")

    # Leer
    productos = db.leer_todos()
    print("Productos en BD:", json.dumps(productos, ensure_ascii=False, indent=2))

    # Escribir (agregar)
    nuevo = db.agregar({"nombre": "Mouse Inalambrico", "precio": 45.99, "stock": 20, "categoria": "electronica"})
    print(f"\nAgregado: {nuevo}")

    # Actualizar
    db.actualizar(nuevo["id"], {"precio": 39.99})
    print(f"Precio actualizado para id={nuevo['id']}")

    # Exportar a PDF
    todos = db.leer_todos()
    exp_pdf = ExportadorPDF()
    print("\n" + exp_pdf.exportar(todos))

    # Exportar strings a CSV / JSON (demo original)
    expCvs  = ExportadorCSV()
    expJson = ExportadorJSON()
    print(expCvs.exportar(["hola", "", "mundo", None, "python"]))
    print(expJson.exportar(["hola", "", "mundo", None, "python"]))   