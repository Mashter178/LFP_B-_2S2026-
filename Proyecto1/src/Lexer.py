from pathlib import Path


class Token:
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"{self.tipo}({self.lexema!r})"


class Lexer:
    PALABRAS_RESERVADAS = {
        "HORARIO",
        "CURSOS",
        "curso",
        "CATEDRATICOS",
        "catedratico",
        "AULAS",
        "aula",
        "CLASES",
        "clase",
        "con",
        "en",
        "codigo",
        "creditos",
        "categoria",
        "capacidad",
        "edificio",
        "dia",
        "inicio",
        "fin",
        "seccion",
        "LUNES",
        "MARTES",
        "TITULAR",
        "INTERINO",
    }

    SIMBOLOS = {
        "{": "LLAVE_ABRE",
        "}": "LLAVE_CIERRA",
        "[": "CORCHETE_ABRE",
        "]": "CORCHETE_CIERRA",
        ":": "DOS_PUNTOS",
        ",": "COMA",
        ";": "PUNTO_COMA",
    }

    def __init__(self, texto):
        self.texto = texto
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.errores = []

    def avanzar(self):
        caracter = self.texto[self.posicion]
        self.posicion += 1

        if caracter == "\n":
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1

        return caracter

    def analizar(self):
        while self.posicion < len(self.texto):
            caracter = self.texto[self.posicion]

            if caracter.isspace():
                self.avanzar()
                continue

            if caracter in self.SIMBOLOS:
                linea = self.linea
                columna = self.columna
                tipo = self.SIMBOLOS[self.avanzar()]
                self.tokens.append(Token(tipo, caracter, linea, columna))
                continue

            if caracter == '"':
                self.leer_cadena()
                continue

            if caracter.isdigit():
                self.leer_numero_o_hora()
                continue

            if caracter.isalpha() or caracter == "_":
                self.leer_identificador()
                continue

            self.errores.append(
                f"Línea {self.linea}, columna {self.columna}: "
                f"carácter no válido {caracter!r}"
            )
            self.avanzar()

        self.tokens.append(Token("EOF", "", self.linea, self.columna))
        return self.tokens

    def leer_cadena(self):
        linea = self.linea
        columna = self.columna
        lexema = self.avanzar()  # Comilla inicial

        while self.posicion < len(self.texto):
            caracter = self.avanzar()
            lexema += caracter

            if caracter == '"':
                self.tokens.append(Token("CADENA", lexema, linea, columna))
                return

        self.errores.append(
            f"Línea {linea}, columna {columna}: cadena sin cerrar"
        )

    def leer_identificador(self):
        linea = self.linea
        columna = self.columna
        lexema = ""

        while self.posicion < len(self.texto):
            caracter = self.texto[self.posicion]

            if not (caracter.isalnum() or caracter == "_"):
                break

            lexema += self.avanzar()

        tipo = (
            "PALABRA_RESERVADA"
            if lexema in self.PALABRAS_RESERVADAS
            else "IDENTIFICADOR"
        )

        self.tokens.append(Token(tipo, lexema, linea, columna))

    def leer_numero_o_hora(self):
        linea = self.linea
        columna = self.columna
        lexema = ""

        while self.posicion < len(self.texto):
            caracter = self.texto[self.posicion]

            if not caracter.isdigit() and caracter != ":":
                break

            lexema += self.avanzar()

        if (
            len(lexema) == 5
            and lexema[2] == ":"
            and lexema[:2].isdigit()
            and lexema[3:].isdigit()
        ):
            tipo = "HORA"
        elif lexema.isdigit():
            tipo = "NUMERO"
        else:
            tipo = "LEXEMA_INVALIDO"

        self.tokens.append(Token(tipo, lexema, linea, columna))


ruta = Path("Proyecto1/test/prueba.txt")
texto = ruta.read_text(encoding="utf-8")

lexer = Lexer(texto)
tokens = lexer.analizar()

for token in tokens:
    print(token)

for error in lexer.errores:
    print("ERROR:", error)