class Tamagotchi():
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.__edad = edad
        self.__hambre = 100
        self.__sed = 100
        self.__energia = 100
        self.__felicidad = 100
        self.__salud = 100
        self.__limpieza = 100
        self.__vivo = True  
        self.contador_critico = 0

    def __str__(self):
        return f"""
    Estado General de {self.nombre}:
    Edad: {self.__edad}
    Hambre: {self.__hambre}
    Sed: {self.__sed}
    Energía: {self.__energia}
    Felicidad: {self.__felicidad}
    Salud: {self.__salud}
    Limpieza: {self.__limpieza}
    Está vivo? {self.__vivo}
        """

    def comer(self):
        if self.__hambre < 100:
            self.__hambre += 40
            if self.__hambre > 100:
                self.__hambre = 100
        else:
            print(f"{self.nombre} ya comió demasiado!")

    def beber(self):
        if self.__sed < 100:
            self.__sed += 20
            if self.__sed > 100:
                self.__sed = 100
        else:
            print(f"{self.nombre} ya tiene suficiente agua!")

    def jugar(self):
        if self.__felicidad < 100:
            self.__felicidad += 20
            if self.__felicidad > 100:
                self.__felicidad = 100
        else:
            print(f"{self.nombre} ya está muy feliz!")

    def dormir(self):
        if self.__energia < 100:
            self.__energia += 30
            if self.__energia > 100:
                self.__energia = 100
        else:
            print(f"{self.nombre} ya está descansado!")

    def verificar_muerte(self):
        if self.__salud <= 0:
            self.__vivo = False
            print(f"{self.nombre} murió por falta de salud.")
            return

        if self.__hambre >= 100:
            self.__vivo = False
            print(f"{self.nombre} murió de hambre.")
            return

        if self.__sed >= 100:
            self.__vivo = False
            print(f"{self.nombre} murió de sed.")
            return

        criticos = 0

        if self.__hambre >= 90:
            criticos += 1
        if self.__sed >= 90:
            criticos += 1
        if self.__energia <= 10:
            criticos += 1
        if self.__felicidad <= 10:
            criticos += 1
        if self.__limpieza <= 10:
            criticos += 1

        if criticos >= 3:
            self.contador_critico += 1
            if self.contador_critico >= 2:
                self.__vivo = False
                print(f"{self.nombre} murió por estado crítico acumulado.")
                return
        else:
            self.contador_critico = 0

        import random
        if self.__salud < 30:
            if random.randint(1, 100) == 1:
                self.__vivo = False
                print(f"{self.nombre} murió por una enfermedad rara.")
                return