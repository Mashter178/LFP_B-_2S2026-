class Telefono:
    #Constructor
    def __init__(self, marca, bateria, numero, memoria):
        #Atributos Publicos
        self.marcas = marca
        self.bateria = bateria
        self.numero = numero
        self.memoria = memoria
        self._precio = None

    def llamar(self, numero):
        print(f"Llamando al {numero} desde el teléfono {self.marcas}")

    def Cargar(self, bateria):
        print(f"Cargando el teléfono {self.marcas} con batería de {self.bateria} mAh")

    def Prender(self):
        print(f"Prendiendo el teléfono {self.marcas}")

    def Apagar(self):
        print(f"Apagando el teléfono {self.marcas}")

    def set_precio(self, precio):
        self._precio = precio

    def get_precio(self):
        return self._precio

    def __str__(self):
        return f"Marca: {self.marcas}, Batería: {self.bateria} mAh, Número: {self.numero}, Memoria: {self.memoria}, Precio: {self._precio}"

if __name__ == "__main__":
    #Creando Objeto
    Samsung = Telefono("Samsung", 4000, "41256881", "128GB")
    Oppo = Telefono("OPPO", 5000, "98564512", "256GB")
    iPhone = Telefono("iPhone", 3000, "98765432", "64GB")

    print("-----------------------")
    iPhone.set_precio(1000)
    print(iPhone)
    iPhone.Prender()
    iPhone.llamar("987654321")
    iPhone.Cargar(3000)
    print("-----------------------")
    Oppo.set_precio(400)
    print(Oppo)
    Oppo.Prender()
    Oppo.llamar("123456789")
    Oppo.Apagar()
    print("-----------------------")