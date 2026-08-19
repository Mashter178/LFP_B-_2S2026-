import os
ruta = os.path.join(os.path.dirname(__file__), "inventario.lfp")

def cargar_inventario():
    inventario = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

            for linea in lineas:
                comida, cantidad, precio, ubicacion = linea.strip().split(",")

                producto = {
                    "comida": comida.strip(),
                    "cantidad": int(cantidad),
                    "precio": float(precio),
                    "ubicacion": ubicacion.strip()
                }

                inventario.append(producto)

    except FileNotFoundError:
        print("No se encontró el archivo de inventario.")

    return inventario


def mostrar_inventario(inventario):
    if not inventario:
        print("El inventario está vacío.")
        return

    print("Inventario:")
    for producto in inventario:
        print("-------------------------")
        print(f"Comida: {producto['comida']}")
        print(f"Cantidad: {producto['cantidad']}")
        print(f"Precio: {producto['precio']}")
        print(f"Ubicación: {producto['ubicacion']}")

#UI
def menu():
    inventario = []


    while True:
        os.system("cls")
        print("\n===== MENÚ =====")
        print("1. Cargar inventario")
        print("2. Mostrar inventario")
        print("3. Salir")

        opcion = input("Elige una opción: ")

        match opcion:
            case "1":
                inventario = cargar_inventario()
                print("Inventario cargado correctamente.")
                print("Presiona Enter para continuar...")
                input()

            case "2":
                mostrar_inventario(inventario)
                print("Presiona Enter para continuar...")
                input()

            case "3":
                print("Saliendo...")
                print("Presiona Enter para continuar...")
                input()
                break

            case _:
                print("Opción inválida.")
                print("Presiona Enter para continuar...")
                input()

menu()