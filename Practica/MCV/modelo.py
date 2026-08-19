class Sudoku:
    def __init__(self, id_sudoku, dificultad, tablero):
        self.id_sudoku = id_sudoku
        self.dificultad = dificultad
        self.tablero = tablero

class Usuario:
    def __init__(self, carnet, nombre, apellido, nivel):
        self.carnet = carnet
        self.nombre = nombre
        self.apellido = apellido
        self.nivel = nivel

class Partida:
    def __init__(self, carnet, id_sudoku, solucion, tiempo_segundos, fecha):
        self.carnet = carnet
        self.id_sudoku = id_sudoku
        self.solucion = solucion
        self.tiempo_segundos = tiempo_segundos
        self.fecha = fecha
        self.porcentaje_validez = 0
        self.resuelto_correctamente = False