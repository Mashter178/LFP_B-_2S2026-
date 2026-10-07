class Token:
	def __init__(self, numero, tipo, lexema, linea, columna):
		self.numero = numero
		self.tipo = tipo
		self.lexema = lexema
		self.linea = linea
		self.columna = columna

	def __repr__(self):
		return (
			f"Token({self.numero}, {self.tipo!r}, {self.lexema!r}, "
			f"{self.linea}:{self.columna})"
		)


class ErrorLexico:
	def __init__(self, numero, lexema, tipo, descripcion, linea, columna):
		self.numero = numero
		self.lexema = lexema
		self.tipo = tipo
		self.descripcion = descripcion
		self.linea = linea
		self.columna = columna

	def __str__(self):
		return (
			f"Error {self.numero}: {self.tipo} - {self.descripcion} "
			f"({self.lexema!r}, línea {self.linea}, columna {self.columna})"
		)


class AnalizadorLexico:

	def __init__(self, texto):
		self.texto = texto
		self.posicion = 0
		self.linea = 1
		self.columna = 1
		self.numero_token = 0
		self.numero_error = 0
		self.tokens = []
		self.errores = []
		self.inicio_linea = True
		self.pila_indentacion = [0]
		self.tokens_pendientes = []
		self.en_bloque_codigo = False

	def actual(self):
		if self.posicion >= len(self.texto):
			return ""
		return self.texto[self.posicion]

	def siguiente(self, cantidad=1):
		posicion = self.posicion + cantidad
		if posicion >= len(self.texto):
			return ""
		return self.texto[posicion]

	def avanzar(self):
		caracter = self.actual()
		if caracter == "":
			return caracter
		self.posicion += 1
		if caracter == "\n":
			self.linea += 1
			self.columna = 1
			self.inicio_linea = True
		else:
			self.columna += 1
			self.inicio_linea = False
		return caracter

	def retroceder(self):
		if self.posicion == 0:
			return
		self.posicion -= 1
		caracter = self.texto[self.posicion]
		if caracter == "\n":
			self.linea -= 1
			ultimo_salto = self.texto.rfind("\n", 0, self.posicion)
			self.columna = self.posicion - ultimo_salto
		else:
			self.columna -= 1
		self.inicio_linea = (
			self.posicion == 0 or self.texto[self.posicion - 1] == "\n"
		)

	def agregar_token(self, tipo, lexema, linea=None, columna=None):
		self.numero_token += 1
		token = Token(
			self.numero_token,
			tipo,
			lexema,
			self.linea if linea is None else linea,
			self.columna if columna is None else columna,
		)
		self.tokens.append(token)
		return token

	def agregar_error(self, lexema, tipo, descripcion, linea, columna):
		self.numero_error += 1
		self.errores.append(
			ErrorLexico(
				self.numero_error, lexema, tipo, descripcion, linea, columna
			)
		)

	def consumir_espacios(self):
		cantidad = 0
		while self.actual() in " \t":
			cantidad += 2 if self.actual() == "\t" else 1
			self.avanzar()
		return cantidad

	def resto_linea(self):
		fin = self.texto.find("\n", self.posicion)
		return self.texto[self.posicion:] if fin == -1 else self.texto[self.posicion:fin]

	def es_regla_horizontal(self):
		contenido = self.resto_linea().strip()
		return len(contenido) >= 3 and set(contenido) == {"-"}

	def es_cerca_codigo(self):
		return self.texto[self.posicion:self.posicion + 3] == "```"

	def emitir_indentacion(self, nivel, linea, columna):
		actual = self.pila_indentacion[-1]
		if nivel > actual:
			self.pila_indentacion.append(nivel)
			self.tokens_pendientes.append(("INDENT", "", linea, columna))
		elif nivel < actual:
			while len(self.pila_indentacion) > 1 and nivel < self.pila_indentacion[-1]:
				self.pila_indentacion.pop()
				self.tokens_pendientes.append(("DEDENT", "", linea, columna))

	def consumir_texto(self):
		linea = self.linea
		columna = self.columna
		inicio = self.posicion
		while self.actual() not in "\n*`":
			self.avanzar()
		if self.posicion == inicio:
			self.avanzar()
		return self.agregar_token(
			"TEXTO", self.texto[inicio:self.posicion], linea, columna
		)

	def consumir_bloque_codigo(self):
		linea = self.linea
		columna = self.columna
		inicio = self.posicion
		while self.posicion < len(self.texto):
			if self.inicio_linea and self.es_cerca_codigo():
				break
			self.avanzar()
		if self.posicion == inicio:
			return None
		return self.agregar_token(
			"TEXTO", self.texto[inicio:self.posicion], linea, columna
		)

	def consumir_marcador_linea(self):
		linea = self.linea
		columna = self.columna
		inicio = self.posicion
		if self.actual() == "#":
			cantidad = 0
			while self.actual() == "#" and cantidad < 7:
				cantidad += 1
				self.avanzar()
			if cantidad <= 6 and self.actual() in " \t":
				return self.agregar_token("NUMERAL", "#" * cantidad, linea, columna)
			while self.posicion > inicio:
				self.retroceder()
		if self.actual() == ">":
			while self.actual() == ">":
				self.avanzar()
			lexema = self.texto[inicio:self.posicion]
			if self.actual() in " \t":
				return self.agregar_token("CITA", lexema, linea, columna)
			while self.posicion > inicio:
				self.retroceder()
		return None

	def preparar_inicio_linea(self):
		linea = self.linea
		columna = self.columna
		indentacion = self.consumir_espacios()
		if self.actual() == "\n":
			self.avanzar()
			return self.agregar_token("SALTO_PARRAFO", "", linea, columna)
		if self.actual() == "":
			return None
		if self.es_cerca_codigo():
			for _ in range(3):
				self.avanzar()
			self.en_bloque_codigo = not self.en_bloque_codigo
			return self.agregar_token("CERCA_CODIGO", "```", linea, columna + indentacion)
		if self.es_regla_horizontal():
			inicio = self.posicion
			while self.actual() not in ("", "\n"):
				self.avanzar()
			return self.agregar_token(
				"REGLA_HORIZONTAL", self.texto[inicio:self.posicion], linea, columna
			)
		if self.actual() in "-+*" and self.siguiente() in " \t":
			nivel = indentacion // 2
			self.emitir_indentacion(nivel, linea, columna)
			self.tokens_pendientes.append(
				("VIÑETA", self.avanzar(), linea, columna + indentacion)
			)
			return None
		return self.consumir_marcador_linea()

	def siguiente_token(self):
		if self.tokens_pendientes:
			tipo, lexema, linea, columna = self.tokens_pendientes.pop(0)
			return self.agregar_token(tipo, lexema, linea, columna)
		if self.en_bloque_codigo:
			if self.inicio_linea and self.es_cerca_codigo():
				linea = self.linea
				columna = self.columna
				for _ in range(3):
					self.avanzar()
				self.en_bloque_codigo = False
				return self.agregar_token("CERCA_CODIGO", "```", linea, columna)
			token = self.consumir_bloque_codigo()
			if token:
				return token
		if self.posicion >= len(self.texto):
			while len(self.pila_indentacion) > 1:
				self.pila_indentacion.pop()
				self.tokens_pendientes.append(("DEDENT", "", self.linea, self.columna))
			if self.tokens_pendientes:
				return self.siguiente_token()
			return self.agregar_token("EOF", "", self.linea, self.columna)
		if self.inicio_linea:
			token = self.preparar_inicio_linea()
			if token:
				return token
			if self.tokens_pendientes:
				return self.siguiente_token()
		if self.actual() == "\n":
			self.avanzar()
			return self.siguiente_token()
		linea = self.linea
		columna = self.columna
		if self.texto[self.posicion:self.posicion + 2] == "**":
			self.avanzar()
			self.avanzar()
			return self.agregar_token("NEGRITA", "**", linea, columna)
		if self.actual() == "`":
			self.avanzar()
			return self.agregar_token("CODIGO_INLINE", "`", linea, columna)
		if self.actual() == "*":
			self.avanzar()
			return self.agregar_token("CURSIVA", "*", linea, columna)
		return self.consumir_texto()

	def analizar(self):
		while True:
			token = self.siguiente_token()
			if token.tipo == "EOF":
				break
		return self.tokens


Lexer = AnalizadorLexico