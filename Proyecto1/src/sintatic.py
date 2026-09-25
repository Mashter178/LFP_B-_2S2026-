from pathlib import Path

from Lexer import Lexer


class ErrorSintactico(Exception):
	"""Indica que los tokens no cumplen la gramática del lenguaje."""


class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.posicion = 0

	@property
	def actual(self):
		return self.tokens[self.posicion]

	def avanzar(self):
		token = self.actual
		if token.tipo != "EOF":
			self.posicion += 1
		return token

	def esperar(self, tipo, lexema=None):
		token = self.actual
		coincide_tipo = token.tipo == tipo
		coincide_lexema = lexema is None or token.lexema == lexema

		if not coincide_tipo or not coincide_lexema:
			esperado = tipo if lexema is None else f"{tipo}({lexema!r})"
			encontrado = f"{token.tipo}({token.lexema!r})"
			raise ErrorSintactico(
				f"Línea {token.linea}, columna {token.columna}: "
				f"se esperaba {esperado}, se encontró {encontrado}"
			)

		return self.avanzar()

	def analizar(self):
		horario = self.horario()
		self.esperar("EOF")
		return horario

	def horario(self):
		self.esperar("PALABRA_RESERVADA", "HORARIO")
		self.esperar("LLAVE_ABRE")

		resultado = {
			"cursos": self.cursos(),
			"catedraticos": self.catedraticos(),
			"aulas": self.aulas(),
			"clases": self.clases(),
		}

		self.esperar("LLAVE_CIERRA")
		self.esperar("PUNTO_COMA")
		return resultado

	def inicio_seccion(self, nombre):
		self.esperar("PALABRA_RESERVADA", nombre)
		self.esperar("LLAVE_ABRE")

	def fin_seccion(self):
		self.esperar("LLAVE_CIERRA")
		self.esperar("PUNTO_COMA")

	def cursos(self):
		self.inicio_seccion("CURSOS")
		cursos = []

		while self.actual.lexema != "}":
			self.esperar("PALABRA_RESERVADA", "curso")
			self.esperar("DOS_PUNTOS")
			nombre = self.esperar("CADENA").lexema
			self.esperar("CORCHETE_ABRE")
			codigo = self.campo_codigo("codigo")
			self.esperar("COMA")
			creditos = self.campo_entero("creditos")
			self.esperar("CORCHETE_CIERRA")
			self.esperar("COMA")
			cursos.append({"nombre": nombre, "codigo": codigo, "creditos": creditos})

		self.fin_seccion()
		return cursos

	def catedraticos(self):
		self.inicio_seccion("CATEDRATICOS")
		catedraticos = []

		while self.actual.lexema != "}":
			self.esperar("PALABRA_RESERVADA", "catedratico")
			self.esperar("DOS_PUNTOS")
			nombre = self.esperar("CADENA").lexema
			self.esperar("CORCHETE_ABRE")
			codigo = self.campo_codigo("codigo")
			self.esperar("COMA")
			categoria = self.campo_categoria("categoria")
			self.esperar("CORCHETE_CIERRA")
			self.esperar("COMA")
			catedraticos.append({
				"nombre": nombre,
				"codigo": codigo,
				"categoria": categoria,
			})

		self.fin_seccion()
		return catedraticos

	def aulas(self):
		self.inicio_seccion("AULAS")
		aulas = []

		while self.actual.lexema != "}":
			self.esperar("PALABRA_RESERVADA", "aula")
			self.esperar("DOS_PUNTOS")
			nombre = self.esperar("CODIGO").lexema
			self.esperar("CORCHETE_ABRE")
			capacidad = self.campo_entero("capacidad")
			self.esperar("COMA")
			edificio = self.campo_codigo("edificio")
			self.esperar("CORCHETE_CIERRA")
			self.esperar("COMA")
			aulas.append({
				"nombre": nombre,
				"capacidad": capacidad,
				"edificio": edificio,
			})

		self.fin_seccion()
		return aulas

	def clases(self):
		self.inicio_seccion("CLASES")
		clases = []

		while self.actual.lexema != "}":
			self.esperar("PALABRA_RESERVADA", "clase")
			self.esperar("DOS_PUNTOS")
			curso = self.esperar("CODIGO").lexema
			self.esperar("PALABRA_RESERVADA", "con")
			catedratico = self.esperar("CODIGO").lexema
			self.esperar("PALABRA_RESERVADA", "en")
			aula = self.esperar("CODIGO").lexema
			self.esperar("CORCHETE_ABRE")
			dia = self.campo_dia("dia")
			self.esperar("COMA")
			inicio = self.campo_hora("inicio")
			self.esperar("COMA")
			fin = self.campo_hora("fin")
			self.esperar("COMA")
			seccion = self.campo_cadena("seccion")
			self.esperar("CORCHETE_CIERRA")
			self.esperar("COMA")
			clases.append({
				"curso": curso,
				"catedratico": catedratico,
				"aula": aula,
				"dia": dia,
				"inicio": inicio,
				"fin": fin,
				"seccion": seccion,
			})

		self.fin_seccion()
		return clases

	def campo_cadena(self, nombre):
		self.esperar("PALABRA_RESERVADA", nombre)
		self.esperar("DOS_PUNTOS")
		return self.esperar("CADENA").lexema

	def campo_codigo(self, nombre):
		self.esperar("PALABRA_RESERVADA", nombre)
		self.esperar("DOS_PUNTOS")
		return self.esperar("CODIGO").lexema

	def campo_entero(self, nombre):
		self.esperar("PALABRA_RESERVADA", nombre)
		self.esperar("DOS_PUNTOS")
		return self.esperar("ENTERO").lexema

	def campo_dia(self, nombre):
		self.esperar("PALABRA_RESERVADA", nombre)
		self.esperar("DOS_PUNTOS")
		return self.esperar("DIA").lexema

	def campo_categoria(self, nombre):
		self.esperar("PALABRA_RESERVADA", nombre)
		self.esperar("DOS_PUNTOS")
		return self.esperar("CATEGORIA").lexema

	def campo_hora(self, nombre):
		self.esperar("PALABRA_RESERVADA", nombre)
		self.esperar("DOS_PUNTOS")
		return self.esperar("HORA").lexema


def analizar_archivo(ruta):
	texto = Path(ruta).read_text(encoding="utf-8")
	lexer = Lexer(texto)
	tokens = lexer.analizar()

	if lexer.errores:
		errores = "\n".join(f"- {error}" for error in lexer.errores)
		raise ErrorSintactico(f"Se encontraron errores léxicos:\n{errores}")

	return Parser(tokens).analizar()


if __name__ == "__main__":
	ruta = Path(__file__).resolve().parent.parent / "test" / "prueba.hor"
	try:
		horario = analizar_archivo(ruta)
		print("Análisis sintáctico correcto.")
		print(f"Cursos: {len(horario['cursos'])}")
		print(f"Catedráticos: {len(horario['catedraticos'])}")
		print(f"Aulas: {len(horario['aulas'])}")
		print(f"Clases: {len(horario['clases'])}")
	except (OSError, ErrorSintactico) as error:
		print(f"Error: {error}")
