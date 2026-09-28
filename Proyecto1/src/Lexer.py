from pathlib import Path


class Token:
    def __init__(self, numero, tipo, lexema, linea, columna):
        self.numero = numero
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"Token({self.numero}, {self.tipo!r}, {self.lexema!r}, {self.linea}:{self.columna})"

    def como_diccionario(self):
        return {
            "numero": self.numero,
            "lexema": self.lexema,
            "tipo": self.tipo,
            "linea": self.linea,
            "columna": self.columna,
        }


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

    def como_diccionario(self):
        return {
            "numero": self.numero,
            "lexema": self.lexema,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "linea": self.linea,
            "columna": self.columna,
        }


class AnalizadorLexico:
    DIAS = {
        "LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO",
    }
    CATEGORIAS = {"TITULAR", "INTERINO", "AUXILIAR"}

    PALABRAS_RESERVADAS = {
        "HORARIO", "CURSOS", "curso", "CATEDRATICOS", "catedratico",
        "AULAS", "aula", "CLASES", "clase", "con", "en", "codigo",
        "creditos", "categoria", "capacidad", "edificio", "dia", "inicio",
        "fin", "seccion", "LUNES", "MARTES", "MIERCOLES", "JUEVES",
        "VIERNES", "SABADO", "DOMINGO", "TITULAR", "INTERINO", "AUXILIAR",
    }

    SIMBOLOS = {
        "{": "LLAVE_ABRE", "}": "LLAVE_CIERRA",
        "[": "CORCHETE_ABRE", "]": "CORCHETE_CIERRA",
        ":": "DOS_PUNTOS", ",": "COMA", ";": "PUNTO_COMA",
    }

    def __init__(self, texto):
        self.texto = texto
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.numero_token = 0
        self.numero_error = 0
        self.tokens = []
        self.errores = []

    def actual(self):
        if self.posicion >= len(self.texto):
            return ""
        return self.texto[self.posicion]

    def siguiente(self):
        if self.posicion + 1 >= len(self.texto):
            return ""
        return self.texto[self.posicion + 1]

    def avanzar(self):
        caracter = self.actual()
        if caracter == "":
            return caracter
        self.posicion += 1
        if caracter == "\n":
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        return caracter

    @staticmethod
    def es_letra(caracter):
        return ("A" <= caracter <= "Z") or ("a" <= caracter <= "z")

    @staticmethod
    def es_digito(caracter):
        return "0" <= caracter <= "9"

    @staticmethod
    def es_inicio_identificador(caracter):
        return AnalizadorLexico.es_letra(caracter) or caracter == "_"

    @staticmethod
    def es_parte_identificador(caracter):
        return (
            AnalizadorLexico.es_inicio_identificador(caracter)
            or AnalizadorLexico.es_digito(caracter)
        )

    def agregar_token(self, tipo, lexema, linea, columna):
        self.numero_token += 1
        token = Token(self.numero_token, tipo, lexema, linea, columna)
        self.tokens.append(token)
        return token

    def agregar_error(self, lexema, tipo, descripcion, linea, columna):
        self.numero_error += 1
        self.errores.append(
            ErrorLexico(
                self.numero_error, lexema, tipo, descripcion, linea, columna
            )
        )

    def ignorar_espacios_y_comentarios(self):
        while self.posicion < len(self.texto):
            if self.actual() in " \t\r\n":
                self.avanzar()
                continue

            if self.actual() == "#" and self.siguiente() == "#":
                self.avanzar()
                self.avanzar()
                while self.posicion < len(self.texto) and self.actual() != "\n":
                    self.avanzar()
                continue
            break

    def siguiente_token(self):
        self.ignorar_espacios_y_comentarios()

        if self.posicion >= len(self.texto):
            return self.agregar_token("EOF", "", self.linea, self.columna)

        linea = self.linea
        columna = self.columna
        caracter = self.actual()

        if caracter in self.SIMBOLOS:
            self.avanzar()
            return self.agregar_token(self.SIMBOLOS[caracter], caracter, linea, columna)

        if caracter == '"':
            return self.leer_cadena(linea, columna)

        if self.es_digito(caracter):
            return self.leer_numero_o_hora(linea, columna)

        if self.es_inicio_identificador(caracter):
            return self.leer_identificador(linea, columna)

        self.agregar_error(
            caracter,
            "CARACTER_NO_VALIDO",
            "El carácter no pertenece al alfabeto de HorarioScript.",
            linea,
            columna,
        )
        self.avanzar()
        return self.siguiente_token()

    def leer_cadena(self, linea, columna):
        lexema = self.avanzar()
        cerrada = False

        while self.posicion < len(self.texto):
            caracter = self.avanzar()
            lexema += caracter
            if caracter == '"':
                cerrada = True
                break
            if caracter == "\n":
                break

        if not cerrada:
            self.agregar_error(
                lexema,
                "CADENA_SIN_CERRAR",
                "La cadena no tiene comilla de cierre.",
                linea,
                columna,
            )
            return self.siguiente_token()

        tipo = "CODIGO" if self.es_codigo(lexema) else "CADENA"
        return self.agregar_token(tipo, lexema, linea, columna)

    def leer_identificador(self, linea, columna):
        lexema = ""
        while self.es_parte_identificador(self.actual()):
            lexema += self.avanzar()

        if lexema in self.DIAS:
            tipo = "DIA"
        elif lexema in self.CATEGORIAS:
            tipo = "CATEGORIA"
        elif lexema in self.PALABRAS_RESERVADAS:
            tipo = "PALABRA_RESERVADA"
        else:
            tipo = "IDENTIFICADOR"
        return self.agregar_token(tipo, lexema, linea, columna)

    def leer_numero_o_hora(self, linea, columna):
        lexema = ""
        while self.es_digito(self.actual()):
            lexema += self.avanzar()

        if self.actual() == ":":
            lexema += self.avanzar()
            cantidad_digitos = 0
            while self.es_digito(self.actual()):
                lexema += self.avanzar()
                cantidad_digitos += 1

            if len(lexema) == 5 and cantidad_digitos == 2:
                horas = int(lexema[0:2])
                minutos = int(lexema[3:5])
                if 6 <= horas <= 21 and 0 <= minutos <= 59:
                    return self.agregar_token("HORA", lexema, linea, columna)

                self.agregar_error(
                    lexema,
                    "HORA_FUERA_DE_RANGO",
                    "La hora debe estar entre 06:00 y 21:00.",
                    linea,
                    columna,
                )
                return self.siguiente_token()

            self.agregar_error(
                lexema,
                "HORA_INVALIDA",
                "La hora debe tener el formato HH:MM.",
                linea,
                columna,
            )
            return self.siguiente_token()

        return self.agregar_token("ENTERO", lexema, linea, columna)

    def es_codigo(self, lexema):
        if len(lexema) < 5 or lexema[0] != '"' or lexema[-1] != '"':
            return False

        contenido = lexema[1:-1]
        guion = False
        indice = 0
        while indice < len(contenido):
            caracter = contenido[indice]
            if caracter == "-":
                if guion or indice == 0 or indice == len(contenido) - 1:
                    return False
                guion = True
            elif not (self.es_letra(caracter) or self.es_digito(caracter)):
                return False
            indice += 1
        return guion

    def analizar(self):
        while True:
            token = self.siguiente_token()
            if token.tipo == "EOF":
                break
        return self.tokens


Lexer = AnalizadorLexico


if __name__ == "__main__":
    ruta = Path(__file__).resolve().parent.parent / "test" / "prueba.hor"
    lexer = AnalizadorLexico(ruta.read_text(encoding="utf-8"))
    lexer.analizar()

    print("TABLA DE TOKENS")
    for token in lexer.tokens:
        print(token.como_diccionario())

    print("\nTABLA DE ERRORES LEXICOS")
    for error in lexer.errores:
        print(error.como_diccionario())
