from abc import ABC, abstractmethod

"""
DOC string: Ejercicio 7: Polimorfismo
Crea una clase abstracta "Animal" con un método abstracto "sound()". Luego

"""

class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):
    def sound(self): return "Woof"


class Cat(Animal):
    def sound(self): return "Meow"

class Duck(Animal):
    def sound(self): return "Quack"
    
def make_all_sounds(animals):
    for a in animals:
        print(a.sound())    

animals = [Dog(), Cat(), Duck(), Dog()]
make_all_sounds(animals)