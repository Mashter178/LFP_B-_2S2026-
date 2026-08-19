from pathlib import Path

from importar import Controlador
from validar import calificar_intento
from reportes import (
    reporte_sudoku,
    reporte_jugador,
    reporte_top10
)
from vista import Vista


def main():
    vista = Vista()
    controlador = Controlador()

    base = Path(__file__).resolve().parent.parent / "test"

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
            except Exception as e:
                vista.mostrar_resultado(f"Error cargando sudokus: {e}")
            vista.pausar()

        elif opcion == 3:
            try:
                ruta = base / "intentos.lfp"
                controlador.partidas = controlador.cargar_partidas(ruta)
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
                reporte_sudoku(controlador.sudokus, controlador.partidas, "reporte_sudokus.html")
                vista.mostrar_resultado("Reporte generado: reporte_sudokus.html")
            except Exception as e:
                vista.mostrar_resultado(f"Error generando reporte: {e}")
                vista.pausar()

        elif opcion == 6:
            try:
                reporte_jugador(controlador.usuarios, controlador.partidas, controlador.sudokus, "reporte_jugadores.html")
                vista.mostrar_resultado("Reporte generado: reporte_jugadores.html")
            except Exception as e:
                vista.mostrar_resultado(f"Error generando reporte: {e}")
                vista.pausar()

        elif opcion == 7:
            try:
                reporte_top10(controlador.partidas, controlador.usuarios, controlador.sudokus, "reporte_top10.html")
                vista.mostrar_resultado("Reporte generado: reporte_top10.html")
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