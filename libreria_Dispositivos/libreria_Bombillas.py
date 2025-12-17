from libreria_Dispositivos.libreria_Dispositivo import Dispositivo

"""
 Clase que representa una bombilla con estado (encendida/apagada),
 nivel de intensidad (0-100) y color RGB (tupla de 3 enteros 0-255).
"""

class Bombilla(Dispositivo):
    _contador_bombillas = 0
    UMBRAL_MAX = 100
    UMBRAL_MIN = 0
    def __init__(self,nombre_bombilla : str,estado: bool = True, nivel_intensidad: int = 100, color: tuple = (255, 255, 255)):
        # Asignación de ID automático
        Bombilla._contador_bombillas += 1
        # Llama al constructor de la clase base, usando intensidad como nivel principal
        super().__init__(nombre_bombilla, estado, nivel_intensidad)
        self.tipo_dispositivo = "Bombilla"
        self._id = f"bombilla{Bombilla._contador_bombillas}"# Sobrescribe el ID de la base
        self._color = color
   # Sobrescribe los métodos de control de intensidad
    def aumentarIntensidad(self, paso: int = 0):
        """Aumenta la intensidad. Lanza ValueError si supera el umbral."""
        # Si el valor de paso es 0 (valor por defecto abstracto), se usa 10
        paso_efectivo = paso if paso != 0 else 10
        nuevo_nivel = self._nivel_principal + paso_efectivo
        if nuevo_nivel > self.UMBRAL_MAX:
            raise ValueError(
                f"Error: La intensidad de la bombilla no puede superar {self.UMBRAL_MAX}. Intento: {nuevo_nivel}")
        self._nivel_principal = nuevo_nivel
        print(f"Intensidad de '{self._nombre}' aumentada a {self._nivel_principal}.")

    def disminuirIntensidad(self, paso: int = 0):
        """Disminuye la intensidad. Lanza ValueError si supera el umbral."""
        # Si el valor de paso es 0 (valor por defecto abstracto), se usa 10
        paso_efectivo = paso if paso != 0 else 10
        nuevo_nivel = self._nivel_principal - paso_efectivo
        if nuevo_nivel < self.UMBRAL_MIN:
            raise ValueError(
                f"Error: La intensidad de la bombilla no puede ser inferior a {self.UMBRAL_MIN}. Intento: {nuevo_nivel}")
        self._nivel_principal = nuevo_nivel
        print(f"Intensidad de '{self._nombre}' disminuida a {self._nivel_principal}.")

    # Metodo de ajuste de color (setter no interactivo)
    def set_color(self, r: int, g: int, b: int):
        """Establece el color RGB (0-255)."""
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
             raise ValueError("Error: Todos los valores RGB deben estar entre 0 y 255.")
        self._color = (r, g, b)
        print(f"Color de '{self._nombre}' cambiado a RGB: {self._color}.")

    def obtener_estado(self) :
        """Imprime el estado completo de la bombilla y lo retorna como un diccionario."""
        diccionario_estado = {
            "nombre": self._nombre,
            "estado": self._estado,
            "color": self._color,
            "intensidad": self._nivel_principal
        }
        estado_str = "Encendida" if self._estado else "Apagada"
        print(f"  Estado de {self._nombre}: {estado_str}, Intensidad: {self._nivel_principal}, Color: {self._color}")
        return diccionario_estado


