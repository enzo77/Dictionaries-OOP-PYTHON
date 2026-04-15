def saludar(nombre):
    return "Hola, " + nombre

print("Soy saludos.py y mi __name__ es:", __name__)

if __name__ == "__main__":
    print(saludar("Mundo"))  # esto solo corre si ejecutas saludos.py directamente