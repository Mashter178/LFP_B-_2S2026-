import os

from validar import cadena_a_matriz, valida_pistas, valida_tablero

class Vista:
    def limpiar_pantalla(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pausar(self):
        input("\nPresione Enter para continuar...")

    def mostrar_menu(self):
        self.limpiar_pantalla()
        print("\n=== MENÚ ===")
        print("1. Cargar jugadores")
        print("2. Cargar sudokus")
        print("3. Cargar intentos")
        print("4. Validar un intento")
        print("5. Generar reporte por sudoku")
        print("6. Generar reporte por jugador")
        print("7. Generar top 10 mejores tiempos")
        print("8. Salir")

    def leer_opcion(self):
        try:
            return int(input("Seleccione una opción: "))
        except ValueError:
            print("Debe ingresar un número.")
            return -1

    def mostrar_resultado(self, mensaje):
        print(mensaje)
    
    def leer_texto(self, texto):
        return input(texto)

def main():
    while True:
        menu()
        opcion = int(input("Ingrese opción: "))

        if opcion == 1:
            original = input("Ingrese tablero original: ")
            solucion = input("Ingrese solución propuesta: ")
            resultado = calificar_intento(original, solucion)
            print(resultado)
        elif opcion == 2:
            break

if __name__ == "__main__":
    main()

