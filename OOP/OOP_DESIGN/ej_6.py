"""Módulo de ejemplo con instrumentos musicales y un concierto.

Este módulo define una interfaz abstracta para instrumentos y varias
implementaciones concretas. También incluye una función para ejecutar
un concierto mostrando el sonido de cada instrumento.
"""

from abc import ABC, abstractmethod

class Instrumento(ABC):

    @abstractmethod
    def tocar(self):
        pass


class Guitarra(Instrumento):
    def tocar(self):
        return "Rasgueo de guitarra"


class Piano(Instrumento):
    def tocar(self):
        return "Melodia piano"


class Bateria(Instrumento):
    def tocar(self):
        return "Ritmo de bateria"


def concierto(instrumentos):
    for i in instrumentos:
        print(i.tocar())


Instrumentos = [Guitarra(), Piano(), Bateria()]
concierto(Instrumentos)