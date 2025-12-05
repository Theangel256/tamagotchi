import random
from typing import Optional
from src.item import Item
from src.tamagotchi import Tamagotchi

class Game:
    """
    Controlador: maneja ticks, eventos aleatorios, skip turn, y reglas adicionales.
    """

    def __init__(self, tamagotchi: Tamagotchi):
        self.tama = tamagotchi
        self.turno = 0
        self.ultimo_evento: Optional[str] = None

        # Definir eventos: lista de (probabilidad, función, mensaje)
        # Probabilidades expresadas como 0.0-1.0 por turno.
        self.eventos = [
            (0.06, self._evento_calor, "Hace calor: sed +10, energía -5"),
            (0.04, self._evento_enfermar, "Se enfermó: salud -20"),
            (0.03, self._evento_encontrar_item, "Encontró una manzana"),
            (0.02, self._evento_visita, "Visita inesperada: felicidad +30"),
            (0.015, self._evento_lesion_juego, "Se lastimó jugando: salud -10, felicidad +20"),
        ]

    # --------------------
    # Metodos publicos
    # --------------------
    def avanzar_turno(self) -> str:
        """Avanza un turno del juego y devuelve mensaje de evento (si ocurre)."""
        if not self.tama.vivo:
            self.ultimo_evento = "El tamagotchi está muerto."
            return self.ultimo_evento

        self.turno += 1
        # acción principal del turno
        self.tama.tick()

        # Eventos aleatorios
        evento_msg = self._procesar_eventos_aleatorios()

        # Muerte aleatoria rara: 1% si salud < 15
        if self.tama.salud < 15 and random.random() < 0.01:
            self.tama._forzar_muerte("Evento raro: muerte súbita por salud crítica")
            evento_msg = "Muerte súbita rara."

        self.ultimo_evento = evento_msg or "Turno normal"
        return self.ultimo_evento

    def saltar_turno(self) -> str:
        """Permite al jugador saltar un turno (mismo efecto que avanzar_turno)."""
        return self.avanzar_turno()

    # --------------------
    # Eventos
    # --------------------
    def _procesar_eventos_aleatorios(self) -> str | None:
        mensajes = []
        for prob, func, msg in self.eventos:
            if random.random() <= prob:
                func()
                mensajes.append(msg)
        return "; ".join(mensajes) if mensajes else None

    def _evento_calor(self):
        self.tama._aplicar_efectos({"sed": -10, "energia": -5})

    def _evento_enfermar(self):
        self.tama._aplicar_efectos({"salud": -20})

    def _evento_encontrar_item(self):
        item = Item("Manzana", "comida", {"hambre": 20, "felicidad": 5})
        self.tama.inventario.add(item)

    def _evento_visita(self):
        self.tama._aplicar_efectos({"felicidad": +30})

    def _evento_lesion_juego(self):
        self.tama._aplicar_efectos({"salud": -10, "felicidad": +20})
