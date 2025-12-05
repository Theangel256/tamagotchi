from typing import Dict, List, Optional, Any

class Inventario:
    """
    Gestiona la lista de items del Tamagotchi.
    
    Permite almacenar, contar y recuperar items, respetando una capacidad máxima.
    Los items se agrupan por nombre para facilitar su gestión (ej. 3 Manzanas ocupan 3 espacios
    pero se acceden bajo la clave "Manzana").
    """

    def __init__(self, capacidad_maxima: int = 10):
        """
        Inicializa un inventario vacío.

        Args:
            capacidad_maxima (int): El número máximo de items que pueden almacenarse.
                                    Por defecto es 10.
        """
        # Diccionario: nombre_item -> lista de objetos item
        self.__items: Dict[str, List[Any]] = {}
        self.__capacidad = capacidad_maxima

    @property
    def items(self) -> Dict[str, List[Any]]:
        """
        Lista de items almacenados.
        
        Returns:
            Dict[str, List[Any]]: Diccionario donde la clave es el nombre del item
                                  y el valor es una lista de instancias de Item.
        """
        return self.__items

    def total_items(self) -> int:
        """
        Calcula la cantidad total de items en el inventario.
        
        Returns:
            int: La suma de todos los items almacenados.
        """
        return sum(len(lst) for lst in self.__items.values())

    def add(self, item):
        """
        Agrega un item al inventario si hay espacio.

        Args:
            item (Item): El objeto Item a agregar.

        Returns:
            str: Mensaje indicando si se agregó o si el inventario está lleno.
        """
        if self.total_items() >= self.__capacidad:
            return "Inventario lleno"
        
        nombre = item.nombre
        self.__items.setdefault(nombre, []).append(item)
        return f"Agregado {nombre}"

    def usar_item(self, nombre) -> Optional[Item]:
        """
        Consume (elimina y devuelve) un item del inventario.

        Args:
            nombre (str): El nombre del item a usar (ej. "Manzana").

        Returns:
            Optional[Item]: La instancia del item si existe, o None si no hay.
                            Si era el último de su tipo, la clave se elimina del diccionario.
        """
        if nombre not in self.__items:
            return None
        lista = self.__items[nombre]
        item = lista.pop(0)
        if not lista:
            del self.__items[nombre]
        return item