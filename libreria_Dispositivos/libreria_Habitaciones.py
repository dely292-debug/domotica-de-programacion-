from libreria_Dispositivos.libreria_Bombillas import Bombilla
from libreria_Dispositivos.libreria_Aire_Acondicionado  import Aire

class Habitacion:
    def __init__(self, tipo_habitacion):
        self._tipo_habitacion=tipo_habitacion
        # lista para almacenar bombillas y aires
        self._lista_bombillas = []
        self._lista_aires = []

    def __str__(self):
        return self._tipo_habitacion

    #Metodos para añadir bombillas
    def agregar_bombilla(self,nombre_bombilla):
        nueva_bombilla = Bombilla(nombre_bombilla)
        self._lista_bombillas.append(nueva_bombilla)
        print(f"Bombilla '{nueva_bombilla}' ha sido añadida a '{self._tipo_habitacion}'.")

    def eliminar_bombilla(self,bombilla_objetivo):
        if bombilla_objetivo in self._lista_bombillas:
         self._lista_bombillas.remove(bombilla_objetivo)
         print(f"Bombilla: {bombilla_objetivo} ha sido eliminada de {self._tipo_habitacion}")
        else:
            print(f"Bombilla: {bombilla_objetivo} no se encuentra en {self._tipo_habitacion}")
    #Metodos para aires
    def agregar_aire(self,nombre_aire):
        nuevo_aire=Aire(nombre_aire)
        self._lista_aires.append(nuevo_aire)
        print(f"Aire:{nuevo_aire} ha sido añadido a {self._tipo_habitacion}")

    def eliminar_aire(self,aire_objetivo):
        if aire_objetivo in self._lista_aires:
         self._lista_aires.remove(aire_objetivo)
        else:
         print(f"Aire : {aire_objetivo}no se encuentra en {self._tipo_habitacion}")

    #Metodos de estado
    def mostrar_estado(self):
        total_bombillas=self._lista_bombillas
        total_aires = self._lista_aires
        total_dispositivos=len(self._lista_bombillas)+len(self._lista_aires)

        # Convertir la lista de objetos a una cadena de nombres separados por comas
        nombres_bombillas = [str(b) for b in total_bombillas]
        nombres_aires = [str(a) for a in total_aires]

        print(f"\n--- 🏠 Estado de la Habitación: {self._tipo_habitacion} ---")
        print(f"Dispositivos totales instalados: {total_dispositivos}\n")

        print("Bombillas")
        if nombres_bombillas:
            print(f"Hay {len(total_bombillas)} bombilla(s): {', '.join(nombres_bombillas)}")
            for b in total_bombillas:
                b.obtener_estado()  # Llama al Metodo de la bombilla
        else:
            print("No hay bombillas instaladas.")

        print("\nAires Acondicionados")
        print(f"{len(total_bombillas)} Bombillas llamadas {', '.join(nombres_bombillas) if nombres_bombillas else 'Ninguna'} . \n{len(total_aires)} Aires llamados{', '.join(nombres_aires) if nombres_aires else 'Ninguno'} .")
        if nombres_aires:
                    print(f"Hay {len(total_aires)} aire(s): {', '.join(nombres_aires)}")
                    for a in total_aires:
                        a.obtener_estado() # Llama al Metodo del aire
        else:
            print("No hay Aires Acondicionados instalados.")