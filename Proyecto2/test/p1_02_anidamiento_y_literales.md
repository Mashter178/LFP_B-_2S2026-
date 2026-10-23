# Pruebas de anidamiento y contenido literal

Este archivo verifica que el analizador respete la **jerarquía** de listas y citas, y que trate como texto literal el contenido de los bloques de código.

## Listas con tres niveles

- Nivel uno, primer ítem
  - Nivel dos, primer ítem
    - Nivel tres, primer ítem
    - Nivel tres, segundo ítem
  - Nivel dos, segundo ítem
- Nivel uno, segundo ítem
  - Nivel dos con un solo hijo
    - Nivel tres final

## Lista con cuatro niveles

- Lenguajes
  - Naturales
  - Formales
    - Regulares
      - Expresiones regulares
      - Autómatas finitos
    - Libres de contexto
      - Autómatas de pila
- Procesadores
  - Intérprete
  - Compilador

## Descensos de varios niveles a la vez

* Primer elemento
  * Segundo nivel
    * Tercer nivel
* Regreso directo al primer nivel
  * Otro segundo nivel
* Último elemento

## Formato dentro de las listas

- Un ítem con **negrita** y *cursiva*
  - Un ítem con `código` en línea
    - Un ítem con **negrita**, *cursiva* y `código` juntos
- *Cursiva* al inicio del ítem
- **Negrita** al inicio del ítem
- `Código` al inicio del ítem

## Viñetas y cursiva en el inicio de línea

*Este párrafo comienza con cursiva y no es una lista.*

**Este párrafo comienza con negrita y tampoco es una lista.**

* *Esta línea sí es una lista y tiene cursiva dentro*
* **Esta también es una lista con negrita**

## Símbolos que no forman estructuras

#sinespacio no es un encabezado porque falta el espacio.

+sinespacio tampoco es una viñeta.

-sinespacio tampoco es una viñeta.

Use la bandera --verbose y la opción -h para obtener ayuda.

## Citas anidadas

> Primer nivel de la cita
>> Segundo nivel de la cita
>>> Tercer nivel de la cita
>> Regreso al segundo nivel
> Regreso al primer nivel

Una cita con espacios entre los símbolos:

> > Cita de segundo nivel escrita con espacio

> Cita de primer nivel con **negrita**, *cursiva* y `código`
>> Cita de segundo nivel con **negrita**

## Contenido literal en bloques de código

El contenido de este bloque no debe interpretarse como Markdown.

```
# Esto no es un encabezado
- Esto no es una viñeta
  - Ni esto una sublista
> Esto no es una cita
---
**Esto no es negrita
*Ni esto cursiva
`Ni esto código
```

Otro bloque con lenguaje, que incluye líneas vacías:

```python
def principal():
    # **comentario** con símbolos *especiales*

    print("Hola")

    return 0
```

## Código en línea con símbolos

El código en línea conserva sus símbolos: `a**b`, `*puntero`, `#comentario` y `-resta`.

La expresión `**kwargs` en Python no activa la negrita dentro de `código`.

Los operadores `*`, `**` y `>` se muestran tal cual dentro de las comillas invertidas.

---

---

## Reglas horizontales

Texto antes de la regla.

---

Texto entre dos reglas.

--------

Texto después de la regla larga.

Fin de las pruebas de anidamiento.
