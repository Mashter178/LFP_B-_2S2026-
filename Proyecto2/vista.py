import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
    from controlador import ControladorMarkdown
except ImportError:
    from .controlador import ControladorMarkdown


class VentanaMarkdown(tk.Tk):
    def __init__(self, ruta_inicial=None):
        super().__init__()
        self.title("Analizador Markdown")
        self.geometry("760x520")
        self.minsize(620, 420)

        self.controlador = ControladorMarkdown()
        self.ruta = Path(ruta_inicial) if ruta_inicial else None
        self.archivo = tk.StringVar(
            value=str(self.ruta) if self.ruta else "Ningún archivo seleccionado"
        )
        self.estado = tk.StringVar(value="Seleccione un archivo Markdown.")

        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = ttk.Frame(self, padding=12)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(3, weight=1)

        ttk.Label(
            contenedor,
            text="Analizador Markdown",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        barra = ttk.Frame(contenedor)
        barra.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        barra.columnconfigure(1, weight=1)
        ttk.Label(barra, text="Archivo:").grid(row=0, column=0, padx=(0, 8))
        ttk.Label(barra, textvariable=self.archivo).grid(
            row=0, column=1, sticky="ew"
        )
        ttk.Button(
            barra,
            text="Seleccionar",
            command=self.seleccionar_archivo,
        ).grid(row=0, column=2, padx=(8, 0))

        acciones = ttk.Frame(contenedor)
        acciones.grid(row=2, column=0, sticky="w", pady=(0, 8))
        ttk.Button(
            acciones,
            text="Analizar",
            command=self.analizar_archivo,
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            acciones,
            text="Generar HTML",
            command=self.generar_html,
        ).pack(side="left")

        ttk.Label(contenedor, textvariable=self.estado).grid(
            row=3, column=0, sticky="nw", pady=(0, 8)
        )

        self.salida = tk.Text(contenedor, wrap="word", state="disabled")
        self.salida.grid(row=4, column=0, sticky="nsew")
        contenedor.rowconfigure(4, weight=1)

    def seleccionar_archivo(self):
        directorio_test = Path(__file__).resolve().parent / "test"
        ruta = filedialog.askopenfilename(
            title="Seleccionar Markdown",
            initialdir=str(self.ruta.parent if self.ruta else directorio_test),
            filetypes=[("Markdown", "*.md"), ("Todos los archivos", "*.*")],
        )
        if ruta:
            self.ruta = Path(ruta)
            self.archivo.set(str(self.ruta))
            self.estado.set("Archivo seleccionado. Presione Analizar.")

    def analizar_archivo(self):
        if self.ruta is None:
            messagebox.showwarning("Archivo requerido", "Seleccione un archivo .md.")
            return

        try:
            resultado = self.controlador.analizar_archivo(self.ruta)
        except OSError as error:
            messagebox.showerror("No se pudo leer el archivo", str(error))
            return

        self.mostrar_resultado(resultado)

    def mostrar_resultado(self, resultado):
        if resultado["errores_lexicos"]:
            self.estado.set("El análisis terminó con errores léxicos.")
        elif resultado["error_sintactico"]:
            self.estado.set("El análisis terminó con un error sintáctico.")
        elif resultado["errores_semanticos"]:
            self.estado.set("El análisis terminó con errores semánticos.")
        else:
            self.estado.set("Análisis correcto.")

        lineas = [
            f"Tokens: {len(resultado['tokens'])}",
            "",
            "ESTADÍSTICAS",
        ]
        for nombre, valor in resultado["estadisticas"].items():
            lineas.append(f"{nombre}: {valor}")

        errores = resultado["errores_lexicos"][:]
        if resultado["error_sintactico"]:
            errores.append(resultado["error_sintactico"])
        errores.extend(resultado["errores_semanticos"])
        if errores:
            lineas.extend(["", "ERRORES"])
            lineas.extend(f"- {error}" for error in errores)
        if resultado["advertencias"]:
            lineas.extend(["", "ADVERTENCIAS"])
            lineas.extend(f"- {advertencia}" for advertencia in resultado["advertencias"])

        self.escribir_salida("\n".join(lineas))

    def escribir_salida(self, texto):
        self.salida.configure(state="normal")
        self.salida.delete("1.0", tk.END)
        self.salida.insert("1.0", texto)
        self.salida.configure(state="disabled")

    def generar_html(self):
        if self.controlador.arbol is None:
            messagebox.showwarning("Análisis requerido", "Analice un archivo antes de generar HTML.")
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar HTML",
            defaultextension=".html",
            filetypes=[("HTML", "*.html")],
        )
        if not ruta:
            return

        try:
            self.controlador.guardar_html(ruta, self.ruta.stem if self.ruta else "Documento Markdown")
        except OSError as error:
            messagebox.showerror("No se pudo guardar el HTML", str(error))
            return
        messagebox.showinfo("HTML generado", f"Archivo guardado en:\n{ruta}")


if __name__ == "__main__":
    VentanaMarkdown().mainloop()
