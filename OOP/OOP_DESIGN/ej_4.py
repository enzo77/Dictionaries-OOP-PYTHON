class Volador:
    def volar(self):
        return f"puedo Volar"

class Nadador:
    def nadar(self):
        return f"puedo Nadar"


class Pato(Volador, Nadador):
    def presentarse(self):
        return f"Soy un pato: {self.volar()} y {self.nadar()}"
    
p = Pato()
print(p.presentarse())   