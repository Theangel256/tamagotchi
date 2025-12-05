from src.inventario import Inventario

class Tamagotchi:
    def __init__(self, nombre, edad):
        self.__nombre = nombre
        self.__edad = edad

        # Atributos base
        self.__hambre = 100
        self.__sed = 100
        self.__energia = 100
        self.__felicidad = 100
        self.__salud = 100
        self.__limpieza = 100
        self.__vivo = True

        self.inventario = Inventario(10)

    # Atributos
    @property
    def nombre(self): return self.__nombre
    @property
    def edad(self): return self.__edad
    @property
    def hambre(self): return self.__hambre
    @property
    def sed(self): return self.__sed
    @property
    def energia(self): return self.__energia
    @property
    def felicidad(self): return self.__felicidad
    @property
    def salud(self): return self.__salud
    @property
    def limpieza(self): return self.__limpieza
    @property
    def vivo(self): return self.__vivo

    # Métodos internos
    def _clamp(self, v): return max(0, min(100, v))

    def _aplicar_efectos(self, efectos):
        for atributo, valor in efectos.items():
            interno = f"_Tamagotchi__{atributo}"
            if hasattr(self, interno):
                actual = getattr(self, interno)
                setattr(self, interno, self._clamp(actual + valor))

    def _forzar_muerte(self, razon):
        print("⚠", razon)
        self.__vivo = False

    # Acciones
    def comer(self):
        self._aplicar_efectos({"hambre": +40, "limpieza": -5})

    def beber(self):
        self._aplicar_efectos({"sed": +30, "limpieza": -5})

    def jugar(self):
        self._aplicar_efectos({"felicidad": +20, "energia": -10, "hambre": -10, "sed": -10})

    def dormir(self):
        self._aplicar_efectos({"energia": +100, "hambre": -10, "sed": -10})

    def banarse(self):
        self._aplicar_efectos({"limpieza": +100})

    def curar(self):
        self._aplicar_efectos({"salud": +40})

    def usar_item(self, nombre):
        item = self.inventario.usar_item(nombre)
        if not item: return
        self._aplicar_efectos(item.efectos)

    # Deterioro por turnos, se llama cada vez que se actualiza el juego
    def deterioro_por_turno(self):
        self._aplicar_efectos({
            "hambre": -2,
            "sed": -3,
            "felicidad": -1,
            "energia": -1,
            "limpieza": -1
        })

        if self.__hambre < 20 or self.__sed < 20 or self.__limpieza < 20:
            self._aplicar_efectos({"salud": -2})

    # Actualización del juego
    def tick(self):
        if not self.__vivo: return
        self.deterioro_por_turno()
        if self.__hambre == 0 or self.__sed == 0 or self.__salud == 0:
            self._forzar_muerte("Muerte por estado vital")
