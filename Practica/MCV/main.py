from pathlib import Path

from importar import Controlador
from validar import calificar_intento
from reportes import (
    reporte_sudoku,
    reporte_jugador,
    reporte_top10
)
from vista import Vista
from reportes import REPORT_DIR


def main():
    vista = Vista()
    controlador = Controlador()

    base = Path(__file__).resolve().parent.parent / "test"
    
    controlador.sudokus = controlador.cargar_sudokus(base / "sudokus.lfp")
    controlador.usuarios = controlador.cargar_usuarios(base / "jugadores.lfp")
    controlador.partidas = controlador.cargar_partidas(base / "intentos.lfp", controlador.sudokus)

    while True:
        vista.mostrar_menu()
        opcion = vista.leer_opcion()

        if opcion == 1:
            try:
                ruta = base / "jugadores.lfp"
                controlador.usuarios = controlador.cargar_usuarios(ruta)
                vista.mostrar_resultado("Jugadores cargados correctamente.")
            except Exception as e:
                vista.mostrar_resultado(f"Error cargando jugadores: {e}")
            vista.pausar()

        elif opcion == 2:
            try:
                ruta = base / "sudokus.lfp"
                controlador.sudokus = controlador.cargar_sudokus(ruta)
                vista.mostrar_resultado("Sudokus cargados correctamente.")
                vista.mostrar_resultado(f"Cantidad de sudokus con dificultad 'medio': {controlador.AAA}")
            except Exception as e:
                vista.mostrar_resultado(f"Error cargando sudokus: {e}")
            vista.pausar()

        elif opcion == 3:
            try:
                ruta = base / "intentos.lfp"
                controlador.partidas = controlador.cargar_partidas(ruta, controlador.sudokus)
                vista.mostrar_resultado("Intentos cargados correctamente.")
            except Exception as e:
                vista.mostrar_resultado(f"Error cargando intentos: {e}")
            vista.pausar()

        elif opcion == 4:
            original = vista.leer_texto("Ingrese tablero original (81 caracteres): ")
            solucion = vista.leer_texto("Ingrese solución propuesta (81 caracteres): ")
            resultado = calificar_intento(original, solucion)
            vista.mostrar_resultado(resultado)
            vista.pausar()

        elif opcion == 5:
            try:
                archivo = str(REPORT_DIR / "resumen_sudoku.html")
                reporte_sudoku(controlador.sudokus, controlador.partidas, archivo)
                vista.mostrar_resultado("Reporte generado: resumen_sudoku.html")
            except Exception as e:
                vista.mostrar_resultado(f"Error generando reporte: {e}")
                vista.pausar()

        elif opcion == 6:
            try:
                archivo2 = str(REPORT_DIR / "rendimiento_jugador.html")
                reporte_jugador(controlador.usuarios, controlador.partidas, controlador.sudokus, archivo2)

                archivo3 = str(REPORT_DIR / "top10_tiempos.html")
                reporte_top10(controlador.partidas, controlador.usuarios, controlador.sudokus, archivo3)

                vista.mostrar_resultado("Reportes generados: rendimiento_jugador.html, top10_tiempos.html")
            except Exception as e:
                vista.mostrar_resultado(f"Error generando reporte: {e}")
                vista.pausar()

        elif opcion == 8:
            print("Saliendo...")
            vista.pausar()
            break

        else:
            vista.mostrar_resultado("Opción no válida.")
            vista.pausar()

if __name__ == "__main__":
    main()