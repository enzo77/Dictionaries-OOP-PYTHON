class Ser:
    def __init__(self, tipo):
        self.tipo = tipo

class Animal(Ser):
    def __init__(self, tipo, reino):
        super().__init__(tipo)
        self.reino = reino

class Mamifero(Animal):
    def __init__(self, tipo, reino, clase):
        super().__init__(tipo, reino)
        self.clase = clase

m = Mamifero("ser vivo", "animal", "perro")
print(m.clase, m.reino, m.tipo)