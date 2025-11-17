from typing import Tuple
from libreria_Dispositivos.libreria_Programador import Programador
"""
 Clase que representa una bombilla con estado (encendida/apagada),
 nivel de intensidad (0-100) y color RGB (tupla de 3 enteros 0-255).
"""

class Bombilla:
    _contador_bombillas = 0
    def __init__(self,nombre_bombilla : str,estado: bool = True, nivel_intensidad: int = 100, color: Tuple[int, int, int] = (255, 255, 255)):
        # Asignación de ID automático
        Bombilla._contador_bombillas += 1
        self._id = f"bombilla{Bombilla._contador_bombillas}"

        self._estado = estado
        self._nivel_intensidad = nivel_intensidad
        self._color = color
        self._nombre_bombilla=nombre_bombilla
        self._programador: Programador = None  # Tipado mejorado

    def __str__(self) :
        return f"{self._nombre_bombilla} ({self._id})"

    # --- Funcionalidad del Programador ---
    def asignar_programador(self) -> Programador:
        """Asigna o actualiza un objeto Programador a esta bombilla."""
        if self._programador is None:
            # Aquí se pasa la INSTANCIA de la bombilla
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



    # Métodos para encender/apagar

    def encender(self) :
        self._estado=True
        print(f"Bombilla '{self._nombre_bombilla}' encendida.")

    def apagar(self):
        self._estado = False
        print(f"Bombilla '{self._nombre_bombilla}' apagada.")

    # Métodos para cambiar intensidad; acepta valor directo o pide por input
    def cambiar_intensidad(self):
        intensidad_valida=False
        while not intensidad_valida:
          comprobacion = input("Introduce nivel de intensidad (0-100): ").strip()
          try:
              nivel_intensidad = int (comprobacion)     #comprobaccion de tipo
          except ValueError:
              print(f"Nivel de intensidad no válido: debe ser entero entre 0 y 100")
              continue                                 #vuelve al inicio del bucle
          if not 0<=nivel_intensidad<=100:
              print("Introduce nivel de intensidad (0-100): ")
              continue                                  #vuelve al inicio del bucle
          self._nivel_intensidad = nivel_intensidad     # si llegamos aqui el valor es valido
          print(f"Brillo de '{self._nombre_bombilla}' ajustado a {self._nivel_intensidad}.")
          intensidad_valida = True

    # Métodos para cambiar color; acepta tupla o pide por input
    def cambiar_color(self):
        print(f"Cambiando color para '{self._nombre_bombilla}':")
        nuevo_color = ()
        color_correcto=True
        while color_correcto:
            try:
                r = int(input("Introduce el valor de R (0-255): "))
                g = int(input("Introduce el valor de G (0-255): "))
                b= int(input("Introduce el valor de B(0-255): "))
                if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                    print("Error: Todos los valores RGB deben estar entre 0 y 255.")
                    color_correcto = False
                nuevo_color = (r, g, b)
                self._color = nuevo_color
                print(f"Color de '{self._nombre_bombilla}' cambiado a RGB: {self._color}")
                color_correcto = False
            except ValueError:
                print("Error: Introduce valores enteros válidos (0-255).")
# Métodos para obtener el estado completo
    def obtener_estado(self):
        """ Imprime el estado completo de la bombilla y lo retorna como un diccionario. """
        diccionario_estado = {
            "nombre": self._nombre_bombilla,
            "estado": self._estado,
            "color": self._color,
            "intensidad": self._nivel_intensidad
        }
        estado_str = "Encendida" if self._estado else "Apagada"
        print(f"  Estado de {self._nombre_bombilla}: {estado_str}, Intensidad: {self._nivel_intensidad}, Color: {self._color}")
        return diccionario_estado
