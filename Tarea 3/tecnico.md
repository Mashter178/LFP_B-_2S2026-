# Expresiones regulares del analizador léxico

El analizador utiliza expresiones regulares para reconocer los diferentes
componentes del código fuente. Cada expresión se guarda junto con el nombre
de la categoría del token en `PATRONES`.

## Símbolos utilizados

| Símbolo | Significado |
|---|---|
| `\b` | Indica un límite de palabra. Evita reconocer una palabra reservada dentro de otra palabra. |
| `(?: ... )` | Agrupa opciones sin crear un grupo capturable. |
| `\|` | Significa "o". Permite elegir entre varias alternativas. |
| `\d` | Representa cualquier dígito del 0 al 9. |
| `+` | Indica una o más repeticiones. |
| `.` | Representa cualquier carácter; dentro de `\.` se interpreta como un punto literal. |
| `[ ... ]` | Define un conjunto de caracteres permitidos. |
| `[A-Za-z]` | Permite una letra mayúscula o minúscula sin incluir la ñ. |
| `_` | Representa literalmente el guion bajo. |
| `*` | Indica cero o más repeticiones. |

## Patrones de tokens

### Palabras reservadas

```text
\b(?:if|while|for|int|float|return)\b
```

Reconoce únicamente las palabras `if`, `while`, `for`, `int`, `float` y
`return`. Los límites `\b` evitan que, por ejemplo, `integer` sea reconocido
como la palabra reservada `int`.

### Identificador inválido

```text
[0-9]+[A-Za-z_][A-Za-z0-9_]*
```

Detecta nombres como `123numero`. Comienzan con uno o más números y después
contienen una letra o un guion bajo. Se reportan como error porque un
identificador válido no puede comenzar con un número.

### Número real

```text
\d+\.\d+
```

Reconoce números con parte entera y parte decimal, como `10.5`.

- `\d+`: uno o más dígitos antes del punto.
- `\.`: un punto decimal literal.
- `\d+`: uno o más dígitos después del punto.

### Número entero

```text
\d+
```

Reconoce uno o más dígitos consecutivos, como `5` y `0`.

### Identificador válido

```text
[A-Za-z_][A-Za-z0-9_]*
```

El primer carácter debe ser una letra o `_`. Los caracteres siguientes pueden
ser letras, números o `_`. Por ejemplo, `valor` y `valor2` son válidos.

### Operadores relacionales

```text
==|!=|<=|>=|<|>
```

Reconoce los operadores `==`, `!=`, `<=`, `>=`, `<` y `>`. Las opciones de dos
caracteres aparecen primero para que `>=` no se separe en `>` y `=`.

### Operadores aritméticos

```text
\+|-|\*|/
```

Reconoce `+`, `-`, `*` y `/`. Los símbolos `+` y `*` se escapan con `\` porque
tienen un significado especial dentro de una expresión regular.

### Asignación

```text
=
```

Reconoce el operador de asignación `=`.

### Delimitadores

```text
[(){};,]
```

Reconoce los caracteres `(`, `)`, `{`, `}`, `;` y `,`.

## Orden de evaluación

Todos los patrones se unen mediante `|` en `PATRON_GENERAL`. El analizador
prueba las alternativas en el orden en que aparecen en `PATRONES`. Por eso:

1. Las palabras reservadas aparecen antes que los identificadores.
2. Los identificadores inválidos aparecen antes que los números.
3. Los números reales aparecen antes que los enteros.
4. Los operadores de dos caracteres aparecen antes que los de un carácter.

Cuando ningún patrón coincide con el carácter actual, el analizador lo
reporta como un error léxico. En el código proporcionado, el carácter `#` se
detecta de esta manera.
