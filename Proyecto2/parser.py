try:
	from lexer import Lexer
except ImportError:
	from .lexer import Lexer


class ErrorSintactico(Exception):
	"""Indica que la secuencia de tokens no cumple la gramática."""


class Parser:
	BLOQUES = {
		"NUMERAL",
		"VIÑETA",
		"CITA",
		"CERCA_CODIGO",
		"REGLA_HORIZONTAL",
		"SALTO_PARRAFO",
		"INDENT",
		"DEDENT",
		"EOF",
	}

	def __init__(self, tokens):
		self.tokens = tokens
		self.posicion = 0

	@property
	def actual(self):
		return self.tokens[self.posicion]

	def mirar(self, tipo):
		return self.actual().tipo == tipo

	def avanzar(self):
		token = self.actual()
		if token.tipo != "EOF":
			self.posicion += 1
		return token

	def esperar(self, tipo):
		if not self.mirar(tipo):
			token = self.actual()
			raise ErrorSintactico(
				f"Línea {token.linea}, columna {token.columna}: "
				f"se esperaba {tipo}, se encontró {token.tipo} "
				f"({token.lexema!r})"
			)
		return self.avanzar()

	def analizar(self):
		documento = self.documento()
		self.esperar("EOF")
		return documento

	def documento(self):
		hijos = []
		while not self.mirar("EOF"):
			if self.mirar("SALTO_PARRAFO"):
				self.avanzar()
				continue
			if self.mirar("DEDENT"):
				break
			hijos.append(self.bloque())
		return {"tipo": "DOCUMENTO", "hijos": hijos}

	def bloque(self):
		if self.mirar("NUMERAL"):
			return self.encabezado()
		if self.mirar("VIÑETA"):
			return self.lista()
		if self.mirar("CITA"):
			return self.cita()
		if self.mirar("CERCA_CODIGO"):
			return self.bloque_codigo()
		if self.mirar("REGLA_HORIZONTAL"):
			return self.regla_horizontal()
		if self.mirar("INDENT"):
			token = self.actual()
			raise ErrorSintactico(
				f"Línea {token.linea}, columna {token.columna}: "
				"indentación sin una viñeta asociada"
			)
		return self.parrafo()

	def encabezado(self):
		numeral = self.esperar("NUMERAL")
		contenido = self.contenido_bloque()
		if not contenido:
			raise ErrorSintactico(
				f"Línea {numeral.linea}, columna {numeral.columna}: "
				"el encabezado necesita contenido"
			)
		return {
			"tipo": "ENCABEZADO",
			"nivel": len(numeral.lexema),
			"contenido": contenido,
		}

	def parrafo(self):
		contenido = self.contenido_bloque()
		if not contenido:
			token = self.actual()
			raise ErrorSintactico(
				f"Línea {token.linea}, columna {token.columna}: "
				f"token inesperado {token.tipo}"
			)
		return {"tipo": "PARRAFO", "contenido": contenido}

	def cita(self):
		marcador = self.esperar("CITA")
		contenido = self.contenido_bloque()
		return {
			"tipo": "CITA",
			"nivel": len(marcador.lexema),
			"contenido": contenido,
		}

	def regla_horizontal(self):
		token = self.esperar("REGLA_HORIZONTAL")
		return {"tipo": "REGLA_HORIZONTAL", "lexema": token.lexema}

	def bloque_codigo(self):
		apertura = self.esperar("CERCA_CODIGO")
		contenido = ""
		if self.mirar("TEXTO"):
			contenido = self.avanzar().lexema
		self.esperar("CERCA_CODIGO")
		return {
			"tipo": "BLOQUE_CODIGO",
			"delimitador": apertura.lexema,
			"contenido": contenido,
		}

	def lista(self):
		elementos = []
		while self.mirar("VIÑETA"):
			self.avanzar()
			contenido = self.contenido_bloque()
			if not contenido:
				token = self.actual()
				raise ErrorSintactico(
					f"Línea {token.linea}, columna {token.columna}: "
					"la viñeta necesita contenido"
				)

			item = {"tipo": "ITEM", "contenido": contenido}
			if self.mirar("INDENT"):
				self.avanzar()
				item["hijos"] = self.lista()
				if self.mirar("DEDENT"):
					self.avanzar()
			elementos.append(item)

		if self.mirar("DEDENT"):
			self.avanzar()
		return {"tipo": "LISTA", "elementos": elementos}

	def contenido_bloque(self):
		contenido = []
		while self.actual().tipo not in self.BLOQUES:
			contenido.append(self.elemento_inline())
		return contenido

	def elemento_inline(self):
		if self.mirar("TEXTO"):
			token = self.avanzar()
			return {"tipo": "TEXTO", "valor": token.lexema}
		if self.mirar("NEGRITA"):
			return self.enfasis("NEGRITA", "NEGRITA")
		if self.mirar("CURSIVA"):
			return self.enfasis("CURSIVA", "CURSIVA")
		if self.mirar("CODIGO_INLINE"):
			return self.enfasis("CODIGO_INLINE", "CODIGO_INLINE")
		token = self.actual()
		raise ErrorSintactico(
			f"Línea {token.linea}, columna {token.columna}: "
			f"token inline inesperado {token.tipo}"
		)

	def enfasis(self, tipo_apertura, tipo_cierre):
		apertura = self.esperar(tipo_apertura)
		contenido = []
		while not self.mirar(tipo_cierre):
			if self.mirar("EOF") or self.actual().tipo in self.BLOQUES:
				raise ErrorSintactico(
					f"Línea {apertura.linea}, columna {apertura.columna}: "
					f"falta el cierre {tipo_cierre}"
				)
			contenido.append(self.elemento_inline())
		self.esperar(tipo_cierre)
		return {"tipo": tipo_apertura, "contenido": contenido}


def analizar_texto(texto):
	lexer = Lexer(texto)
	tokens = lexer.analizar()
	if lexer.errores:
		raise ErrorSintactico("Se encontraron errores léxicos antes del parser")
	return Parser(tokens).analizar()
