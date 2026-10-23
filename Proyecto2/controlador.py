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
    def generar(self, arbol, titulo="Documento Markdown"):
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

    def render_bloque(self, nodo):
        tipo = nodo["tipo"]
        if tipo == "ENCABEZADO":
            nivel = nodo["nivel"]
            return f"<h{nivel}>{self.render_contenido(nodo['contenido'])}</h{nivel}>"
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


class ControladorMarkdown:
    def __init__(self):
        self.lexer = None
        self.tokens = []
        self.arbol = None
        self.errores_lexicos = []
        self.error_sintactico = None
        self.errores_semanticos = []
        self.advertencias = []

    def analizar_texto(self, texto):
        self.lexer = Lexer(texto)
        self.tokens = self.lexer.analizar()
        self.errores_lexicos = self.lexer.errores

        if self.errores_lexicos:
            return self.resultado()

        try:
            self.arbol = Parser(self.tokens).analizar()
        except ErrorSintactico as error:
            self.error_sintactico = error
            return self.resultado()

        if AnalizadorSemantico is None:
            self.advertencias.append(
                "semantic.py no está disponible; se omitió el análisis semántico."
            )
        else:
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
        for clave in ("hijos", "contenido", "elementos"):
            valor = nodo.get(clave)
            if isinstance(valor, list):
                for hijo in valor:
                    self.contar_nodos(hijo, estadisticas)
            elif isinstance(valor, dict):
                self.contar_nodos(valor, estadisticas)

    def generar_html(self, titulo="Documento Markdown"):
        if self.arbol is None:
            raise ValueError("No hay un AST válido para generar HTML.")
        return GeneradorHTML().generar(self.arbol, titulo)

    def guardar_html(self, ruta_salida, titulo="Documento Markdown"):
        Path(ruta_salida).write_text(
            self.generar_html(titulo), encoding="utf-8"
        )

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
