from src.inventario import Inventario

class Tamagotchi:
    """
    Modelo del Tamagotchi.
    - Atributos encapsulados (0-100)
    - Edad en turnos
    - Evolución por edad
    - Turnos críticos acumulados por atributos en riesgo
    """
    EVOLUTIONS = [
        (0, "Huevo"),
        (5, "Bebé"),
        (18, "Joven"),
        (30, "Adulto"),
        (60, "Anciano")
    ]
    def __init__(self, nombre: str, edad: int = 0):
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

        # Contadores de turnos críticos para muerte por acumulación
        self.__turnos_criticos = 0
        self.__edad_counter = 0

        self.inventario = Inventario(10)

        self.params = {
            "edad": 1,
            "turnos_para_envejecer": 10,
            "critico_threshold": 10,
            "turnos_criticos_para_muerte": 3,
        }

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
        """
        Método privado para aplicar efectos sobre atributos.
        Acepta llaves: 'hambre','sed','energia','felicidad','salud','limpieza'
        """
        if not self.__vivo:
            return
            
        mapping = {
            "hambre": "__hambre",
            "sed": "__sed",
            "energia": "__energia",
            "felicidad": "__felicidad",
            "salud": "__salud",
            "limpieza": "__limpieza"
        }
        for atributo, valor in efectos.items():
            interno = f"_Tamagotchi{mapping[atributo]}"
            # accede dinamicamente a el atributo privado
            actual = getattr(self, interno)
            # modifica el atributo privado
            setattr(self, interno, self._clamp(actual + valor))
            
    def _forzar_muerte(self, razon: str = "Sin descripción"):
        self.__vivo = False
        print(f"[Muerte] {self.__nombre}: {razon}")

    # Estados
    @property
    def estado_general(self) -> str:
        promedio = (self.__hambre + self.__sed + self.__salud + self.__energia) / 4
        if promedio >= 85: return "Excelente"
        if promedio >= 60: return "Bueno"
        if promedio >= 30: return "Regular"
        return "Crítico"
    @property
    def estado_emocional(self) -> str:
        score = (self.__felicidad + self.__energia) / 2
        if score >= 80: return "Eufórico"
        if score >= 50: return "Contento"
        if score >= 30: return "Cansado"
        return "Deprimido"
    @property
    def riesgo_de_muerte(self) -> str:
        crit = 0
        for v in (self.__hambre, self.__sed, self.__salud):
            if v < 20: crit += 1
        if crit >= 2: return "Alto"
        if crit == 1: return "Medio"
        return "Bajo"
    @property
    def evolucion(self) -> str:
        # Determinar etapa según edad
        etapa = "Unknown"
        for i, nombre in reversed(self.EVOLUTIONS):
            if self.__edad >= i:
                etapa = nombre
                break
        return etapa
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

    def usar_item(self, nombre: str):
        item = self.inventario.usar_item(nombre)
        if not item: return
        self._aplicar_efectos(item.efectos)
        return f"Usado {item.nombre}"

    # Deterioro por turnos, se llama cada vez que se actualiza el juego
    def deterioro_por_turno(self):
        # Deterioro reducido
        self._aplicar_efectos({
            "hambre": -1,
            "sed": -2,
            "felicidad": -1,
            "energia": -1,
            "limpieza": -1
        })

        if self.__hambre < 20 or self.__sed < 20 or self.__limpieza < 20:
            self._aplicar_efectos({"salud": -3})
            
    def actualizar_edad(self):
        # Envejecer cada 10 turnos (días)
        turnos_para_envejecer = self.params.get("turnos_para_envejecer", 10)
        self.__edad_counter += 1
        if self.__edad_counter >= turnos_para_envejecer:
            self.__edad += self.params.get("edad", 1)
            self.__edad_counter = 0

    def _chequear_criticos_acumulados(self):
        """
        Incrementa contador de turnos críticos si 3 o más atributos están en zona crítica.
        Devuelve True si supera el umbral para morir por acumulación.
        """
        criticos = 0
        threshold = self.params.get("critico_threshold", 10)
        for v in (self.__hambre, self.__sed, self.__salud, self.__energia, self.__felicidad, self.__limpieza):
            if v <= threshold:
                criticos += 1
        if criticos >= 3:
            self.__turnos_criticos += 1
        else:
            # se recupera lentamente si no está en crítico
            self.__turnos_criticos = max(0, self.__turnos_criticos - 1)
        return self.__turnos_criticos >= self.params.get("turnos_criticos_para_muerte", 3)
    
    def tick(self):
        """Paso de tiempo: deterioro, edad y verificar muerte básica."""
        if not self.__vivo:
            return

        self.deterioro_por_turno()
        self.actualizar_edad()

        # Muerte inmediata por 0 en atributos vitales
        if self.__hambre == 0 or self.__sed == 0 or self.__salud == 0:
            self._forzar_muerte("Falleció por valor vital en 0")
            return

        # Muerte por acumulación de turnos críticos
        if self._chequear_criticos_acumulados():
            self._forzar_muerte("Falleció por condiciones críticas acumuladas")
    # --------------------
    # Mostrar estado (para debugging/UI)
    # --------------------
    def mostrar_estado_detallado(self) -> str:
        return (
            f"Nombre: {self.__nombre}\n"
            f"Edad: {self.__edad}\n"
            f"Evolución: {self.evolucion}\n"
            f"Hambre: {self.__hambre}\n"
            f"Sed: {self.__sed}\n"
            f"Energía: {self.__energia}\n"
            f"Felicidad: {self.__felicidad}\n"
            f"Salud: {self.__salud}\n"
            f"Limpieza: {self.__limpieza}\n"
            f"Estado general: {self.estado_general}\n"
            f"Estado emocional: {self.estado_emocional}\n"
            f"Riesgo muerte: {self.riesgo_de_muerte}\n"
            f"Vivo: {self.__vivo}\n"
        )