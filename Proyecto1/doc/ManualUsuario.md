# Manual de Usuario

## 1. Descripcion

HorarioScript es una herramienta para analizar archivos de horarios academicos con extension `.hor`. El sistema valida el archivo en tres etapas:

1. Analisis lexico.
2. Analisis sintactico.
3. Analisis semantico.

## 2. Requisitos

- Python 3.10 o superior.
- Tkinter, incluido normalmente con Python para Windows.
- Un archivo con extension `.hor`.

## 3. Ejecucion

Desde la carpeta raiz del proyecto:

```powershell
python .\Proyecto1\src\app.py
```

El comando abre la interfaz grafica.

Para ejecutar solamente en consola:

```powershell
python .\Proyecto1\src\app.py --consola
```

Tambien se puede iniciar la interfaz con un archivo seleccionado:

```powershell
python .\Proyecto1\src\app.py .\Proyecto1\test\prueba.hor
```

## 4. Uso de la interfaz

1. Presione `Seleccionar .hor`.
2. Seleccione un archivo dentro de la carpeta `Proyecto1/test` o cualquier otra ubicacion.
3. Presione `Analizar`.
4. Consulte las pestanas de resultados.
5. Presione `Generar HTML` para crear los reportes.

### Interfaz principal

La ventana permite seleccionar el archivo, ejecutar el analisis y consultar
las diferentes pestanas del sistema.

![Interfaz principal de HorarioScript](Imagen2.png)

## 5. Pestanas

- **Resumen:** estado general y cantidades encontradas.
- **Tokens:** tabla de tokens con lexema, tipo, linea y columna.
- **Errores lexicos:** errores encontrados durante el recorrido del archivo.
- **Cursos:** cursos declarados.
- **Catedraticos:** catedraticos y categorias.
- **Aulas:** aulas, capacidad y edificio.
- **Clases:** relaciones entre curso, catedratico, aula y horario.
- **Estadisticas:** cantidades y tiempo total programado.

### Pestana de tokens

La pestana `Tokens` presenta el resultado del analisis lexico con el numero,
lexema, tipo, linea y columna de cada token.

![Pestana de tokens](Imagen3.png)

## 6. Reportes HTML

Los reportes se guardan en `Proyecto1/report`:

- `resumen_general.html`
- `clases_por_dia.html`
- `ocupacion.html`

## 7. Mensajes de error

El sistema informa la fase donde ocurre el problema. Los errores lexicos muestran el lexema, tipo, descripcion, linea y columna. Los errores semanticos indican referencias inexistentes, datos invalidos o choques de horario.
