import re

PATRONES = [
    ("PALABRA_RESERVADA", r"\b(?:if|while|for|int|float|return)\b"),
    ("IDENTIFICADOR_INVALIDO", r"[0-9]+[A-Za-z_][A-Za-z0-9_]*"),
    ("NUMERO_REAL", r"\d+\.\d+"),
    ("NUMERO_ENTERO", r"\d+"),
    ("IDENTIFICADOR", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OPERADOR_RELACIONAL", r"==|!=|<=|>=|<|>"),
    ("OPERADOR_ARITMETICO", r"\+|-|\*|/"),
    ("ASIGNACION", r"="),
    ("DELIMITADOR", r"[(){};,]"),
]

PATRON_GENERAL = re.compile(
    "|".join(f"(?P<T{i}>{patron})"
            for i, (_, patron) in enumerate(PATRONES))
)

CODIGO = """int 123numero = 5;
float valor# = 10.5;
if (123numero > valor#) { return 0; }"""

tokens = []
errores = []

linea = 1
posicion = 0

while posicion < len(CODIGO):
    caracter = CODIGO[posicion]

    if caracter.isspace():
        if caracter == "\n":
            linea += 1
        posicion += 1
        continue

    coincidencia = PATRON_GENERAL.match(CODIGO, posicion)

    if coincidencia:
        indice = int(coincidencia.lastgroup[1:])
        categoria = PATRONES[indice][0]
        lexema = coincidencia.group()

        if categoria == "IDENTIFICADOR_INVALIDO":
            errores.append((linea, lexema, "Un identificador no puede iniciar con un número"))
        else:
            tokens.append((categoria, lexema, PATRONES[indice][1]))

        posicion = coincidencia.end()
    else:
        errores.append((linea, caracter, "Carácter no válido"))
        posicion += 1

print("\nTOKENS RECONOCIDOS")
print(f"{'TOKEN':<24} {'LEXEMA':<12} PATRÓN")
print("-" * 75)
for token, lexema, patron in tokens:
    print(f"{token:<24} {lexema:<12} {patron}")

print("\nERRORES LÉXICOS")
if errores:
    for linea, lexema, descripcion in errores:
        print(f"- Línea {linea}: '{lexema}' -> {descripcion}")
else:
    print("Ningún error encontrado.")