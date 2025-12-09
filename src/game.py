import random
from typing import Optional
from item import Item
from tamagotchi import Tamagotchi

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
            (0.03, self._evento_juguete_viejo, "Encontró un juguete viejo: felicidad +15"),
            (0.05, self._evento_dia_soleado, "Día soleado: felicidad +10"),
            (0.05, self._evento_lluvia, "Lluvia: felicidad -10"),
        ]

    # --------------------
    # Metodos publicos (Acciones del Jugador)
    # --------------------
    def comer(self):
        # 10% probabilidad de comida en mal estado
        if random.random() < 0.10:
            self.tama._aplicar_efectos({"salud": -10, "hambre": +20})
            self.ultimo_evento = "¡Comida en mal estado! (Salud -10)"
        else:
            self.tama.comer()

    def dormir(self):
        # 15% probabilidad de pesadilla
        if random.random() < 0.15:
            self.tama._aplicar_efectos({"energia": +50, "felicidad": -20})
            self.ultimo_evento = "¡Tuvo una pesadilla! (No descansó bien)"
        else:
            self.tama.dormir()

    def beber(self): self.tama.beber()
    def jugar(self): self.tama.jugar()
    def banarse(self): self.tama.banarse()
    def curar(self): self.tama.curar()

    # --------------------
    # Control de Turnos
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
        
        # Si hubo un evento específico por acción (ej. pesadilla), lo priorizamos o combinamos
        if self.ultimo_evento and self.ultimo_evento not in ["Turno normal", "El tamagotchi está muerto."]:
             if evento_msg:
                 evento_msg = f"{self.ultimo_evento} | {evento_msg}"
             else:
                 evento_msg = self.ultimo_evento
        
        # Resetear ultimo evento de acción para el siguiente
        self.ultimo_evento = None

        # Muerte aleatoria rara: 1% si salud < 15
        if self.tama.salud < 15 and random.random() < 0.01:
            self.tama._forzar_muerte("Evento raro: muerte súbita por salud crítica")
            evento_msg = "Muerte súbita rara."

        # Generar mensaje final
        dia_msg = f"Día {self.turno}"
        final_msg = f"{dia_msg}: {evento_msg}" if evento_msg else f"{dia_msg}: Todo tranquilo."

        # Agregar hints de estado
        hints = []
        if self.tama.energia < 20: hints.append("¡Necesita dormir!")
        if self.tama.hambre < 20: hints.append("¡Tiene hambre!")
        if self.tama.sed < 20: hints.append("¡Tiene sed!")
        if self.tama.felicidad < 20: hints.append("¡Está triste!")
        if self.tama.salud < 20: hints.append("¡Se siente mal!")
        
        if hints:
            final_msg += " " + " ".join(hints)

        return final_msg

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

    def _evento_juguete_viejo(self):
        self.tama._aplicar_efectos({"felicidad": +15})

    def _evento_dia_soleado(self):
        self.tama._aplicar_efectos({"felicidad": +10})

    def _evento_lluvia(self):
        self.tama._aplicar_efectos({"felicidad": -10})
