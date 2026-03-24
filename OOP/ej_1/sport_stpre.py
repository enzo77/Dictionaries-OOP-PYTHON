class Team:
    """
    Docstring para Team
    Attributes:
        name   (str): Nombre del equipo.
        points (int): Puntos acumulados, empieza en 0.
        
    """
    def __init__(self, name):
        """
        Crea un nuevo equipo con 0 puntos.
        
        Args:
            name (str): Nombre del equipo.
        """
        self.name = name
        self.points = 0
        
    def win_match(self):
        """
        Registra una victoria. Suma 3 puntos al equipo.
        """
        self.points += 3 
    
    def draw_match(self):
        """
        Registra un empate. Suma 1 punto al equipo.
        """
        self.points += 1
    
    def get_points(self):
        """
        Retorna el total de puntos acumulados.
        
        Returns:
            int: Puntos actuales del equipo.
        """
        return self.points
    
t = Team("Tigers")

t.draw_match()
print(t.get_points())