import argparse
from pathlib import Path

from Lexer import AnalizadorLexico
from controlador import ControladorHorario
from semantic import AnalizadorSemantico
from sintatic import ErrorSintactico, Parser


class Aplicacion:
    def __init__(self, ruta_archivo=None):
        self.ruta_archivo = ruta_archivo
        self.lexer = None
        self.tokens = []
        self.horario = None
        self.errores_lexicos = []
        self.error_sintactico = None
        self.errores_semanticos = []
        self.controlador = None
        self.datos_reportes = None

    def ejecutar(self, ruta_archivo=None):
        ruta = Path(ruta_archivo or self.ruta_archivo or self.ruta_predeterminada())
        self.ruta_archivo = ruta
        texto = ruta.read_text(encoding="utf-8")

        self.lexer = AnalizadorLexico(texto)
        self.tokens = self.lexer.analizar()
        self.errores_lexicos = self.lexer.errores

        if self.errores_lexicos:
            return self.resultado()

        try:
            self.horario = Parser(self.tokens).analizar()
        except ErrorSintactico as error:
            self.error_sintactico = error
            return self.resultado()

        analizador_semantico = AnalizadorSemantico(self.horario)
        self.errores_semanticos = analizador_semantico.analizar()
        self.controlador = ControladorHorario(self.horario)
        self.datos_reportes = self.controlador.datos_para_reportes()
        return self.resultado()

    def resultado(self):
        return {
            "ruta": self.ruta_archivo,
            "tokens": self.tokens,
            "horario": self.horario,
            "errores_lexicos": self.errores_lexicos,
            "error_sintactico": self.error_sintactico,
            "errores_semanticos": self.errores_semanticos,
            "datos_reportes": self.datos_reportes,
        }

    def esta_correcto(self):
        return not (
            self.errores_lexicos
            or self.error_sintactico
            or self.errores_semanticos
        )

    @staticmethod
    def ruta_predeterminada():
        return Path(__file__).resolve().parent.parent / "test" / "prueba.hor"

    def imprimir_resultado(self):
        print(f"Archivo: {self.ruta_archivo}")
        print(f"Tokens: {len(self.tokens)}")
        print(f"Errores léxicos: {len(self.errores_lexicos)}")

        if self.errores_lexicos:
            for error in self.errores_lexicos:
                print(f"- {error}")
            return

        if self.error_sintactico:
            print(f"Error sintáctico: {self.error_sintactico}")
            return

        print("Análisis sintáctico: correcto")
        print(f"Errores semánticos: {len(self.errores_semanticos)}")
        for error in self.errores_semanticos:
            print(f"- {error}")

        if self.esta_correcto():
            print("Análisis léxico, sintáctico y semántico correcto.")


def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta HorarioScript mediante la interfaz o la consola."
    )
    parser.add_argument(
        "archivo",
        nargs="?",
        help="Ruta opcional del archivo .hor.",
    )
    parser.add_argument(
        "--consola",
        action="store_true",
        help="Ejecuta el análisis sin abrir Tkinter.",
    )
    argumentos = parser.parse_args()

    if not argumentos.consola:
        from vista import VentanaHorario

        ventana = VentanaHorario(argumentos.archivo)
        ventana.mainloop()
        return 0

    aplicacion = Aplicacion(argumentos.archivo)
    try:
        aplicacion.ejecutar()
        aplicacion.imprimir_resultado()
    except OSError as error:
        print(f"No se pudo leer el archivo: {error}")
        return 1

    return 0 if aplicacion.esta_correcto() else 1


if __name__ == "__main__":
    raise SystemExit(main())
