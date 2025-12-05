from typing import Dict

class Item:
    """
    Representa un objeto consumible o utilizable dentro del juego.
    
    Los items pueden tener efectos positivos o negativos sobre las estadísticas
    del Tamagotchi (como hambre, felicidad, salud, etc.).
    """
    
    def __init__(self, nombre: str, tipo: str, efectos: Dict[str, int]):
        """
        Inicializa un nuevo Item.

        Args:
            nombre (str): El nombre identificador del item (ej. "Manzana", "Poción").
            tipo (str): La categoría del item (ej. "comida", "medicina", "juguete").
                        Esto puede usarse para filtrar items o determinar comportamientos específicos.
            efectos (Dict[str, int]): Un diccionario que define cómo afecta este item a las estadísticas.
                                      Las claves deben coincidir con los atributos del Tamagotchi (ej. "hambre", "felicidad").
                                      Los valores positivos aumentan la estadística, los negativos la disminuyen.
                                      Ejemplo: {"hambre": 20, "felicidad": 5} recupera 20 de hambre y 5 de felicidad.
        """
        self.__nombre = nombre
        self.__tipo = tipo
        self.__efectos = efectos

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del item."""
        return self.__nombre

    @property
    def tipo(self) -> str:
        """Devuelve el tipo/categoría del item."""
        return self.__tipo

    @property
    def efectos(self) -> Dict[str, int]:
        """Devuelve el diccionario de efectos del item."""
        return self.__efectos

    def __str__(self):
        """Devuelve una representación legible del item."""
        efectos = ", ".join(f"{k} {v:+}" for k, v in self.__efectos.items())
        return f"{self.__nombre} ({self.__tipo}): {efectos}"