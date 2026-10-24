from html import escape
from pathlib import Path

try:
    from lexer import Lexer
    from parser import ErrorSintactico, Parser
except ImportError:
    from .lexer import Lexer
    from .parser import ErrorSintactico, Parser

try:
    from semantic import AnalizadorSemantico
except ImportError:
    AnalizadorSemantico = None


class GeneradorHTML:
    def __init__(self):
        self.encabezados = []

    def generar(self, arbol, titulo="Documento Markdown"):
        self.encabezados = []
        contenido = "\n".join(self.render_bloque(nodo) for nodo in arbol["hijos"])
        return (
            "<!doctype html>\n"
            "<html lang=\"es\">\n"
            "<head>\n"
            "<meta charset=\"utf-8\">\n"
            f"<title>{escape(titulo)}</title>\n"
            "</head>\n"
            "<body>\n"
            f"{contenido}\n"
            "</body>\n"
            "</html>\n"
        )

    def generar_estadisticas(self, estadisticas, titulo="Estadísticas"):
        filas = "\n".join(
            f"<tr><th>{escape(str(nombre))}</th><td>{valor}</td></tr>"
            for nombre, valor in estadisticas.items()
        )
        return self.documento_base(
            titulo,
            f"<h1>{escape(titulo)}</h1>\n<table>\n{filas}\n</table>",
        )

    def generar_indice(self, titulo="Tabla de contenido"):
        if self.encabezados:
            elementos = "\n".join(
                f'<li class="nivel-{entrada["nivel"]}">'
                f'<a href="#{entrada["id"]}">{escape(entrada["texto"])}</a></li>'
                for entrada in self.encabezados
            )
        else:
            elementos = "<li>No se encontraron encabezados.</li>"
        return self.documento_base(
            titulo,
            f"<h1>{escape(titulo)}</h1>\n<ul>\n{elementos}\n</ul>",
        )

    @staticmethod
    def documento_base(titulo, contenido):
        return (
            "<!doctype html>\n"
            "<html lang=\"es\">\n"
            "<head>\n"
            "<meta charset=\"utf-8\">\n"
            f"<title>{escape(titulo)}</title>\n"
            "<style>body{font-family:Arial,sans-serif;margin:2rem}"
            "table{border-collapse:collapse}th,td{border:1px solid #999;"
            "padding:.4rem .7rem;text-align:left}.nivel-2{margin-left:1rem}"
            ".nivel-3{margin-left:2rem}.nivel-4{margin-left:3rem}</style>\n"
            "</head>\n"
            f"<body>\n{contenido}\n</body>\n</html>\n"
        )

    def generar_diagnostico(self, texto, errores, titulo="Documento Markdown"):
        lista_errores = "\n".join(
            f"<li>{escape(str(error))}</li>" for error in errores
        )
        return (
            "<!doctype html>\n"
            "<html lang=\"es\">\n"
            "<head>\n"
            "<meta charset=\"utf-8\">\n"
            f"<title>{escape(titulo)} - diagnóstico</title>\n"
            "</head>\n"
            "<body>\n"
            "<h1>Documento con errores</h1>\n"
            f"<ul>\n{lista_errores}\n</ul>\n"
            f"<pre>{escape(texto)}</pre>\n"
            "</body>\n"
            "</html>\n"
        )

    def render_bloque(self, nodo):
        tipo = nodo["tipo"]
        if tipo == "ENCABEZADO":
            nivel = nodo["nivel"]
            numero = len(self.encabezados) + 1
            identificador = f"encabezado-{numero}"
            self.encabezados.append({
                "id": identificador,
                "nivel": nivel,
                "texto": self.texto_contenido(nodo["contenido"]),
            })
            return (
                f'<h{nivel} id="{identificador}">'
                f"{self.render_contenido(nodo['contenido'])}</h{nivel}>"
            )
        if tipo == "PARRAFO":
            return f"<p>{self.render_contenido(nodo['contenido'])}</p>"
        if tipo == "LISTA":
            elementos = "\n".join(self.render_item(item) for item in nodo["elementos"])
            return f"<ul>\n{elementos}\n</ul>"
        if tipo == "CITA":
            return f"<blockquote>{self.render_contenido(nodo['contenido'])}</blockquote>"
        if tipo == "BLOQUE_CODIGO":
            return f"<pre><code>{escape(nodo['contenido'])}</code></pre>"
        if tipo == "REGLA_HORIZONTAL":
            return "<hr>"
        return ""

    def render_item(self, nodo):
        contenido = self.render_contenido(nodo["contenido"])
        hijos = ""
        if "hijos" in nodo:
            hijos = "\n" + self.render_bloque(nodo["hijos"])
        return f"<li>{contenido}{hijos}</li>"

    def render_contenido(self, contenido):
        return "".join(self.render_inline(nodo) for nodo in contenido)

    def render_inline(self, nodo):
        tipo = nodo["tipo"]
        if tipo == "TEXTO":
            return escape(nodo["valor"])
        if tipo == "NEGRITA":
            return f"<strong>{self.render_contenido(nodo['contenido'])}</strong>"
        if tipo == "CURSIVA":
            return f"<em>{self.render_contenido(nodo['contenido'])}</em>"
        if tipo == "CODIGO_INLINE":
            return f"<code>{self.render_contenido(nodo['contenido'])}</code>"
        return ""

    def texto_contenido(self, contenido):
        partes = []
        for nodo in contenido:
            if nodo["tipo"] == "TEXTO":
                partes.append(nodo["valor"])
            elif "contenido" in nodo:
                partes.append(self.texto_contenido(nodo["contenido"]))
        return "".join(partes).strip()


class ControladorMarkdown:
    def __init__(self):
        self.lexer = None
        self.tokens = []
        self.arbol = None
        self.errores_lexicos = []
        self.error_sintactico = None
        self.errores_semanticos = []
        self.advertencias = []
        self.texto = ""

    def analizar_texto(self, texto):
        self.texto = texto
        self.arbol = None
        self.error_sintactico = None
        self.errores_semanticos = []
        self.advertencias = []
        self.lexer = Lexer(texto)
        self.tokens = self.lexer.analizar()
        self.errores_lexicos = self.lexer.errores

        try:
            self.arbol = Parser(self.tokens).analizar()
        except ErrorSintactico as error:
            self.error_sintactico = error

        if self.arbol is not None and AnalizadorSemantico is None:
            self.advertencias.append(
                "semantic.py no está disponible; se omitió el análisis semántico."
            )
        elif self.arbol is not None:
            analizador = AnalizadorSemantico(self.arbol)
            self.errores_semanticos = analizador.analizar()
        return self.resultado()

    def analizar_archivo(self, ruta):
        ruta = Path(ruta)
        return self.analizar_texto(ruta.read_text(encoding="utf-8"))

    def estadisticas(self):
        estadisticas = {
            "caracteres": 0,
            "tokens": len(self.tokens),
            "bloques": 0,
            "palabras": 0,
            "encabezados": 0,
            "parrafos": 0,
            "listas": 0,
            "elementos_lista": 0,
            "citas": 0,
            "bloques_codigo": 0,
            "reglas_horizontales": 0,
            "negritas": 0,
            "cursivas": 0,
            "codigo_inline": 0,
        }
        if self.lexer is not None:
            estadisticas["caracteres"] = len(self.lexer.texto)
        if self.arbol is not None:
            self.contar_nodos(self.arbol, estadisticas)
        return estadisticas

    def contar_nodos(self, nodo, estadisticas):
        if not isinstance(nodo, dict):
            return
        tipo = nodo.get("tipo")
        tipos_bloque = {
            "ENCABEZADO",
            "PARRAFO",
            "LISTA",
            "CITA",
            "BLOQUE_CODIGO",
            "REGLA_HORIZONTAL",
        }
        if tipo in tipos_bloque:
            estadisticas["bloques"] += 1
        if tipo in estadisticas:
            estadisticas[tipo] += 1
        equivalencias = {
            "ENCABEZADO": "encabezados",
            "PARRAFO": "parrafos",
            "LISTA": "listas",
            "CITA": "citas",
            "BLOQUE_CODIGO": "bloques_codigo",
            "REGLA_HORIZONTAL": "reglas_horizontales",
            "NEGRITA": "negritas",
            "CURSIVA": "cursivas",
            "CODIGO_INLINE": "codigo_inline",
        }
        if tipo in equivalencias:
            estadisticas[equivalencias[tipo]] += 1
        if tipo == "ITEM":
            estadisticas["elementos_lista"] += 1
        if tipo == "TEXTO":
            estadisticas["palabras"] += len(nodo.get("valor", "").split())
        for clave in ("hijos", "contenido", "elementos"):
            valor = nodo.get(clave)
            if isinstance(valor, list):
                for hijo in valor:
                    self.contar_nodos(hijo, estadisticas)
            elif isinstance(valor, dict):
                self.contar_nodos(valor, estadisticas)

    def generar_html(self, titulo="Documento Markdown"):
        generador = GeneradorHTML()
        if self.arbol is not None:
            return generador.generar(self.arbol, titulo)
        errores = list(self.errores_lexicos)
        if self.error_sintactico:
            errores.append(self.error_sintactico)
        errores.extend(self.errores_semanticos)
        return generador.generar_diagnostico(self.texto, errores, titulo)

    def guardar_html(self, ruta_salida, titulo="Documento Markdown"):
        Path(ruta_salida).write_text(
            self.generar_html(titulo), encoding="utf-8"
        )

    def guardar_reportes(self, directorio, titulo="Documento Markdown"):
        directorio = Path(directorio)
        directorio.mkdir(parents=True, exist_ok=True)
        generador = GeneradorHTML()
        if self.arbol is not None:
            documento = generador.generar(self.arbol, titulo)
        else:
            documento = self.generar_html(titulo)
        estadisticas = generador.generar_estadisticas(
            self.estadisticas(), "Estadísticas del documento"
        )
        indice = generador.generar_indice("Tabla de contenido")
        rutas = {
            "documento": directorio / "documento_renderizado.html",
            "estadisticas": directorio / "estadisticas.html",
            "indice": directorio / "tabla_contenido.html",
        }
        rutas["documento"].write_text(documento, encoding="utf-8")
        rutas["estadisticas"].write_text(estadisticas, encoding="utf-8")
        rutas["indice"].write_text(indice, encoding="utf-8")
        return rutas

    def resultado(self):
        return {
            "tokens": self.tokens,
            "arbol": self.arbol,
            "errores_lexicos": self.errores_lexicos,
            "error_sintactico": self.error_sintactico,
            "errores_semanticos": self.errores_semanticos,
            "advertencias": self.advertencias,
            "estadisticas": self.estadisticas(),
        }

    def esta_correcto(self):
        return not (
            self.errores_lexicos
            or self.error_sintactico
            or self.errores_semanticos
        )
