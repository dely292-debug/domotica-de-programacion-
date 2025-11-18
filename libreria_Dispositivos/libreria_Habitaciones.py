from libreria_Dispositivos.libreria_Bombillas import Bombilla
from libreria_Dispositivos.libreria_Aire_Acondicionado  import Aire
from typing import List
class Habitacion:
    """Contenedor para dispositivos (Bombillas y Aires)."""
    def __init__(self, tipo_habitacion):
        self._tipo_habitacion = tipo_habitacion
        self._lista_bombillas: List[Bombilla] = []
        self._lista_aires: List[Aire] = []

    def __str__(self):
        return self._tipo_habitacion

    def agregar_bombilla(self, nombre_bombilla):
        nueva_bombilla = Bombilla(nombre_bombilla)
        self._lista_bombillas.append(nueva_bombilla)
        print(f"Bombilla '{nueva_bombilla}' ha sido añadida a '{self._tipo_habitacion}'.")

    def eliminar_bombilla(self, bombilla_objetivo):
        if bombilla_objetivo in self._lista_bombillas:
            self._lista_bombillas.remove(bombilla_objetivo)
            print(f"Bombilla: {bombilla_objetivo} ha sido eliminada de {self._tipo_habitacion}")
        else:
            print(f"Bombilla: {bombilla_objetivo} no se encuentra en {self._tipo_habitacion}")

    def agregar_aire(self, nombre_aire):
        nuevo_aire = Aire(nombre_aire)
        self._lista_aires.append(nuevo_aire)
        print(f"Aire:{nuevo_aire} ha sido añadido a {self._tipo_habitacion}")

    def eliminar_aire(self, aire_objetivo):
        if aire_objetivo in self._lista_aires:
            self._lista_aires.remove(aire_objetivo)
            print(f"Aire: {aire_objetivo} ha sido eliminado de {self._tipo_habitacion}")
        else:
            print(f"Aire : {aire_objetivo} no se encuentra en {self._tipo_habitacion}")

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