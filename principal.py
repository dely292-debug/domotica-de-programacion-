from libreria_Dispositivos.libreria_Habitaciones import Habitacion
from libreria_Dispositivos.libreria_Aire_Acondicionado import Aire
from libreria_Dispositivos.libreria_Bombillas import Bombilla
from libreria_Dispositivos.libreria_Programador import Programador
import pickle
import os
from typing import Tuple, List, Dict, Any
NOMBRE_ARCHIVO_DATOS = 'habitaciones_data.pkl'

def guardar_habitaciones(lista_habitaciones: List[Habitacion]):
    """Guarda la lista de habitaciones en un archivo usando pickle."""

    try:
        with open(NOMBRE_ARCHIVO_DATOS, 'wb') as f:
            pickle.dump(lista_habitaciones, f)
        print(f"\n Datos guardados en '{NOMBRE_ARCHIVO_DATOS}'.")
    except Exception as e:
        print(f"\n Error al guardar los datos: {e}")


def cargar_habitaciones() -> List[Habitacion]:
    """Carga la lista de habitaciones desde un archivo usando pickle."""
    if os.path.exists(NOMBRE_ARCHIVO_DATOS):
        try:
            with open(NOMBRE_ARCHIVO_DATOS, 'rb') as f:
                lista_habitaciones = pickle.load(f)
            print(f"\n Datos cargados de '{NOMBRE_ARCHIVO_DATOS}' con {len(lista_habitaciones)} habitaciones.")
            return lista_habitaciones
        except Exception as e:
            print(f"\n Error al cargar los datos. Se iniciará con una lista vacía: {e}")
            return []
    else:
        print("\nNo se encontró archivo de datos. Iniciando con lista de habitaciones vacía.")
        return []


def mostrar_menu():
    """Muestra las opciones del menú."""
    print("\n" + "=" * 40)
    print("      **Menú de Gestión Domótica** ")
    print("=" * 40)
    print("1. Crear habitación")
    print("2. Añadir dispositivo")
    print("3. Quitar dispositivo")
    print("4. Mostrar estado de habitación")
    print("5. Listar todas las habitaciones")
    print("6. Mostrar dispositivos por habitaciones")
    print("7. Gestionar Programador (Bombilla/Aire)")
    print("8. **Gestionar Estado y Nivel (INTENSIDAD/TEMP)**")  # Nuevo punto de gestión
    print("9. Salir (Guardar Datos)")


def seleccionar_habitacion(lista_habitaciones, accion="gestionar"):
    """Función auxiliar para seleccionar una habitación existente."""
    if not lista_habitaciones:
        print(" No hay habitaciones creadas. Por favor, cree una primero.")
        return None
    print("\n--- Habitaciones disponibles ---")
    for i, nombre_instancia in enumerate(lista_habitaciones):
        print(f"{i}.- {nombre_instancia._tipo_habitacion} ")

    while True:
        seleccion = input(f"\n Seleccione el número o nombre de la habitación a {accion}: ").strip()

        if seleccion.isdigit():
            indice = int(seleccion)
            if 0 <= indice < len(lista_habitaciones):
                return lista_habitaciones[indice]
            else:
                print(f"Número de habitación no válido.El numero debe estar entre 0 y {len(lista_habitaciones) - 1}")
        else:
            habitacion_encontrada = next((h for h in lista_habitaciones if h._tipo_habitacion == seleccion), None)
            if habitacion_encontrada:
                return habitacion_encontrada
            else:
                print(" Nombre o número de habitación no encontrado.")

        if seleccion.lower() == 'cancelar':
            return None


def anadir_dispositivo(lista_habitaciones):
    """Opción 2: Añade un dispositivo a una habitación."""
    habitacion_seleccionada = seleccionar_habitacion(lista_habitaciones, "añadir un dispositivo")

    if habitacion_seleccionada is None:
        return

    print(f"\nVa añadir un dispositivo a la habitacion **{habitacion_seleccionada._tipo_habitacion}**.")
    print("\n--- Tipos de Dispositivo ---")
    print("1. Bombilla")
    print("2. Aire Acondicionado")
    print("----------------------------")
    opcion_disp = input(" Seleccione el tipo (1 o 2): ").strip()
    nombre_disp = input(" Ingrese el nombre del dispositivo: ").strip()

    if not nombre_disp:
        print(" El nombre del dispositivo no puede estar vacío.")
        return

    if opcion_disp == '1':
        habitacion_seleccionada.agregar_bombilla(nombre_disp)
    elif opcion_disp == '2':
        habitacion_seleccionada.agregar_aire(nombre_disp)
    else:
        print(" Opción de dispositivo no válida.")


def seleccionar_dispositivo(habitacion_seleccionada: Habitacion, tipo_disp: str, accion: str):
    """Función auxiliar para seleccionar un dispositivo de una habitación."""
    if tipo_disp == '1':
        lista_dispositivos = habitacion_seleccionada._lista_bombillas
        tipo_disp_nombre = "bombilla"
    elif tipo_disp == '2':
        lista_dispositivos = habitacion_seleccionada._lista_aires
        tipo_disp_nombre = "aire acondicionado"
    else:
        print("Opción de dispositivo no válida.")
        return None, None

    if not lista_dispositivos:
        print(f"No hay {tipo_disp_nombre}s en {habitacion_seleccionada._tipo_habitacion} para {accion}. ")
        return None, None

    print(f"\n {tipo_disp_nombre.capitalize()}s disponibles:")
    for i, dispositivo in enumerate(lista_dispositivos):
        print(f"{i}.- {dispositivo}")

    while True:
        seleccion = input(f"Seleccione el **número** del {tipo_disp_nombre}: ").strip()
        if seleccion.isdigit():
            try:
                indice = int(seleccion)
                if 0 <= indice < len(lista_dispositivos):
                    return lista_dispositivos[indice], tipo_disp_nombre
                else:
                    print(f"Número fuera de rango [0-{len(lista_dispositivos) - 1}].")
            except ValueError:
                print("Entrada no válida. Por favor, introduzca un número.")
        else:
            print("Entrada no válida. Por favor, introduzca un número.")


def gestionar_estado_dispositivo(lista_habitaciones):
    """Opción 8: Permite encender, apagar, y ajustar nivel/temperatura (con manejo de errores)."""

    habitacion_seleccionada = seleccionar_habitacion(lista_habitaciones, "gestionar dispositivos")
    if habitacion_seleccionada is None: return

    print(f"\n--- Gestión de Dispositivos en **{habitacion_seleccionada._tipo_habitacion}** ---")
    print("1. Bombilla")
    print("2. Aire Acondicionado")
    opcion_disp = input("Seleccione el tipo de dispositivo (1/2): ").strip()

    dispositivo_obj, tipo_disp_nombre = seleccionar_dispositivo(
        habitacion_seleccionada, opcion_disp, "gestionar su estado"
    )
    if dispositivo_obj is None: return

    while True:
        print(f"\n*** Dispositivo: **{dispositivo_obj}** ***")
        dispositivo_obj.obtener_estado()
        print("\nOpciones de gestión:")
        print("a. Encender")
        print("b. Apagar")
        if isinstance(dispositivo_obj, Bombilla):
            print("c. Subir Intensidad")
            print("d. Bajar Intensidad")
            print("e. Cambiar Color (RGB)")
        elif isinstance(dispositivo_obj, Aire):
            print("c. Subir Temperatura")
            print("d. Bajar Temperatura")
        print("z. Volver al menú principal")

        opcion = input("Seleccione una opción (a-z): ").strip().lower()

        if opcion == 'z':
            break

        if opcion == 'a':
            dispositivo_obj.encender()
        elif opcion == 'b':
            dispositivo_obj.apagar()
        elif opcion == 'c':
            paso = 10 if isinstance(dispositivo_obj, Bombilla) else 1
            try:
                paso = int(input(f"Introduce el paso para aumentar ({paso}): ") or paso)
                dispositivo_obj.aumentarIntensidad(paso)
            except ValueError as e:  # Captura el error de umbral (Refactorización c)
                print(f" Operación fallida: {e}")
            except Exception as e:
                print(f"Error de entrada: {e}")
        elif opcion == 'd':
            paso = 10 if isinstance(dispositivo_obj, Bombilla) else 1
            try:
                paso = int(input(f"Introduce el paso para disminuir ({paso}): ") or paso)
                dispositivo_obj.disminuirIntensidad(paso)
            except ValueError as e:  # Captura el error de umbral (Refactorización c)
                print(f" Operación fallida: {e}")
            except Exception as e:
                print(f" Error de entrada: {e}")
        elif opcion == 'e' and isinstance(dispositivo_obj, Bombilla):
            try:
                print("\n--- Ajuste de Color RGB ---")
                r = int(input("Introduce el valor de R (0-255): "))
                g = int(input("Introduce el valor de G (0-255): "))
                b = int(input("Introduce el valor de B (0-255): "))
                dispositivo_obj.set_color(r, g, b)
            except ValueError as e:
                print(f" Error de entrada: {e}. Asegúrese de usar números enteros entre 0 y 255.")
            except Exception as e:
                print(f" Error general: {e}")
        else:
            print("Opción no válida para este dispositivo.")


def crear_habitacion(lista_habitaciones):
    """Opción 1: Crea una nueva instancia de Habitacion."""
    nombre = input("️\n Ingrese el nombre de la habitación a crear: ").strip()
    if any(h._tipo_habitacion == nombre for h in lista_habitaciones):
        print(f" Error: Ya existe una habitación con el nombre '{nombre}'.")
    else:
        lista_habitaciones.append(Habitacion(nombre))
        print(f"Habitación '{nombre}' creada exitosamente.")


def quitar_dispositivo(lista_habitaciones):
    """Opción 3: Quita un dispositivo de una habitación."""
    habitacion_seleccionada = seleccionar_habitacion(lista_habitaciones, "quitar un dispositivo")
    if habitacion_seleccionada is None: return

    print(f"\n--- Quitar dispositivo de {habitacion_seleccionada._tipo_habitacion} ---")
    print("1. Bombilla")
    print("2. Aire Acondicionado")
    opcion_disp = input(" Seleccione el tipo de dispositivo a quitar (1/2): ").strip()

    dispositivo_obj, tipo_disp = seleccionar_dispositivo(
        habitacion_seleccionada, opcion_disp, "quitar"
    )
    if dispositivo_obj is None: return

    if opcion_disp == '1':
        habitacion_seleccionada.eliminar_bombilla(dispositivo_obj)
    elif opcion_disp == '2':
        habitacion_seleccionada.eliminar_aire(dispositivo_obj)


def mostrar_estado_habitacion(lista_habitaciones):
    """Opción 4: Muestra el estado de una habitación específica."""
    habitacion_seleccionada = seleccionar_habitacion(lista_habitaciones, "mostrar su estado")
    if habitacion_seleccionada:
        habitacion_seleccionada.mostrar_estado()


def listar_habitaciones(lista_habitaciones):
    """Opción 5: Lista todas las habitaciones creadas."""
    print("\n-- Listado de Todas las Habitaciones ---")
    if not lista_habitaciones:
        print(" Actualmente no hay habitaciones creadas.")
        return
    nombres = [h._tipo_habitacion for h in lista_habitaciones]
    print(f"Hay **{len(lista_habitaciones)}** habitaciones creadas en la actualidad, llamadas: {', '.join(nombres)}.")


def mostrar_dispositivos_por_habitaciones(lista_habitaciones):
    """Opción 6: Muestra todos los dispositivos en todas las habitaciones."""
    print("\n--- Dispositivos Instalados por Habitación ---")
    if not lista_habitaciones:
        print(" Actualmente no hay habitaciones creadas.")
        return
    for habitacion in lista_habitaciones:
        print(f"\nPara la habitacion **{habitacion._tipo_habitacion}**")
        total_dispositivos = len(habitacion._lista_bombillas) + len(habitacion._lista_aires)
        print(f"Total de dispositivos: **{total_dispositivos}**")

        nombres_bombillas = [str(b) for b in habitacion._lista_bombillas]
        print(f"  Bombillas: {', '.join(nombres_bombillas) if nombres_bombillas else 'Ninguna'}")

        nombres_aires = [str(a) for a in habitacion._lista_aires]
        print(f"  Aires Acondicionados: {', '.join(nombres_aires) if nombres_aires else 'Ninguno'}")


def gestionar_programador(lista_habitaciones):
    """Opción 7: Permite asignar y configurar un programador a una bombilla o aire."""

    habitacion_seleccionada = seleccionar_habitacion(lista_habitaciones, "gestionar un programador")
    if habitacion_seleccionada is None: return

    while True:
        print(f"\nDispositivos programables en **{habitacion_seleccionada._tipo_habitacion}**:")
        print("1. Bombilla")
        print("2. Aire Acondicionado")
        print("3. Volver")

        opcion_disp = input("Seleccione el tipo de dispositivo a programar (1/2/3): ").strip()

        if opcion_disp == '3':
            return

        dispositivo_obj, tipo_disp_nombre = seleccionar_dispositivo(
            habitacion_seleccionada, opcion_disp, "programar"
        )
        if dispositivo_obj is None: continue

        # Asignar/obtener el programador
        programador = dispositivo_obj.asignar_programador()

        # Menú de programación
        while True:
            print(f"\nProgramando: **{dispositivo_obj}**")
            print("a. Programar Encendido (Comienzo)")
            print("b. Programar Apagado (Fin)")
            print("c. Borrar Programación")
            print("d. Mostrar Programación Actual")
            print("e. Volver a selección de dispositivo")
            opcion = input("Seleccione una opción (a-e): ").strip().lower()

            if opcion == 'e':
                break
            elif opcion == 'd':
                programador.mostrar_programacion()
                continue

            # Pide la información de tiempo para a, b, c
            try:
                dia = input("Día (ej. Lunes): ").strip()
                if dia.capitalize() not in Programador.getDiasSemana():
                    print(f"Día no válido. Días aceptados: {Programador.getDiasSemana()}")
                    continue
                hora = int(input("Hora (0-23): "))
                min = int(input("Minuto (0-59): "))
                seg = int(input("Segundo (0-59): "))

                if not Programador._validar_tiempo(hora, min, seg):
                    print("Los valores de hora, minuto o segundo están fuera de rango.")
                    continue

                if opcion == 'a':
                    programador.comienzo(dia, hora, min, seg)
                elif opcion == 'b':
                    programador.fin(dia, hora, min, seg)
                elif opcion == 'c':
                    programador.borrar(dia, hora, min, seg)
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Error: Los valores de tiempo deben ser números enteros.")
            except Exception as e:
                print(f"Ocurrió un error: {e}")


def menu():
    """Función principal que ejecuta el menú."""
    # Cargar datos al inicio (HU04)
    lista_habitaciones = cargar_habitaciones()

    condicionmenu = True
    while condicionmenu:
        mostrar_menu()
        opcion = input(" Seleccione una opción (1-9): ").strip()

        if opcion == '1':
            crear_habitacion(lista_habitaciones)
        elif opcion == '2':
            anadir_dispositivo(lista_habitaciones)
        elif opcion == '3':
            quitar_dispositivo(lista_habitaciones)
        elif opcion == '4':
            mostrar_estado_habitacion(lista_habitaciones)
        elif opcion == '5':
            listar_habitaciones(lista_habitaciones)
        elif opcion == '6':
            mostrar_dispositivos_por_habitaciones(lista_habitaciones)
        elif opcion == '7':
            gestionar_programador(lista_habitaciones)
        elif opcion == '8':
            gestionar_estado_dispositivo(lista_habitaciones)  # Refactorización c
        elif opcion == '9':
            guardar_habitaciones(lista_habitaciones)  # Guardar datos al salir (HU04)
            print("\n ¡Gracias por usar el sistema de gestión de habitaciones! Saliendo...")
            condicionmenu = False
        else:
            print(" Opción no válida. Por favor, ingrese un número del 1 al 9.")


if __name__ == "__main__":
    menu()
