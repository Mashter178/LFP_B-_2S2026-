import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from app import Aplicacion
from reportes import GeneradorReportes


class VentanaHorario(tk.Tk):
    Directorio = Path(__file__).resolve().parent.parent / "test"

    def __init__(self, ruta_archivo=None):
        super().__init__()
        self.title("HorarioScript")
        self.geometry("1060x680")
        self.minsize(820, 520)

        self.aplicacion = Aplicacion()
        self.ruta_seleccionada = Path(ruta_archivo) if ruta_archivo else None
        self.estado = tk.StringVar(value="Seleccione un archivo .hor para comenzar.")
        self.archivo = tk.StringVar(
            value=str(self.ruta_seleccionada)
            if self.ruta_seleccionada
            else "Ningún archivo seleccionado"
        )
        self.tablas = {}
        self.salida_resumen = None

        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = ttk.Frame(self, padding=16)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        ttk.Label(
            contenedor,
            text="Analizador HorarioScript",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")

        barra = ttk.Frame(contenedor)
        barra.grid(row=1, column=0, sticky="ew", pady=(14, 10))
        barra.columnconfigure(1, weight=1)

        ttk.Label(barra, text="Archivo:").grid(row=0, column=0, padx=(0, 8))
        ttk.Label(barra, textvariable=self.archivo).grid(
            row=0, column=1, sticky="w"
        )
        ttk.Button(
            barra,
            text="Seleccionar .hor",
            command=self.seleccionar_archivo,
        ).grid(row=0, column=2, padx=(8, 0))
        ttk.Button(
            barra,
            text="Analizar",
            command=self.analizar_archivo,
        ).grid(row=0, column=3, padx=(8, 0))
        ttk.Button(
            barra,
            text="Generar HTML",
            command=self.generar_html,
        ).grid(row=0, column=4, padx=(8, 0))

        ttk.Label(contenedor, textvariable=self.estado).grid(
            row=2, column=0, sticky="w", pady=(0, 8)
        )

        self.pestanas = ttk.Notebook(contenedor)
        self.pestanas.grid(row=3, column=0, sticky="nsew")
        contenedor.rowconfigure(3, weight=1)

        self.crear_pestana_texto("Resumen")
        self.crear_pestana_tabla("Tokens", "tokens", ["N.º", "Lexema", "Tipo", "Línea", "Columna"])
        self.crear_pestana_tabla("Errores léxicos", "errores", ["N.º", "Lexema", "Tipo", "Descripción", "Línea", "Columna"])
        self.crear_pestana_tabla("Cursos", "cursos", ["Nombre", "Código", "Créditos"])
        self.crear_pestana_tabla("Catedráticos", "catedraticos", ["Nombre", "Código", "Categoría"])
        self.crear_pestana_tabla("Aulas", "aulas", ["Aula", "Capacidad", "Edificio"])
        self.crear_pestana_tabla("Clases", "clases", ["Curso", "Catedrático", "Aula", "Día", "Inicio", "Fin", "Sección"])
        self.crear_pestana_texto("Estadísticas")

    def crear_pestana_texto(self, nombre):
        marco = ttk.Frame(self.pestanas, padding=8)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        salida = tk.Text(marco, wrap="word", state="disabled", font=("Consolas", 10))
        salida.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(marco, orient="vertical", command=salida.yview)
        barra.grid(row=0, column=1, sticky="ns")
        salida.configure(yscrollcommand=barra.set)
        self.pestanas.add(marco, text=nombre)
        self.tablas[nombre] = salida
        if nombre == "Resumen":
            self.salida_resumen = salida

    def crear_pestana_tabla(self, nombre, clave, columnas):
        marco = ttk.Frame(self.pestanas, padding=8)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        for columna in columnas:
            tabla.heading(columna, text=columna)
            tabla.column(columna, width=130, minwidth=80, anchor="w")
        tabla.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        barra.grid(row=0, column=1, sticky="ns")
        tabla.configure(yscrollcommand=barra.set)
        self.pestanas.add(marco, text=nombre)
        self.tablas[clave] = tabla

    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo HorarioScript",
            initialdir=str(self.Directorio),
            filetypes=[("Archivos HorarioScript", "*.hor"), ("Todos", "*.*")],
        )
        if ruta:
            self.ruta_seleccionada = Path(ruta)
            self.archivo.set(str(self.ruta_seleccionada))
            self.estado.set("Archivo seleccionado. Presione Analizar.")

    def analizar_archivo(self):
        if not self.ruta_seleccionada:
            messagebox.showwarning(
                "Archivo requerido",
                "Seleccione un archivo .hor antes de analizar.",
            )
            return

        ruta = self.ruta_seleccionada
        try:
            self.aplicacion = Aplicacion(ruta)
            self.aplicacion.ejecutar()
        except OSError as error:
            messagebox.showerror("No se pudo leer el archivo", str(error))
            return
        self.mostrar_resultado()

    def mostrar_resultado(self):
        errores_lexicos = self.aplicacion.errores_lexicos
        error_sintactico = self.aplicacion.error_sintactico
        errores_semanticos = self.aplicacion.errores_semanticos

        if errores_lexicos:
            self.estado.set("El análisis terminó con errores léxicos.")
        elif error_sintactico:
            self.estado.set("El análisis terminó con un error sintáctico.")
        elif errores_semanticos:
            self.estado.set("El análisis terminó con errores semánticos.")
        else:
            self.estado.set("Análisis léxico, sintáctico y semántico correcto.")

        self.cargar_tokens()
        self.cargar_errores()
        if self.aplicacion.horario:
            self.cargar_datos()
        self.mostrar_resumen()

    def limpiar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def cargar_tokens(self):
        tabla = self.tablas["tokens"]
        self.limpiar_tabla(tabla)
        for token in self.aplicacion.tokens:
            tabla.insert("", "end", values=(token.numero, token.lexema, token.tipo, token.linea, token.columna))

    def cargar_errores(self):
        tabla = self.tablas["errores"]
        self.limpiar_tabla(tabla)
        for error in self.aplicacion.errores_lexicos:
            tabla.insert("", "end", values=(error.numero, error.lexema, error.tipo, error.descripcion, error.linea, error.columna))

    def cargar_datos(self):
        horario = self.aplicacion.horario
        datos = self.aplicacion.datos_reportes["clasificacion"]
        for clave, filas in (
            ("cursos", horario["cursos"]),
            ("catedraticos", horario["catedraticos"]),
            ("aulas", horario["aulas"]),
            ("clases", datos["clases"]),
        ):
            tabla = self.tablas[clave]
            self.limpiar_tabla(tabla)
            for fila in filas:
                valores = self.valores_fila(clave, fila)
                tabla.insert("", "end", values=valores)

    def valores_fila(self, clave, fila):
        limpiar = lambda valor: str(valor).strip('"')
        if clave == "cursos":
            return (limpiar(fila["nombre"]), limpiar(fila["codigo"]), fila["creditos"])
        if clave == "catedraticos":
            return (limpiar(fila["nombre"]), limpiar(fila["codigo"]), fila["categoria"])
        if clave == "aulas":
            return (limpiar(fila["nombre"]), fila["capacidad"], limpiar(fila["edificio"]))
        return tuple(limpiar(fila[campo]) for campo in ("curso", "catedratico", "aula", "dia", "inicio", "fin", "seccion"))

    def mostrar_resumen(self):
        lineas = [
            f"Archivo: {self.aplicacion.ruta_archivo}",
            f"Tokens reconocidos: {len(self.aplicacion.tokens)}",
            f"Errores léxicos: {len(self.aplicacion.errores_lexicos)}",
            f"Error sintáctico: {'sí' if self.aplicacion.error_sintactico else 'no'}",
            f"Errores semánticos: {len(self.aplicacion.errores_semanticos)}",
        ]
        if self.aplicacion.datos_reportes:
            estadisticas = self.aplicacion.datos_reportes["estadisticas"]
            lineas.extend([
                "", "ESTADÍSTICAS",
                f"Cursos: {estadisticas['total_cursos']}",
                f"Catedráticos: {estadisticas['total_catedraticos']}",
                f"Aulas: {estadisticas['total_aulas']}",
                f"Clases: {estadisticas['total_clases']}",
                f"Minutos programados: {estadisticas['minutos_totales']}",
            ])
        errores = list(self.aplicacion.errores_lexicos) + list(self.aplicacion.errores_semanticos)
        if self.aplicacion.error_sintactico:
            errores.append(self.aplicacion.error_sintactico)
        if errores:
            lineas.extend(["", "ERRORES"])
            lineas.extend(f"- {error}" for error in errores)
        self.escribir_texto(self.salida_resumen, "\n".join(lineas))
        if self.aplicacion.datos_reportes:
            estadisticas = self.aplicacion.datos_reportes["estadisticas"]
            datos = "\n".join(f"{clave}: {valor}" for clave, valor in estadisticas.items())
            self.escribir_texto(self.tablas["Estadísticas"], datos)

    def escribir_texto(self, widget, texto):
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", texto)
        widget.configure(state="disabled")

    def generar_html(self):
        if not self.aplicacion.datos_reportes:
            messagebox.showwarning("Sin datos", "Analice un archivo válido antes de generar HTML.")
            return
        archivos = GeneradorReportes(self.aplicacion.datos_reportes).generar_todos()
        nombres = "\n".join(str(archivo) for archivo in archivos)
        messagebox.showinfo("Reportes generados", f"Se generaron estos archivos:\n\n{nombres}")


def main():
    ventana = VentanaHorario()
    ventana.mainloop()


if __name__ == "__main__":
    main()
