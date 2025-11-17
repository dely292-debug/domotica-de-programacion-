from libreria_Dispositivos.libreria_Habitaciones import Habitacion
from libreria_Dispositivos.libreria_Programador import Programador

def mostrar_menu():
    """Muestra las opciones del menú."""

    print("      **Menú de Gestión de Habitaciones** ")
    print("1. Crear habitación")
    print("2. Añadir dispositivo")
    print("3. Quitar dispositivo")
    print("4. Mostrar estado de habitación")
    print("5. Listar todas las habitaciones")
    print("6. Mostrar dispositivos por habitaciones")
    print("7. Gestionar Programador (Bombilla/Aire)")
    print("8. Salir")


def crear_habitacion(lista_habitaciones):
    """Opción 1: Crea una nueva instancia de Habitacion y la añade a lista_habitaciones."""
    nombre = input("️\n Ingrese el nombre de la habitación a crear : \n").strip()
    # CORRECCIÓN DE LÓGICA: Comprobar si el atributo _tipo_habitacion del objeto ya existe
    if any(h._tipo_habitacion == nombre for h in lista_habitaciones):
        print(f" Error: Ya existe una habitación con el nombre '{nombre}'.")
    else:
        lista_habitaciones.append(Habitacion(nombre))
        print(f"Habitación '{nombre}' creada exitosamente.\n")

def seleccionar_habitacion(lista_habitaciones,accion="gestionar"):
    """Función auxiliar para seleccionar una habitación existente."""
    if not lista_habitaciones:
        print(" No hay habitaciones creadas. Por favor, cree una primero.")
        return None
    print("\n--- Habitaciones disponibles ---")
    # Muestra el índice (i) de la lista, que comienza en 0
    for i,nombre_instancia in enumerate(lista_habitaciones):
        print(f"{i}.- {nombre_instancia._tipo_habitacion} ")

    while True:
        try:
            # Pide al usuario que seleccione el número o el nombre de la habitacion
            seleccion = input(f"\n Seleccione el número de la habitación a {accion} o escriba su nombre: ").strip()

            # 1 Manejo de la seleccion por numero
            if seleccion.isdigit():
                # Si es un número, el índice es el número que el usuario introdujo (i = 0, 1, 2...)
                indice = int(seleccion)
                if 0 <= indice < len(lista_habitaciones):
                    # devuelve la INSTANCIA DEL OJETO HABITACION
                    nombre_sel = lista_habitaciones[indice]
                    return nombre_sel# Devuelve el nombre
                else:
                    print(f"Número de habitación no válido.El numero debe estar entre 0 y {len(lista_habitaciones)-1}")
             # 2 Manejo de la seleccion por nombre
            else:
               habitacion_encontrada=None
               #Itera sobre la lista para buscar coincidencia por el atributo ._tipo_habitacion
               for nombre_instancia in lista_habitaciones:
                   # Compara la cadena introducida por el usuario (seleccion)
                   # con el atributo ._tipo_habitacion del objeto actual
                   if seleccion==nombre_instancia._tipo_habitacion:
                       habitacion_encontrada=nombre_instancia
                       break
               if habitacion_encontrada:
                   return habitacion_encontrada
               else:
                   print(" Nombre o número de habitación no encontrado.")
        except Exception as e:
            print(f"Entrada no válida: {e}")


def anadir_dispositivo(lista_habitaciones):
    """Opción 2: Añade un dispositivo a una habitación."""
    # 1. Selecciona la INSTANCIA de la habitación
    habitacion_seleccionada = seleccionar_habitacion(lista_habitaciones, "añadir un dispositivo")

    if habitacion_seleccionada is None:
        return

    print(f"Va añadir un disposito a la habitacion {habitacion_seleccionada._tipo_habitacion} seleccione el tipo:\n" )
    print("\n--- Tipos de Dispositivo ---")
    print("1. Bombilla")
    print("2. Aire Acondicionado")
    print("----------------------------")
    opcion_disp = input(" Seleccione el tipo de dispositivo:\n Pulse '1' para bombilla  \n Pulse '2' para aire \n").strip()
    nombre_disp = input("  Ingrese el nombre del dispositivo:\n ").strip()

    if not nombre_disp:
        print(" El nombre del dispositivo no puede estar vacío.")
        return

    # 2. Llama al mETODO sobre la INSTANCIA de la habitación seleccionada

    if opcion_disp == '1':
        habitacion_seleccionada.agregar_bombilla(nombre_disp)
    elif opcion_disp == '2':
        habitacion_seleccionada.agregar_aire(nombre_disp)
    else:
        print(" Opción de dispositivo no válida.")


def quitar_dispositivo(lista_habitaciones):
    """Opción 3: Quita un dispositivo de una habitación."""
    # 1. Selecciona la INSTANCIA de la habitación
    habitacion_seleccionada = seleccionar_habitacion(lista_habitaciones,"quitar un dispositivo")
    if habitacion_seleccionada is None:
        return

    print(f"\n--- Quitar dispositivo de {habitacion_seleccionada._tipo_habitacion} ---")
    print("1. Bombilla")
    print("2. Aire Acondicionado")
    print("----------------------------")

    opcion_disp = input(" Seleccione el tipo de dispositivo a quitar (1/2): ").strip()

    lista_dispositivos = None
    tipo_disp = ""
    eliminar_metodo = None
    if not opcion_disp :
        print(" La opcion de dispositivo no puede estar vacío.")
        return

    # --- Lógica para Bombillas ---
    if opcion_disp == '1':
        lista_dispositivos = habitacion_seleccionada._lista_bombillas
        tipo_disp="bombilla"
        eliminar_metodo = habitacion_seleccionada.eliminar_bombilla
    elif opcion_disp == '2':
        lista_dispositivos = habitacion_seleccionada._lista_aires
        tipo_disp = "aire acondicionado"
        eliminar_metodo = habitacion_seleccionada.eliminar_aire
    else:
        print("  Opción de dispositivo no válida.")
        return

    if not lista_dispositivos:
        print(f"No hay {tipo_disp}s en {habitacion_seleccionada._tipo_habitacion} para quitar. ")
        return
    print(f"\n {tipo_disp.capitalize()}s disponibles:")
    for i, dispositivo in enumerate(lista_dispositivos):
        # Muestra el nombre/representación del objeto dispositivo
        print(f"{i}.- {dispositivo}")

    while True:
            #Pide al usuario que seleccione el número o el nombre de la habitacion
            seleccion = input(f"Seleccione el número de {tipo_disp} a quitar" ).strip()
            if seleccion.isdigit():
                try:
                    # Si es un número, el índice es el número que el usuario introdujo (i = 0, 1, 2...)
                   indice=int (seleccion)
                   max_indice = (len(lista_dispositivos) - 1)
                   if 0<=indice<=max_indice:
                       dispositivo_eliminado=lista_dispositivos[indice]
                       eliminar_metodo(dispositivo_eliminado)  # Llama al MEtodo de eliminación (recibe el objeto)
                       return
                   else:
                        print(f"La seleccion {seleccion} no corresponde con ningun numero comprendido entre [0-{max_indice}]")
                except Exception as e:
                   print(f"entrada no valida: {e}")
            else:
                print(f"La seleccion {seleccion} no es un numero valido")

def mostrar_estado_habitacion(lista_habitaciones):
    """Opción 4: Muestra el estado de una habitación específica."""
    habitacion_seleccionada = seleccionar_habitacion(lista_habitaciones,"mostrar su estado")
    if habitacion_seleccionada:
        habitacion_seleccionada.mostrar_estado()
def listar_habitaciones(lista_habitaciones):
    """Opción 5: Lista todas las habitaciones creadas."""
    print("\n--  Listado de Todas las Habitaciones ---")
    if not lista_habitaciones:
        print("  Actualmente no hay habitaciones creadas.")
        return
    nombres = [h._tipo_habitacion for h in lista_habitaciones]
    print(f"Hay **{len(lista_habitaciones)}** habitaciones creadas en la actualidad, llamadas: {', '.join(nombres)}.")
    print("Para añadir diríjase al menú opción 1.")

def mostrar_dispositivos_por_habitaciones(lista_habitaciones):
    """Opción 6: Muestra todos los dispositivos en todas las habitaciones."""
    print("\n---  Dispositivos Instalados por Habitación ---")
    if not lista_habitaciones:
        print(" Actualmente no hay habitaciones creadas.")
        return
    for habitacion in lista_habitaciones:
        # Se accede al nombre a través del atributo '_tipo_habitacion'
        print(f"\nPara la habitacion {habitacion._tipo_habitacion}")
        total_dispositivos = len(habitacion._lista_bombillas) + len(habitacion._lista_aires)
        print(f"Total de dispositivos: **{total_dispositivos}**")

        # 1. Creamos una lista de nombres aplicando str() a cada objeto Bombilla
        nombres_bombillas = [str(b) for b in habitacion._lista_bombillas]
        print( f"  Bombillas: {', '.join(nombres_bombillas) if nombres_bombillas else 'Ninguna'}")

        # 2. Creamos una lista de nombres aplicando str() a cada objeto Aire
        nombres_aires = [str(a) for a in habitacion._lista_aires]
        print(f"   Aires Acondicionados: {', '.join(nombres_aires) if nombres_aires else 'Ninguno'}" )


def gestionar_programador(lista_habitaciones):
    """Opción 7: Permite asignar y configurar un programador a una bombilla o aire."""
    print("\n--- Gestor de Programación ---")

    # 1. Seleccionar la habitación
    habitacion_seleccionada = seleccionar_habitacion(lista_habitaciones, "gestionar un programador")
    if habitacion_seleccionada is None:
        return
    while True:
        print(f"\nDispositivos programables en **{habitacion_seleccionada._tipo_habitacion}**:")
        print("1. Bombilla")
        print("2. Aire Acondicionado")
        print("3. Volver")

        opcion_disp = input("Seleccione el tipo de dispositivo a programar (1/2/3): ").strip()

        if opcion_disp == '3':
            return

        dispositivos = None
        tipo_disp_nombre = ""

        if opcion_disp == '1':
            dispositivos = habitacion_seleccionada._lista_bombillas
            tipo_disp_nombre = "bombilla"
        elif opcion_disp == '2':
            dispositivos = habitacion_seleccionada._lista_aires
            tipo_disp_nombre = "aire acondicionado"
        else:
            print("Opción no válida.")
            continue

        if not dispositivos:
            print(f"No hay {tipo_disp_nombre}s en {habitacion_seleccionada._tipo_habitacion} para programar.")
            continue
        # 1. Seleccionar el dispositivo
        print(f"\n{tipo_disp_nombre.capitalize()}s disponibles:")
        for i, disp in enumerate(dispositivos):
            print(f"{i}.- {disp}")
        try:
            seleccion = int(input(f"Seleccione el **número** del {tipo_disp_nombre} a programar: ").strip())
            dispositivo_obj = dispositivos[seleccion]
        except (ValueError, IndexError):
            print("Selección no válida. Vuelva a intentarlo.")
            continue
        # 2. Asignar/obtener el programador
        programador = dispositivo_obj.asignar_programador()
        # 3. Menú de programación (idéntico al anterior)
        while True:
            print(f"\nProgramando: **{dispositivo_obj}**")
            # ... (código del submenú de programación a-e se mantiene igual) ...
            print("a. Programar Encendido (Comienzo)")
            print("b. Programar Apagado (Fin)")
            print("c. Borrar Programación")
            print("d. Mostrar Programación Actual")
            print("e. Volver a selección de dispositivo")
            opcion = input("Seleccione una opción (a-e): ").strip().lower()
            if opcion == 'e':
                break  # Sale del submenú, vuelve a la selección de 1/2/3
            elif opcion == 'd':
                programador.mostrar_programacion()
                continue
            try:
                dia = input("Día (ej. Lunes): ").strip()
                if dia.capitalize() not in Programador.getDiasSemana() and opcion != 'd':
                    print(f"Día no válido. Días aceptados: {Programador.getDiasSemana()}")
                    continue
                hora = int(input("Hora (0-23): "))
                min = int(input("Minuto (0-59): "))
                seg = int(input("Segundo (0-59): "))
                if not (0 <= hora <= 23 and 0 <= min <= 59 and 0 <= seg <= 59):
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
    lista_habitaciones = []
    condicionmenu=True
    while condicionmenu:
        mostrar_menu()
        opcion = input(" Seleccione una opción (1-8): ").strip()
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
            gestionar_programador(lista_habitaciones)  # Nueva función
        elif opcion == '8':
            print("\n ¡Gracias por usar el sistema de gestión de habitaciones! Saliendo...")
            condicionmenu = False
        else:
            print(" Opción no válida. Por favor, ingrese un número del 1 al 8.")
if __name__ == "__main__":
    menu()
