from libreria_Dispositivos.libreria_Programador import Programador
class Aire:
     _contador_aires = 0
     def __init__(self, nombre_aire : str , estado : bool = True, temperatura : int = 22) :
         # Asignación de ID automático
         Aire._contador_aires += 1
         self._id = f"aire{Aire._contador_aires}"

         self._estado=estado
         self._temperatura=temperatura
         self._nombre_aire=nombre_aire
         self._programador: Programador = None  # Tipado mejorado

     def __str__(self):
         # Retorna el nombre del aire para que se imprima correctamente
         return f"{self._nombre_aire} ({self._id})"

     # --- Funcionalidad del Programador ---
     def asignar_programador(self) -> Programador:
         """Asigna o actualiza un objeto Programador a este Aire."""
         if self._programador is None:
             # Aquí se pasa la INSTANCIA del aire
             self._programador = Programador(self)
             print(f"Programador asignado a '{self}'.")
         else:
             print(f"'{self}' ya tiene un programador asignado.")
         return self._programado

     def comprobar_programacion(self):
         """Comprueba si la hora actual coincide con algún evento programado."""
         if self._programador is None:
             return
         self._programador.ejecutar_programacion()

      #Metodos para enceder/apagar aire
     def encender (self):
         self._estado=True
         print(f"Aire '{self._nombre_aire}' encendido.")

     def apagar(self):
         self._estado = False
         print(f"Aire '{self._nombre_aire}' apagado.")

      #Metodo para cambiar temperatura
     def cambiar_temperatura(self) :
         temperatura_valida = False
         while not temperatura_valida :
           comprobacion = input("Introduce nivel de temperatura [-20,+60]: ").strip()
           try:
             temperatura = int(comprobacion)      #comprobaccion de tipo
           except ValueError:
             print("el valor introducido debe ser un entero entre [-20+60] :")
             continue                             #vuelve al inicio del bucle
           if not -20 <= temperatura <= 60 :      #comprobacion de valor
             print ("el nivel ajustado esta fuera de rango[-20+60] : " )
             continue                             #vuelve al inicio del bucle
                                                  #si llegamos aqui el valor es valido
           self._temperatura=temperatura
           print(f"El nivel de temperatura de '{self._nombre_aire}' ha sido ajustado a {self._temperatura} ºC.")
           temperatura_valida = True

    # Metodo para leer temperatura
     def lectura_temperatura(self):
         print(f"La temperatura consigna de '{self._nombre_aire}' es {self._temperatura} ºC.")

    # Metodo para leer estado

     def obtener_estado(self):
         """ Imprime el estado completo del aire y lo retorna como un diccionario. """
         diccionario_estado = {
             "nombre": self._nombre_aire,
             "estado": self._estado,
             "temperatura": self._temperatura
         }
         estado_str = "Encendido" if self._estado else "Apagado"
         print(f"  Estado de {self._nombre_aire}: {estado_str}, Temperatura: {self._temperatura} ºC")
         return diccionario_estado