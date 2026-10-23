# Documento con errores léxicos y sintácticos

Este archivo contiene errores intencionales. El analizador debe reportarlos todos en una sola pasada, sin detenerse en el primero, y seguir reconociendo correctamente el contenido válido que los rodea.

## Prueba 1: negrita sin cerrar

Este párrafo es correcto y contiene **negrita bien cerrada** y *cursiva bien cerrada*.

Este párrafo abre una **negrita que nunca se cierra y continúa hasta el final de la línea.

Este párrafo vuelve a ser correcto, con `código en línea` y texto normal.

## Prueba 2: cursiva sin cerrar

Esta línea contiene una *cursiva que nunca se cierra y termina sin el asterisco final.

Esta línea es válida y menciona la palabra cursiva sin usar asteriscos.

## Prueba 3: código en línea sin cerrar

Esta línea abre un `fragmento de código que no se cierra nunca.

Esta línea es válida y usa `código correcto` sin problemas.

## Prueba 4: encabezado inválido

####### Este encabezado tiene siete numerales y excede el máximo permitido

###### Este encabezado de nivel seis sí es válido

## Prueba 5: indentación inválida

- Lista con un salto de indentación demasiado grande
    - Este ítem sube dos niveles de una sola vez
- Ítem correcto de regreso al primer nivel
- Otro ítem correcto

Párrafo de separación entre las dos listas de esta prueba.

- Primer nivel correcto
  - Segundo nivel correcto
      - Este ítem salta del nivel uno al nivel tres
  - Regreso correcto al segundo nivel
- Regreso correcto al primer nivel

## Prueba 6: errores dentro de listas y citas

- Ítem normal
  - Ítem con una **negrita sin cerrar dentro de una sublista
  - Ítem normal después del error
- Ítem final de la lista

> Primera línea de la cita, correcta
>> Segunda línea con una *cursiva sin cerrar dentro de la cita
>> Otra segunda línea correcta

## Prueba 7: cita mal formada

>Esta cita no tiene espacio después del símbolo mayor que.

Párrafo correcto entre dos citas.

>Otra cita sin espacio después del símbolo.

> Esta cita sí está bien formada.

## Contenido válido intermedio

Después de tantos errores, el analizador debe seguir reconociendo con normalidad todos los elementos válidos.

### Lista válida

- Elemento uno
  - Subelemento uno
    - Subsubelemento uno
- Elemento dos

### Cita válida

> Primer nivel
>> Segundo nivel

### Bloque de código válido

```python
def saludar():
    return "hola"
```

---

### Más contenido válido

Un párrafo adicional con `código`, **negrita** y *cursiva* para confirmar que el análisis continúa con normalidad.

* Primer elemento de la lista final
* Segundo elemento de la lista final
  * Subelemento del segundo elemento
    * Sub-subelemento del segundo elemento

Un último párrafo válido con **negrita**, *cursiva* y `código` antes del error final.

## Prueba 8: bloque de código sin cerrar

El siguiente bloque se abre pero nunca se cierra. Todo lo que sigue hasta el final del archivo es contenido literal y no debe producir otros errores.

```python
def sin_cierre():
    # **esto no es negrita** porque está dentro del bloque
    print("el bloque nunca termina")
