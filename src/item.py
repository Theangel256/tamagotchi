class Item:
    def __init__(self, nombre, tipo, efectos):
        self.__nombre = nombre
        self.__tipo = tipo
        self.__efectos = efectos

    @property
    def nombre(self): return self.__nombre
    @property
    def tipo(self): return self.__tipo
    @property
    def efectos(self): return self.__efectos

    def __str__(self): 
        efectos = ", ".join(f"{k} {v:+}" for k,v in self.__efectos.items())
        return f"{self.__nombre} ({self.__tipo}): {efectos}"