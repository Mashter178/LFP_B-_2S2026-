# Manual de Usuario

## 1. Descripción del sistema

Este proyecto permite cargar datos de jugadores, sudokus e intentos; validar soluciones de sudoku; y generar reportes en formato HTML.

Se trabaja con una estructura MVC simple:

- Modelo: clases para Sudoku, Usuario y Partida
- Vista: menú y entrada/salida por consola
- Controlador: carga y procesamiento de archivos

## 2. Requisitos

- Python 3.x instalado
- Archivos .lfp ubicados en la carpeta Practica/test
- Carpeta Practica/report para guardar los archivos HTML generados

## 3. Ejecutar la aplicación

Desde la terminal, ubicarse en la carpeta principal y ejecutar:

```bash
python "Practica/MCV/main.py"
```

## 4. Menú principal

El sistema presenta este menú:

1. Cargar jugadores
2. Cargar sudokus
3. Cargar intentos
4. Validar un intento
5. Generar reporte por sudoku
6. Generar reporte por jugador
7. Generar top 10 mejores tiempos
8. Salir

## 5. Funciones del menú

### Opción 1: Cargar jugadores
Carga el contenido del archivo jugadores.lfp.

### Opción 2: Cargar sudokus
Carga el contenido del archivo sudokus.lfp.

### Opción 3: Cargar intentos
Carga el archivo intentos.lfp y calcula validaciones relacionadas con cada partida.

### Opción 4: Validar un intento
El usuario debe ingresar:

- tablero original (81 caracteres)
- solución propuesta (81 caracteres)

La aplicación valida que:

- la solución tenga 81 dígitos
- no modifique pistas originales
- cada fila, columna y caja siga la lógica del sudoku
- el resultado final sea correcto o no

### Opción 5: Generar reporte por sudoku
Genera un resumen de cada sudoku con:

- cantidad de intentos
- tiempo promedio
- tasa de éxito

### Opción 6: Generar reporte por jugador
Muestra el rendimiento por usuario:

- nombre y carnet
- nivel
- intentos realizados
- porcentaje promedio de validez
- tiempo promedio
- cantidad de sudokus resueltos correctamente

### Opción 7: Generar top 10 mejores tiempos
Muestra los 10 tiempos más rápidos de intentos resueltos correctamente.

### Opción 8: Salir
Cierra el programa.

## 6. Archivos HTML generados

Los reportes se guardan en la carpeta:

- Practica/report

Los nombres recomendados son:

- resumen_sudoku.html
- rendimiento_jugador.html
- top10_tiempos.html

## 7. Recomendaciones

- No ingresar cadenas con menos o más de 81 caracteres.
- Verificar que los archivos .lfp estén cargados antes de generar reportes.
- Si ocurre un error en la validación, revisar que se hayan ingresado solo dígitos.
- Presionar Enter para continuar luego de cada acción para mantener una consola más limpia.

## 8. Salida esperada

La aplicación debe mostrar mensajes como:

- Jugadores cargados correctamente.
- Sudokus cargados correctamente.
- Intentos cargados correctamente.
- Reporte generado: resumen_sudoku.html
- Error en la entrada: Debe ingresar exactamente 81 caracteres en cada tablero.

## 9. Observaciones

El sistema está pensado para uso escolar y de aprendizaje, con una implementación simple, clara y fácil de mantener.
