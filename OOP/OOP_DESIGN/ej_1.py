class Employee:
    """
    Representa un empleado con su nombre y salario.

    Attributes:
        name   (str):   Nombre del empleado.
        salary (float): Salario actual del empleado.
    """

    def __init__(self, name, salary):
        
        self.name   = name
        self.salary = salary

    def raise_salary(self, percent):

        if percent <= 0:
            raise ValueError("Percent must be positive")
        self.salary = self.salary * (1 + percent / 100)

    def get_salary(self):

        return self.salary


# Sesión de ejemplo
e = Employee("Laura", 30000)
print(e.get_salary())   

e.raise_salary(10)
print(e.get_salary())  

e.raise_salary(-5)      