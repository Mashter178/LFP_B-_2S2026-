import argparse
from pathlib import Path

try:
    from controlador import ControladorMarkdown
    from vista import VentanaMarkdown
except ImportError:
    from .controlador import ControladorMarkdown
    from .vista import VentanaMarkdown


def imprimir_resultado(resultado):
    print(f"Tokens: {len(resultado['tokens'])}")
    print("\nEstadísticas:")
    for nombre, valor in resultado["estadisticas"].items():
        print(f"  {nombre}: {valor}")

    errores = resultado["errores_lexicos"][:]
    if resultado["error_sintactico"]:
        errores.append(resultado["error_sintactico"])
    errores.extend(resultado["errores_semanticos"])

    if errores:
        print("\nErrores:")
        for error in errores:
            print(f"- {error}")
    else:
        print("\nAnálisis correcto.")

    for advertencia in resultado["advertencias"]:
        print(f"Advertencia: {advertencia}")


def ejecutar_consola(ruta, salida_html=None):
    controlador = ControladorMarkdown()
    resultado = controlador.analizar_archivo(ruta)
    imprimir_resultado(resultado)

    if salida_html and controlador.arbol is not None and controlador.esta_correcto():
        controlador.guardar_html(salida_html, Path(ruta).stem)
        print(f"\nHTML generado: {salida_html}")

    return 0 if controlador.esta_correcto() else 1


def main():
    parser = argparse.ArgumentParser(
        description="Analizador y renderizador de documentos Markdown."
    )
    parser.add_argument(
        "archivo",
        nargs="?",
        help="Archivo Markdown que se desea analizar.",
    )
    parser.add_argument(
        "--consola",
        action="store_true",
        help="Ejecuta el análisis sin abrir Tkinter.",
    )
    parser.add_argument(
        "--html",
        metavar="SALIDA",
        help="Guarda el HTML generado en la ruta indicada.",
    )
    argumentos = parser.parse_args()

    if argumentos.consola:
        if not argumentos.archivo:
            parser.error("--consola requiere un archivo Markdown.")
        try:
            return ejecutar_consola(argumentos.archivo, argumentos.html)
        except OSError as error:
            print(f"No se pudo leer el archivo: {error}")
            return 1

    VentanaMarkdown(argumentos.archivo).mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
