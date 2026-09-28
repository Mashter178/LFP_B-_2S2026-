from pathlib import Path

from sintatic import ErrorSintactico, analizar_archivo as analizar_archivo_sintactico


class ErrorSemantico:
	def __init__(self, mensaje):
		self.mensaje = mensaje

	def __str__(self):
		return self.mensaje


class AnalizadorSemantico:
	DIAS_VALIDOS = {
		"LUNES",
		"MARTES",
		"MIERCOLES",
		"JUEVES",
		"VIERNES",
		"SABADO",
		"DOMINGO",
	}

	CATEGORIAS_VALIDAS = {"TITULAR", "INTERINO", "AUXILIAR"}

	def __init__(self, horario):
		self.horario = horario
		self.errores = []
		self.cursos = {}
		self.catedraticos = {}
		self.aulas = {}

	def analizar(self):
		self.construir_tablas()
		self.validar_referencias()
		self.validar_datos()
		self.validar_choques()
		return self.errores

	def construir_tablas(self):
		self.registrar_repetidos(
			self.horario["cursos"], "codigo", self.cursos, "curso"
		)
		self.registrar_repetidos(
			self.horario["catedraticos"], "codigo", self.catedraticos, "catedrático"
		)
		self.registrar_repetidos(
			self.horario["aulas"], "nombre", self.aulas, "aula"
		)

	def registrar_repetidos(self, elementos, campo, tabla, descripcion):
		for elemento in elementos:
			identificador = elemento[campo].strip('"')

			if identificador in tabla:
				self.errores.append(
					ErrorSemantico(
						f'El {descripcion} "{identificador}" está declarado más de una vez.'
					)
				)
			else:
				tabla[identificador] = elemento

	def validar_referencias(self):
		for clase in self.horario["clases"]:
			curso = clase["curso"].strip('"')
			catedratico = clase["catedratico"].strip('"')
			aula = clase["aula"].strip('"')

			if curso not in self.cursos:
				self.errores.append(
					ErrorSemantico(
						f'El curso "{curso}" usado en una clase no está declarado.'
					)
				)

			if catedratico not in self.catedraticos:
				self.errores.append(
					ErrorSemantico(
						f'El catedrático "{catedratico}" usado en una clase no está declarado.'
					)
				)

			if aula not in self.aulas:
				self.errores.append(
					ErrorSemantico(
						f'El aula "{aula}" usada en una clase no está declarada.'
					)
				)

	def validar_datos(self):
		for curso in self.horario["cursos"]:
			creditos = self.numero(curso["creditos"])
			if creditos <= 0:
				self.errores.append(
					ErrorSemantico(
						f'El curso {curso["codigo"]} debe tener créditos mayores que cero.'
					)
				)

		for catedratico in self.horario["catedraticos"]:
			if catedratico["categoria"] not in self.CATEGORIAS_VALIDAS:
				self.errores.append(
					ErrorSemantico(
						f'La categoría "{catedratico["categoria"]}" no es válida.'
					)
				)

		for aula in self.horario["aulas"]:
			capacidad = self.numero(aula["capacidad"])
			if capacidad <= 0:
				self.errores.append(
					ErrorSemantico(
						f'El aula {aula["nombre"]} debe tener capacidad mayor que cero.'
					)
				)

		for clase in self.horario["clases"]:
			if clase["dia"] not in self.DIAS_VALIDOS:
				self.errores.append(
					ErrorSemantico(
						f'El día "{clase["dia"]}" no es válido para la clase {clase["curso"]}.'
					)
				)

			inicio = self.a_minutos(clase["inicio"])
			fin = self.a_minutos(clase["fin"])
			if inicio >= fin:
				self.errores.append(
					ErrorSemantico(
						f'La clase {clase["curso"]} tiene una hora de inicio igual o posterior a la hora de fin.'
					)
				)

	def validar_choques(self):
		clases = self.horario["clases"]

		for indice, primera in enumerate(clases):
			for segunda in clases[indice + 1:]:
				if primera["dia"] != segunda["dia"]:
					continue

				if not self.se_superponen(primera, segunda):
					continue

				if primera["catedratico"] == segunda["catedratico"]:
					self.errores.append(
						ErrorSemantico(
							f'Choque: el catedrático {primera["catedratico"]} '
							f'está asignado a dos clases el {primera["dia"]} al mismo tiempo.'
						)
					)

				if primera["aula"] == segunda["aula"]:
					self.errores.append(
						ErrorSemantico(
							f'Choque: el aula {primera["aula"]} está asignada a dos clases '
							f'el {primera["dia"]} al mismo tiempo.'
						)
					)

	@staticmethod
	def numero(valor):
		return int(valor.strip('"'))

	@staticmethod
	def a_minutos(hora):
		horas, minutos = hora.split(":")
		return int(horas) * 60 + int(minutos)

	def se_superponen(self, primera, segunda):
		inicio_primera = self.a_minutos(primera["inicio"])
		fin_primera = self.a_minutos(primera["fin"])
		inicio_segunda = self.a_minutos(segunda["inicio"])
		fin_segunda = self.a_minutos(segunda["fin"])
		return inicio_primera < fin_segunda and inicio_segunda < fin_primera


def analizar_archivo(ruta):
	horario = analizar_archivo_sintactico(ruta)
	analizador = AnalizadorSemantico(horario)
	return horario, analizador.analizar()


if __name__ == "__main__":
	ruta = Path(__file__).resolve().parent.parent / "test" / "prueba.hor"

	try:
		horario, errores = analizar_archivo(ruta)
		if errores:
			print("Se encontraron errores semánticos:")
			for error in errores:
				print(f"- {error}")
		else:
			print("Análisis léxico, sintáctico y semántico correcto.")
			print(f"Se analizaron {len(horario['clases'])} clases.")
	except (OSError, ErrorSintactico) as error:
		print(f"Error previo al análisis semántico: {error}")
