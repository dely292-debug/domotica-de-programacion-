
from libreria_Dispositivos.libreria_Bombillas import Bombilla
from libreria_Dispositivos.libreria_Aire_Acondicionado  import Aire
from libreria_Dispositivos.libreria_Log_Historico import ILogHistorico
import datetime

class Habitacion(ILogHistorico): # Ahora hereda de ILogHistorico
    """Contenedor para dispositivos (Bombillas y Aires)."""
    def __init__(self, tipo_habitacion):
        self._tipo_habitacion = tipo_habitacion
        self._lista_bombillas = []
        self._lista_aires= []

    def __str__(self):
        return self._tipo_habitacion

    def agregar_bombilla(self, nombre_bombilla):
        nueva_bombilla = Bombilla(nombre_bombilla)
        self._lista_bombillas.append(nueva_bombilla)
        print(f"Bombilla '{nueva_bombilla}' ha sido añadida a '{self._tipo_habitacion}'.")


    def eliminar_bombilla(self, nombre):
        for b in self._lista_bombillas:
            if b._nombre == nombre:
                self._lista_bombillas.remove(b)
                return True
        return False

    def agregar_aire(self, nombre_aire):
        nuevo_aire = Aire(nombre_aire)
        self._lista_aires.append(nuevo_aire)
        print(f"Aire:{nuevo_aire} ha sido añadido a {self._tipo_habitacion}")


    def eliminar_aire(self, nombre):
        for aire in self._lista_aires:
            if aire._nombre == nombre:
                self._lista_aires.remove(aire)
                return True
        return False

    def mostrar_estado(self):
        total_bombillas = self._lista_bombillas
        total_aires = self._lista_aires
        total_dispositivos = len(total_bombillas) + len(total_aires)

        nombres_bombillas = [str(b) for b in total_bombillas]
        nombres_aires = [str(a) for a in total_aires]

        print(f"\n Estado de la Habitación: {self._tipo_habitacion} ---")
        print(f"Dispositivos totales instalados: {total_dispositivos}")

        print("\n--- Bombillas ---")
        if nombres_bombillas:
            print(f"Hay {len(total_bombillas)} bombilla(s): {', '.join(nombres_bombillas)}")
            for b in total_bombillas:
                b.obtener_estado()
        else:
            print("No hay bombillas instaladas.")

        print("\n--- Aires Acondicionados ---")
        if nombres_aires:
            print(f"Hay {len(total_aires)} aire(s): {', '.join(nombres_aires)}")
            for a in total_aires:
                a.obtener_estado()
        else:
            print("No hay Aires Acondicionados instalados.")

    def guardaLog(self, fichero: str):
        """
        Almacena la fecha actual y el estado de todos los dispositivos
        de la habitación en el fichero especificado.
        """
        try:
            # Obtener la fecha y hora actual
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Crear el contenido del log
            contenido = f"\n*** LOG HISTÓRICO - {self._tipo_habitacion} ***\n"
            contenido += f"FECHA/HORA: {fecha_actual}\n"
            contenido += "-" * 50 + "\n"

            # Recopilar estado de bombillas
            if self._lista_bombillas:
                contenido += f"Bombillas ({len(self._lista_bombillas)}):\n"
                for b in self._lista_bombillas:
                    estado = b.obtener_estado()
                    contenido += f"  - {estado['nombre']} (ID: {b._id}): Estado={'ON' if estado['estado'] else 'OFF'}, Intensidad={estado['intensidad']}, Color={estado['color']}\n"
            else:
                contenido += "Bombillas: Ninguna instalada.\n"

            # Recopilar estado de aires
            if self._lista_aires:
                contenido += f"\nAires Acondicionados ({len(self._lista_aires)}):\n"
                for a in self._lista_aires:
                    estado = a.obtener_estado()
                    contenido += f"  - {estado['nombre']} (ID: {a._id}): Estado={'ON' if estado['estado'] else 'OFF'}, Temperatura={estado['temperatura']}ºC\n"
            else:
                contenido += "\nAires Acondicionados: Ninguno instalado.\n"

            # Escribir en el fichero (modo 'a' para append)
            with open(fichero, 'a') as f:
                f.write(contenido)
                f.write("-" * 50 + "\n")

            print(f" [LOG] Estado de '{self._tipo_habitacion}' guardado con éxito en '{fichero}'.")

        except Exception as e:
            print(f" [LOG ERROR] Error al guardar el log de '{self._tipo_habitacion}': {e}")