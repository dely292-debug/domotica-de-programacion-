from abc import ABC, abstractmethod
from libreria_Dispositivos.libreria_Programador import Programador


class Dispositivo(ABC):
    """
    Clase base para todos los dispositivos controlables (Bombilla, Aire, etc.).
    Agrupa funcionalidades y atributos comunes.
    """
    _contador_dispositivos = 0

    def __init__(self, nombre, estado=False, nivel_inicial=0):
        Dispositivo._contador_dispositivos += 1
        self._id = f"dispositivo{Dispositivo._contador_dispositivos}"
        self._nombre = nombre
        self._estado = estado
        # Este atributo será usado por las subclases para intensidad o temperatura
        self._nivel_principal = nivel_inicial
        self._programador=None

    def __str__(self):
        return f"{self._nombre} ({self._id})"

    # Métodos de control básicos
    def encender(self):
        """Enciende el dispositivo."""
        self._estado = True


    def apagar(self):
        """Apaga el dispositivo."""
        self._estado = False


    # Métodos de ajuste de intensidad: AHORA SON ABSTRACTOS
    @abstractmethod
    def aumentarIntensidad(self, paso: int = 0):
        """Aumenta la intensidad del dispositivo. Debe ser implementado en subclases."""
        pass

    @abstractmethod
    def disminuirIntensidad(self, paso: int = 10):
        """Disminuye la intensidad del dispositivo. Debe ser implementado en subclases."""
        pass

    @abstractmethod
    def obtener_estado(self):
        """Retorna el estado completo del dispositivo."""
        pass

    # Funcionalidad del Programador
    def asignar_programador(self):
        """Asigna o actualiza un objeto Programador a este dispositivo."""
        if self._programador is None:
            self._programador = Programador(self)
        else:
            print(f"'{self}' ya tiene un programador asignado.")
        return self._programador

    def comprobar_programacion(self):
        """Comprueba si la hora actual coincide con algún evento programado."""
        if self._programador is None:
            return
        self._programador.ejecutar_programacion()