
from libreria_Dispositivos.libreria_Bombillas import Bombilla
from libreria_Dispositivos.libreria_Aire_Acondicionado  import Aire
import datetime

class Habitacion:
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

    def guarda_log(self, fichero: str):
        """
        Almacena la fecha actual y el estado de todos los dispositivos
        de la habitación en el fichero especificado.

        Lanza:
            RuntimeError: Si ocurre un error al escribir o procesar el log.
        """
        try:
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Construcción eficiente del contenido
            lineas = [
                f"\n*** LOG HISTÓRICO - {self._tipo_habitacion} ***",
                f"FECHA/HORA: {fecha_actual}",
                "-" * 50
            ]

            # Estado de bombillas
            if self._lista_bombillas:
                lineas.append(f"Bombillas ({len(self._lista_bombillas)}):")
                for b in self._lista_bombillas:
                    estado = b.obtener_estado()
                    lineas.append(
                        f"  - {estado['nombre']} (ID: {b._id}): "
                        f"Estado={'ON' if estado['estado'] else 'OFF'}, "
                        f"Intensidad={estado['intensidad']}, Color={estado['color']}"
                    )
            else:
                lineas.append("Bombillas: Ninguna instalada.")

            # Estado de aires
            if self._lista_aires:
                lineas.append(f"\nAires Acondicionados ({len(self._lista_aires)}):")
                for a in self._lista_aires:
                    estado = a.obtener_estado()
                    lineas.append(
                        f"  - {estado['nombre']} (ID: {a._id}): "
                        f"Estado={'ON' if estado['estado'] else 'OFF'}, "
                        f"Temperatura={estado['temperatura']}ºC"
                    )
            else:
                lineas.append("\nAires Acondicionados: Ninguno instalado.")

            lineas.append("-" * 50 + "\n")

            # Escritura en fichero con UTF-8 para soportar caracteres especiales (º)
            with open(fichero, 'a', encoding='utf-8') as f:
                f.write("\n".join(lineas))

        except (OSError, IOError) as e:
            # Propagamos el error para que la UI decida qué mostrar
            raise RuntimeError(f"Error de acceso al archivo '{fichero}': {e}")
        except Exception as e:
            raise RuntimeError(f"Fallo inesperado al generar log en '{self._tipo_habitacion}': {e}")