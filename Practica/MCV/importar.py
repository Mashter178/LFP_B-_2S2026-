from pathlib import Path
from modelo import Sudoku, Usuario, Partida
from validar import calificar_intento


class Controlador:
    def __init__(self):
        self.sudokus = []
        self.usuarios = []
        self.partidas = []

    def cargar_sudokus(self, ruta):
        sudokus = []
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                id_sudoku, dificultad, tablero = [x.strip() for x in linea.split(",")]
                sudokus.append(Sudoku(id_sudoku, dificultad, tablero))
        return sudokus

    def cargar_usuarios(self, ruta):
        usuarios = []
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                carnet, nombre, apellido, nivel = [x.strip() for x in linea.split(",")]
                usuarios.append(Usuario(carnet, nombre, apellido, nivel))
        return usuarios

    def cargar_partidas(self, ruta, sudokus=None):
        partidas = []
        registros = self._leer_registros_multilinea(ruta, 5)

        for carnet, id_sudoku, solucion, tiempo_segundos, fecha in registros:
            partida = Partida(
                carnet.strip(),
                id_sudoku.strip(),
                solucion.strip(),
                int(tiempo_segundos.strip()),
                fecha.strip(),
            )

            if sudokus is not None:
                sudoku = next(
                    (s for s in sudokus if s.id_sudoku == partida.id_sudoku), None
                )
                if sudoku:
                    resultado = calificar_intento(sudoku.tablero, partida.solucion)
                    partida.porcentaje_validez = resultado["porcentaje_validez"]
                    partida.resuelto_correctamente = resultado["resuelto_correctamente"]

            partidas.append(partida)

        return partidas