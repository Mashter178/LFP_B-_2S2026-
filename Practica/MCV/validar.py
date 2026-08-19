def cadena_a_matriz(cadena):
    cadena = cadena.strip()
    if len(cadena) != 81 or not cadena.isdigit():
        raise ValueError("La cadena debe tener exactamente 81 digitos")

    matriz = []
    for i in range(0, 81, 9):
        fila = [int(c) for c in cadena[i:i+9]]
        matriz.append(fila)
    return matriz


def valida_pistas(original, propuesta):
    for f in range(9):
        for c in range(9):
            if original[f][c] != 0 and propuesta[f][c] != original[f][c]:
                return False
    return True


def valida_grupo(grupo):
    grupo = [x for x in grupo if x != 0]
    if len(grupo) != 9:
        return False
    return sorted(grupo) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def valida_tablero(matriz):
    filas_ok = 0
    columnas_ok = 0
    cajas_ok = 0

    for f in range(9):
        if valida_grupo(matriz[f]):
            filas_ok += 1

    for c in range(9):
        columna = [matriz[f][c] for f in range(9)]
        if valida_grupo(columna):
            columnas_ok += 1

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            caja = []
            for f in range(i, i + 3):
                for c in range(j, j + 3):
                    caja.append(matriz[f][c])
            if valida_grupo(caja):
                cajas_ok += 1

    total = filas_ok + columnas_ok + cajas_ok
    porcentaje = (total / 27) * 100
    return porcentaje, filas_ok, columnas_ok, cajas_ok


def calificar_intento(cadena_original, cadena_solucion):
    try:
        original = cadena_a_matriz(cadena_original)
        propuesta = cadena_a_matriz(cadena_solucion)

        pistas_ok = valida_pistas(original, propuesta)
        porcentaje, filas_ok, columnas_ok, cajas_ok = valida_tablero(propuesta)

        resuelto = (porcentaje == 100) and pistas_ok

        return {
            "porcentaje_validez": porcentaje,
            "filas_validas": filas_ok,
            "columnas_validas": columnas_ok,
            "cajas_validas": cajas_ok,
            "pistas_respetadas": pistas_ok,
            "resuelto_correctamente": resuelto,
        }
    except ValueError as e:
        raise ValueError(f"Formato inválido del tablero: {e}")