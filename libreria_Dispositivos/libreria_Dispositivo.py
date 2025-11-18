
from typing import Dict, Any
from libreria_Dispositivos.libreria_Programador import Programador
class Dispositivo:
    """
    Clase base para todos los dispositivos controlables (Bombilla, Aire, etc.).
    Agrupa funcionalidades y atributos comunes.
    """
    _contador_dispositivos = 0

    def __init__(self, nombre: str, estado: bool = True, nivel_inicial: int = 0):
        Dispositivo._contador_dispositivos += 1
        self._id = f"dispositivo{Dispositivo._contador_dispositivos}"
        self._nombre = nombre
        self._estado = estado
        # Este atributo será usado por las subclases para intensidad o temperatura
        self._nivel_principal = nivel_inicial
        self._programador: Programador = None

    def __str__(self) -> str:
        return f"{self._nombre} ({self._id})"

    # Métodos de control básicos
    def encender(self):
        """Enciende el dispositivo."""
        self._estado = True
        print(f"Dispositivo '{self._nombre}' encendido.")

    def apagar(self):
        """Apaga el dispositivo."""
        self._estado = False
        print(f"Dispositivo '{self._nombre}' apagado.")

    # Métodos de ajuste de intensidad (DEBEN ser implementados/gestionados por subclases)
    def aumentarIntensidad(self, paso: int = 10):
        """Aumenta la intensidad del dispositivo. Debe ser implementado en subclases."""
        raise NotImplementedError("El método aumentarIntensidad debe ser implementado en la subclase.")

    def disminuirIntensidad(self, paso: int = 10):
        """Disminuye la intensidad del dispositivo. Debe ser implementado en subclases."""
        raise NotImplementedError("El método disminuirIntensidad debe ser implementado en la subclase.")

    def obtener_estado(self) -> Dict[str, Any]:
        """Retorna el estado completo del dispositivo."""
        raise NotImplementedError("El método obtener_estado debe ser implementado en la subclase.")

    # Funcionalidad del Programador
    def asignar_programador(self) -> Programador:
        """Asigna o actualiza un objeto Programador a este dispositivo."""
        if self._programador is None:
            self._programador = Programador(self)
            print(f"Programador asignado a '{self}'.")
        else:
            print(f"'{self}' ya tiene un programador asignado.")
        return self._programador

    def comprobar_programacion(self):
        """Comprueba si la hora actual coincide con algún evento programado."""
        if self._programador is None:
            return
        self._programador.ejecutar_programacion()