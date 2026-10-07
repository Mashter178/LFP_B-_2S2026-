class ErrorSemantico:
	def __init__(self, mensaje):
		self.mensaje = mensaje

	def __str__(self):
		return self.mensaje


class AnalizadorSemantico:

	TIPOS_INLINE = {"TEXTO", "NEGRITA", "CURSIVA", "CODIGO_INLINE"}

	def __init__(self, arbol):
		self.arbol = arbol
		self.errores = []

	def error(self, mensaje):
		self.errores.append(ErrorSemantico(mensaje))

	def analizar(self):
		if not isinstance(self.arbol, dict):
			self.error("El parser debe ser un diccionario.")
			return self.errores

		self.validar_documento(self.arbol)
		return self.errores

	def validar_documento(self, nodo):
		self.requerir_tipo(nodo, "DOCUMENTO")
		hijos = self.lista_requerida(nodo, "hijos", "DOCUMENTO")
		for hijo in hijos:
			self.validar_bloque(hijo)

	def validar_bloque(self, nodo):
		if not isinstance(nodo, dict):
			self.error("Cada bloque debe ser un diccionario.")
			return

		tipo = nodo.get("tipo")
		validadores = {
			"ENCABEZADO": self.validar_encabezado,
			"PARRAFO": self.validar_parrafo,
			"LISTA": self.validar_lista,
			"CITA": self.validar_cita,
			"BLOQUE_CODIGO": self.validar_bloque_codigo,
			"REGLA_HORIZONTAL": self.validar_regla_horizontal,
		}
		validador = validadores.get(tipo)
		if validador is None:
			self.error(f"Tipo de bloque desconocido: {tipo!r}.")
			return
		validador(nodo)

	def validar_encabezado(self, nodo):
		nivel = nodo.get("nivel")
		if not isinstance(nivel, int) or not 1 <= nivel <= 6:
			self.error("El nivel de un encabezado debe estar entre 1 y 6.")
		self.validar_contenido(nodo, "ENCABEZADO")

	def validar_parrafo(self, nodo):
		self.validar_contenido(nodo, "PARRAFO")

	def validar_cita(self, nodo):
		nivel = nodo.get("nivel")
		if not isinstance(nivel, int) or nivel < 1:
			self.error("El nivel de una cita debe ser mayor que cero.")
		self.validar_contenido(nodo, "CITA")

	def validar_lista(self, nodo):
		elementos = self.lista_requerida(nodo, "elementos", "LISTA")
		if not elementos:
			self.error("Una lista debe tener un elemento.")
		for elemento in elementos:
			self.validar_item(elemento)

	def validar_item(self, nodo):
		if not isinstance(nodo, dict) or nodo.get("tipo") != "ITEM":
			self.error("Una lista solo puede contener nodos ITEM.")
			return
		self.validar_contenido(nodo, "ITEM")
		if "hijos" in nodo:
			if not isinstance(nodo["hijos"], dict):
				self.error("Los hijos de un ITEM deben formar una LISTA.")
			else:
				self.validar_lista(nodo["hijos"])

	def validar_bloque_codigo(self, nodo):
		contenido = nodo.get("contenido")
		if not isinstance(contenido, str):
			self.error("El contenido de un bloque de código debe ser texto.")
		if nodo.get("delimitador") != "```":
			self.error("El bloque de código debe usar el delimitador ```.")

	def validar_regla_horizontal(self, nodo):
		lexema = nodo.get("lexema")
		if not isinstance(lexema, str) or len(lexema.strip()) < 3:
			self.error("La regla horizontal debe tener al menos tres guiones.")
		elif set(lexema.strip()) != {"-"}:
			self.error("La regla horizontal solo puede contener guiones.")

	def validar_contenido(self, nodo, descripcion):
		contenido = self.lista_requerida(nodo, "contenido", descripcion)
		if not contenido:
			self.error(f"{descripcion} no puede tener contenido vacío.")
			return
		for elemento in contenido:
			self.validar_inline(elemento)

	def validar_inline(self, nodo):
		if not isinstance(nodo, dict):
			self.error("Cada elemento inline debe ser un diccionario.")
			return

		tipo = nodo.get("tipo")
		if tipo == "TEXTO":
			if not isinstance(nodo.get("valor"), str):
				self.error("El valor de TEXTO debe ser una cadena.")
			return

		if tipo in {"NEGRITA", "CURSIVA", "CODIGO_INLINE"}:
			contenido = self.lista_requerida(nodo, "contenido", tipo)
			if not contenido:
				self.error(f"{tipo} no puede estar vacío.")
			for elemento in contenido:
				if isinstance(elemento, dict) and elemento.get("tipo") in self.TIPOS_INLINE:
					self.validar_inline(elemento)
				else:
					self.error(f"Contenido inválido dentro de {tipo}.")
			return

		self.error(f"Tipo inline desconocido: {tipo!r}.")

	def requerir_tipo(self, nodo, tipo_esperado):
		if nodo.get("tipo") != tipo_esperado:
			self.error(
				f"Se esperaba un nodo {tipo_esperado}, "
				f"pero se recibió {nodo.get('tipo')!r}."
			)

	def lista_requerida(self, nodo, clave, descripcion):
		valor = nodo.get(clave)
		if not isinstance(valor, list):
			self.error(f"{descripcion} debe contener una lista en {clave!r}.")
			return []
		return valor


def analizar_arbol(arbol):
	"""Devuelve los errores semánticos encontrados en un AST."""
	return AnalizadorSemantico(arbol).analizar()
