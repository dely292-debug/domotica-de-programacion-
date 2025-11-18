from typing import  Dict, Any
class Aire:
     _contador_aires = 0
     _contador_aires = 0
     UMBRAL_MAX = 60
     UMBRAL_MIN = -20
     def __init__(self, nombre_aire : str , estado : bool = True, temperatura : int = 22) :
         # Asignación de ID automático
         Aire._contador_aires += 1
         # Llama al constructor de la clase base, usando temperatura como nivel principal
         super().__init__(nombre_aire, estado, temperatura)
         self._id = f"aire{Aire._contador_aires}"  # Sobrescribe el ID de la base

     # Sobrescribe los métodos de control de intensidad/temperatura (Refactorización b)
     def aumentarIntensidad(self, paso: int = 1):
         """Aumenta la temperatura (Intensidad en el contexto de la base). Lanza ValueError si supera el umbral."""
         nuevo_nivel = self._nivel_principal + paso
         if nuevo_nivel > self.UMBRAL_MAX:
             raise ValueError(
                 f"Error: La temperatura del aire no puede superar {self.UMBRAL_MAX}ºC. Intento: {nuevo_nivel}")
         self._nivel_principal = nuevo_nivel
         print(f"Temperatura de '{self._nombre}' ajustada a {self._nivel_principal} ºC.")

     def disminuirIntensidad(self, paso: int = 1):
         """Disminuye la temperatura (Intensidad en el contexto de la base). Lanza ValueError si supera el umbral."""
         nuevo_nivel = self._nivel_principal - paso
         if nuevo_nivel < self.UMBRAL_MIN:
             raise ValueError(
                 f"Error: La temperatura del aire no puede ser inferior a {self.UMBRAL_MIN}ºC. Intento: {nuevo_nivel}")
         self._nivel_principal = nuevo_nivel
         print(f"Temperatura de '{self._nombre}' ajustada a {self._nivel_principal} ºC.")

     def obtener_estado(self) -> Dict[str, Any]:
         """Imprime el estado completo del aire y lo retorna como un diccionario."""
         diccionario_estado = {
             "nombre": self._nombre,
             "estado": self._estado,
             "temperatura": self._nivel_principal
         }
         estado_str = "Encendido" if self._estado else "Apagado"
         print(f"  Estado de {self._nombre}: {estado_str}, Temperatura: {self._nivel_principal} ºC")
         return diccionario_estado
