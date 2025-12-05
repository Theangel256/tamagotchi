import random
import src.item import Item

class Game:
    """
    Controlador del juego.
    Maneja turnos, deterioro, eventos y muerte.
    """

    def __init__(self, tamagotchi):
        self.tama = tamagotchi
        self.turno = 0

    def avanzar_turno(self):
        """Avanza un turno del juego."""
        if not self.tama.vivo:
            return

        self.turno += 1
        self.tama.tick()
        self._eventos_aleatorios()
        self._verificar_muerte_extendida()

    def _eventos_aleatorios(self):
        """Ejecuta eventos aleatorios de baja probabilidad."""
        eventos = [
            (0.05, self._evento_calor),
            (0.03, self._evento_enfermar),
            (0.02, self._evento_encontrar_fruta)
        ]

        for prob, evento in eventos:
            if random.random() <= prob:
                evento()

    def _evento_calor(self):
        self.tama._aplicar_efectos({"sed": -10, "energia": -5})

    def _evento_enfermar(self):
        self.tama._aplicar_efectos({"salud": -20})

    def _evento_encontrar_fruta(self):
        self.tama.inventario.add(Item("Manzana", "comida", {"hambre": 20, "felicidad": 5}))

    def _verificar_muerte_extendida(self):
        """Reglas de muerte más completas."""
        criticos = 0
        if self.tama.hambre < 10: criticos += 1
        if self.tama.sed < 10: criticos += 1
        if self.tama.salud < 10: criticos += 1

        # Muerte por acumulación
        if criticos >= 3:
            self.tama._forzar_muerte("Muerte por estado crítico acumulado")

        # Muerte aleatoria (17%) si tiene salud muy baja
        if self.tama.salud < 20 and random.random() < 0.17:
            self.tama._forzar_muerte("Muerte súbita por salud crítica")
