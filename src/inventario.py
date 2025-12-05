class Inventario:
    def __init__(self, capacidad_maxima=10):
        self.__items = {}
        self.__capacidad = capacidad_maxima

    @property
    def items(self): return self.__items

    def total_items(self):
        return sum(len(lst) for lst in self.__items.values())

    def add(self, item):
        if self.total_items() >= self.__capacidad:
            return "Inventario lleno"
        
        nombre = item.nombre
        self.__items.setdefault(nombre, []).append(item)
        return f"Agregado {nombre}"

    def usar_item(self, nombre):
        if nombre not in self.__items:
            return None
        lista = self.__items[nombre]
        item = lista.pop(0)
        if not lista:
            del self.__items[nombre]
        return item