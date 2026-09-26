from html import escape
from pathlib import Path


class GeneradorReportes:
    def __init__(self, datos, directorio_salida=None):
        self.datos = datos
        self.estadisticas = datos["estadisticas"]
        self.clasificacion = datos["clasificacion"]
        self.directorio_salida = Path(
            directorio_salida
            or Path(__file__).resolve().parent.parent / "report"
        )

    def generar_todos(self):
        self.directorio_salida.mkdir(parents=True, exist_ok=True)
        archivos = [
            self.generar_resumen(),
            self.generar_clases_por_dia(),
            self.generar_ocupacion(),
        ]
        return archivos

    def generar_resumen(self):
        filas = [
            ("Cursos", self.estadisticas["total_cursos"]),
            ("Catedráticos", self.estadisticas["total_catedraticos"]),
            ("Aulas", self.estadisticas["total_aulas"]),
            ("Clases", self.estadisticas["total_clases"]),
            ("Cursos sin clase", self.estadisticas["cursos_sin_clase"]),
            ("Aulas disponibles", self.estadisticas["aulas_disponibles"]),
            ("Minutos programados", self.estadisticas["minutos_totales"]),
            (
                "Promedio de minutos por clase",
                round(self.estadisticas["promedio_minutos_por_clase"], 2),
            ),
        ]
        contenido = "".join(
            f"<tr><th>{escape(str(nombre))}</th><td>{escape(str(valor))}</td></tr>"
            for nombre, valor in filas
        )
        return self.guardar(
            "resumen_general.html",
            "Resumen general",
            f"<table><tr><th>Indicador</th><th>Valor</th></tr>{contenido}</table>",
        )

    def generar_clases_por_dia(self):
        filas = []
        for dia, clases in self.clasificacion["clases_por_dia"].items():
            for clase in clases:
                filas.append(
                    "<tr>"
                    f"<td>{escape(dia)}</td>"
                    f"<td>{escape(clase['curso'])}</td>"
                    f"<td>{escape(clase['catedratico'])}</td>"
                    f"<td>{escape(clase['aula'])}</td>"
                    f"<td>{escape(clase['inicio'])} - {escape(clase['fin'])}</td>"
                    f"<td>{escape(clase['seccion'])}</td>"
                    "</tr>"
                )
        tabla = (
            "<table><tr><th>Día</th><th>Curso</th><th>Catedrático</th>"
            "<th>Aula</th><th>Horario</th><th>Sección</th></tr>"
            + "".join(filas)
            + "</table>"
        )
        return self.guardar("clases_por_dia.html", "Clases por día", tabla)

    def generar_ocupacion(self):
        aulas = "".join(
            f"<tr><td>{escape(str(nombre))}</td><td>{cantidad}</td></tr>"
            for nombre, cantidad in self.estadisticas["clases_por_aula"].items()
        )
        catedraticos = "".join(
            f"<tr><td>{escape(str(nombre))}</td><td>{cantidad}</td></tr>"
            for nombre, cantidad in self.estadisticas["clases_por_catedratico"].items()
        )
        contenido = (
            "<h2>Clases por aula</h2>"
            "<table><tr><th>Aula</th><th>Clases</th></tr>"
            f"{aulas}</table>"
            "<h2>Clases por catedrático</h2>"
            "<table><tr><th>Catedrático</th><th>Clases</th></tr>"
            f"{catedraticos}</table>"
        )
        return self.guardar("ocupacion.html", "Ocupación", contenido)

    def guardar(self, nombre, titulo, contenido):
        ruta = self.directorio_salida / nombre
        documento = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{escape(titulo)}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; }}
h1, h2 {{ color: #123b5d; }}
table {{ border-collapse: collapse; min-width: 560px; margin-bottom: 28px; }}
th, td {{ border: 1px solid #b8c4ce; padding: 9px 12px; text-align: left; }}
th {{ background: #dceaf2; }}
tr:nth-child(even) {{ background: #f5f8fa; }}
</style>
</head>
<body><h1>{escape(titulo)}</h1>{contenido}</body>
</html>"""
        ruta.write_text(documento, encoding="utf-8")
        return ruta
