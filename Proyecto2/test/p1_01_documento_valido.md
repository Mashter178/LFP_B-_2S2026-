# Guía de estudio: Lenguajes Formales y de Programación

Este documento resume los temas principales del curso con **definiciones claras**, *ejemplos breves* y fragmentos de `código`.

## Introducción

Los lenguajes formales permiten describir con **precisión matemática** qué cadenas pertenecen a un lenguaje.

Un compilador transforma un programa fuente en otro lenguaje y *verifica* que cumpla las reglas del lenguaje de origen.

El curso se divide en tres bloques: análisis léxico, análisis sintáctico y construcción de herramientas en `Python`.

## Análisis léxico

### Tokens y lexemas

Un **token** es una categoría como identificador o número, y un *lexema* es la secuencia concreta de caracteres reconocida.

La función `siguiente_token()` entrega un token cada vez que el analizador sintáctico lo solicita.

#### Patrones

Un patrón describe todos los lexemas posibles de un token, normalmente mediante una expresión regular.

##### Ejemplos de patrones

El patrón de un identificador es una letra seguida de letras o dígitos.

###### Nota final del bloque

Los patrones se implementan con un autómata finito determinista.

### Autómatas finitos

- Autómata finito determinista
  - Una transición por símbolo
  - Sin transiciones vacías
- Autómata finito no determinista
  - Varias transiciones por símbolo
  - Con transiciones vacías
    - Se eliminan al convertir a determinista
    - Método del árbol
- Minimización de estados

### Errores léxicos

Un error léxico ocurre cuando una secuencia de caracteres no coincide con ningún patrón del lenguaje.

* Carácter desconocido
* Número mal formado
* Cadena sin cerrar

---

## Análisis sintáctico

### Gramáticas libres de contexto

Una gramática libre de contexto tiene **cuatro componentes**: terminales, no terminales, producciones y símbolo inicial.

+ Terminales
+ No terminales
+ Producciones
  + Lado izquierdo con un solo no terminal
  + Lado derecho con una secuencia de símbolos
+ Símbolo inicial

### Árboles de derivación

El árbol de derivación muestra cómo se aplican las producciones para reconocer una cadena.

- Raíz
  - Símbolo inicial
- Nodos internos
  - No terminales
    - Cada nodo representa una producción
    - Los hijos son los símbolos del lado derecho
- Hojas
  - Terminales
  - Tokens reconocidos

### Recursividad

Una producción es **recursiva** cuando el no terminal aparece en su propio lado derecho.

La recursividad por la izquierda es un problema para el análisis descendente, y se resuelve con la función `eliminar_recursion()`.

- Recursividad por la izquierda
- Recursividad por la derecha
- Recursividad central

---

## Citas importantes

> El análisis sintáctico es donde la teoría se encuentra con la práctica.
>> Y es donde más se aprende, según los estudiantes.

Otra cita de un solo nivel con formato:

> Un **buen diseño** de la gramática evita *muchos problemas* posteriores.

## Ejemplos de código

Un autómata sencillo se puede representar con un diccionario de transiciones.

```python
transiciones = {
    ("q0", "a"): "q1",
    ("q1", "b"): "q0",
}

def siguiente(estado, simbolo):
    return transiciones.get((estado, simbolo))
```

Un fragmento sin lenguaje indicado:

```
entrada: aabb
salida: aceptada
```

Y una última función con `return` explícito.

```java
public boolean acepta(String cadena) {
    return cadena.length() % 2 == 0;
}
```

-----

## Resumen del curso

Los **tres pasos** del procesamiento de un lenguaje son el análisis léxico, el análisis sintáctico y la generación del resultado.

Repase los temas con *calma* y practique con ejemplos propios.

- Revisar los apuntes
- Resolver los ejercicios
  - Autómatas
  - Gramáticas
- Preparar el proyecto

Fin del documento.
