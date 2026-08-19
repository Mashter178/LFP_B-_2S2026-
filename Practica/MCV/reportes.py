from pathlib import Path

REPORT_DIR = Path(__file__).resolve().parent.parent / "report"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def archivo_reporte(nombre_archivo):
    return REPORT_DIR / nombre_archivo


def reporte_sudoku(sudokus, intentos, ruta_salida="reporte_sudokus.html"):
    """Reporte 1: Resumen por Sudoku"""
    filas = []

    for sudoku in sudokus:
        relacionados = [i for i in intentos if i.id_sudoku == sudoku.id_sudoku]
        total = len(relacionados)

        if total == 0:
            tiempo_promedio = 0
            tasa_exito = 0
        else:
            tiempos = [i.tiempo_segundos for i in relacionados if i.resuelto_correctamente]
            tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
            exitos = sum(1 for i in relacionados if i.resuelto_correctamente)
            tasa_exito = (exitos / total) * 100

        filas.append(f"""
            <tr>
                <td>{sudoku.id_sudoku}</td>
                <td>{sudoku.dificultad}</td>
                <td>{total}</td>
                <td>{tiempo_promedio:.2f}</td>
                <td>{tasa_exito:.2f}%</td>
            </tr>
        """)

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte 1 - Resumen por Sudoku</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Reporte 1: Resumen por Sudoku</h1>
        <table>
            <tr>
                <th>Identificador</th>
                <th>Dificultad</th>
                <th>Cantidad de intentos</th>
                <th>Tiempo promedio</th>
                <th>Tasa de éxito</th>
            </tr>
            {''.join(filas)}
        </table>
    </body>
    </html>
    """

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        archivo.write(html)

    return archivo_reporte("reporte_sudokus.html")


def reporte_jugador(jugadores, intentos, sudokus, ruta_salida="reporte_jugadores.html"):
    """Reporte 2: Rendimiento por Jugador"""
    filas = []

    for jugador in jugadores:
        relacionados = [i for i in intentos if i.carnet == jugador.carnet]
        tableros_intentados = len(relacionados)

        if relacionados:
            porcentaje_validez = sum(i.porcentaje_validez for i in relacionados) / tableros_intentados
            tiempo_promedio = sum(i.tiempo_segundos for i in relacionados) / tableros_intentados
            tableros_resueltos = sum(1 for i in relacionados if i.resuelto_correctamente)
        else:
            porcentaje_validez = 0
            tiempo_promedio = 0
            tableros_resueltos = 0

        filas.append(f"""
            <tr>
                <td>{jugador.nombre} {jugador.apellido}</td>
                <td>{jugador.carnet}</td>
                <td>{jugador.nivel}</td>
                <td>{tableros_intentados}</td>
                <td>{porcentaje_validez:.2f}%</td>
                <td>{tiempo_promedio:.2f}</td>
                <td>{tableros_resueltos}</td>
            </tr>
        """)

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte 2 - Rendimiento por Jugador</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Reporte 2: Rendimiento por Jugador</h1>
        <table>
            <tr>
                <th>Nombre completo</th>
                <th>Carnet</th>
                <th>Nivel</th>
                <th>Tableros intentados</th>
                <th>Porcentaje de validez promedio</th>
                <th>Tiempo promedio</th>
                <th>Tableros resueltos perfectamente</th>
            </tr>
            {''.join(filas)}
        </table>
    </body>
    </html>
    """

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        archivo.write(html)

    return archivo_reporte("reporte_jugadores.html")


def reporte_top10(intentos, jugadores, sudokus, ruta_salida="reporte_top10.html"):
    """Reporte 3: Top 10 mejores tiempos"""
    mejores = []

    for intento in intentos:
        if intento.resuelto_correctamente:
            jugador = next((j for j in jugadores if j.carnet == intento.carnet), None)
            sudoku = next((s for s in sudokus if s.id_sudoku == intento.id_sudoku), None)

            if jugador and sudoku:
                mejores.append({
                    "tiempo": intento.tiempo_segundos,
                    "carnet": intento.carnet,
                    "nombre": f"{jugador.nombre} {jugador.apellido}",
                    "id_tablero": intento.id_sudoku,
                    "dificultad": sudoku.dificultad,
                })

    mejores.sort(key=lambda x: x["tiempo"])
    mejores = mejores[:10]

    filas = []
    for i, item in enumerate(mejores, start=1):
        filas.append(f"""
            <tr>
                <td>{i}</td>
                <td>{item['carnet']}</td>
                <td>{item['nombre']}</td>
                <td>{item['id_tablero']}</td>
                <td>{item['dificultad']}</td>
                <td>{item['tiempo']}</td>
            </tr>
        """)

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte 3 - Top 10 Mejores Tiempos</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Reporte 3: Top 10 Mejores Tiempos</h1>
        <table>
            <tr>
                <th>Posición</th>
                <th>Carnet</th>
                <th>Nombre completo</th>
                <th>Identificador del tablero</th>
                <th>Dificultad</th>
                <th>Tiempo</th>
            </tr>
            {''.join(filas)}
        </table>
    </body>
    </html>
    """

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        archivo.write(html)

    return archivo_reporte("reporte_top10.html")


def generar_todos_los_reportes(sudokus, jugadores, intentos):
    reporte_sudoku(sudokus, intentos, "reporte_sudokus.html")
    generar_reporte_jugadores(jugadores, intentos, sudokus, "reporte_jugadores.html")
    reporte_top10(intentos, jugadores, sudokus, "reporte_top10.html")
    return "Reportes generados con éxito."


def generar_html_tabla(titulo, columnas, filas, nombre_archivo):
    cabeceras = "".join(f"<th>{col}</th>" for col in columnas)

    filas_html = ""
    for fila in filas:
        celdas = "".join(f"<td>{valor}</td>" for valor in fila)
        filas_html += f"<tr>{celdas}</tr>"

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{titulo}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>{titulo}</h1>
        <table>
            <tr>{cabeceras}</tr>
            {filas_html}
        </table>
    </body>
    </html>
    """

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html)

    return nombre_archivo


def reporte_resumen_sudokus(sudokus, intentos):
    filas = []

    for sudoku in sudokus:
        relacionados = [i for i in intentos if i.id_sudoku == sudoku.id_sudoku]
        total = len(relacionados)

        if total == 0:
            tiempo_promedio = 0
            tasa_exito = 0
        else:
            tiempos = [i.tiempo_segundos for i in relacionados if i.resuelto_correctamente]
            tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
            exitos = sum(1 for i in relacionados if i.resuelto_correctamente)
            tasa_exito = (exitos / total) * 100

        fila = [
            sudoku.id_sudoku,
            sudoku.dificultad,
            total,
            round(tiempo_promedio, 2),
            f"{tasa_exito:.2f}%"
        ]
        filas.append(fila)

    columnas = [
        "Identificador",
        "Dificultad",
        "Cantidad de intentos",
        "Tiempo promedio",
        "Tasa de éxito"
    ]

    return generar_html_tabla(
        "Reporte 1: Resumen por Sudoku",
        columnas,
        filas,
        "reporte_sudokus.html"
    )


def reporte_rendimiento_jugadores(jugadores, intentos):
    filas = []

    for jugador in jugadores:
        relacionados = [i for i in intentos if i.carnet == jugador.carnet]
        tableros_intentados = len(relacionados)

        if tableros_intentados > 0:
            porcentaje_validez = sum(i.porcentaje_validez for i in relacionados) / tableros_intentados
            tiempo_promedio = sum(i.tiempo_segundos for i in relacionados) / tableros_intentados
            tableros_resueltos = sum(1 for i in relacionados if i.resuelto_correctamente)
        else:
            porcentaje_validez = 0
            tiempo_promedio = 0
            tableros_resueltos = 0

        fila = [
            f"{jugador.nombre} {jugador.apellido}",
            jugador.carnet,
            jugador.nivel,
            tableros_intentados,
            f"{porcentaje_validez:.2f}%",
            round(tiempo_promedio, 2),
            tableros_resueltos
        ]
        filas.append(fila)

    columnas = [
        "Nombre completo",
        "Carnet",
        "Nivel",
        "Tableros intentados",
        "Porcentaje de validez promedio",
        "Tiempo promedio",
        "Tableros resueltos perfectamente"
    ]

    return generar_html_tabla(
        "Reporte 2: Rendimiento por Jugador",
        columnas,
        filas,
        "reporte_jugadores.html"
    )


def reporte_top_10_mejores_tiempos(intentos, jugadores, sudokus):
    mejores = []

    for intento in intentos:
        if intento.resuelto_correctamente:
            jugador = next((j for j in jugadores if j.carnet == intento.carnet), None)
            sudoku = next((s for s in sudokus if s.id_sudoku == intento.id_sudoku), None)

            if jugador and sudoku:
                mejores.append({
                    "tiempo": intento.tiempo_segundos,
                    "carnet": intento.carnet,
                    "nombre": f"{jugador.nombre} {jugador.apellido}",
                    "id_tablero": intento.id_sudoku,
                    "dificultad": sudoku.dificultad
                })

    mejores.sort(key=lambda x: x["tiempo"])
    mejores = mejores[:10]

    filas = []
    for posicion, item in enumerate(mejores, start=1):
        fila = [
            posicion,
            item["carnet"],
            item["nombre"],
            item["id_tablero"],
            item["dificultad"],
            item["tiempo"]
        ]
        filas.append(fila)

    columnas = [
        "Posición",
        "Carnet",
        "Nombre completo",
        "Identificador del tablero",
        "Dificultad",
        "Tiempo"
    ]

    return generar_html_tabla(
        "Reporte 3: Top 10 Mejores Tiempos",
        columnas,
        filas,
        "reporte_top10.html"
    )


def generar_todos_los_reportes(sudokus, jugadores, intentos):
    reporte_resumen_sudokus(sudokus, intentos)
    reporte_rendimiento_jugadores(jugadores, intentos)
    reporte_top_10_mejores_tiempos(intentos, jugadores, sudokus)
    return "Reportes generados con éxito."
