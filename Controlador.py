import pickle
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from libreria_Dispositivos.libreria_Habitaciones import Habitacion


class ControladorDomotica:
    def __init__(self, vista):
        self.vista = vista
        self.habitaciones = []

        # Enlaces de eventos
        self.vista.botonCargarHabitaciones.config(command=self.cargar_datos)
        self.vista.botonNuevaHabitacion.config(command=self.crear_habitacion)
        self.vista.botonNuevoDispositivo.config(command=self.crear_dispositivo)
        self.vista.comboHabitaciones.bind("<<ComboboxSelected>>", self.actualizar_lista_dispositivos)

        self.vista.botonEncender.config(command=lambda: self.cambiar_estado(True))
        self.vista.botonApagar.config(command=lambda: self.cambiar_estado(False))
        self.vista.botonSubir.config(command=lambda: self.ajustar_nivel(1))
        self.vista.botonBajar.config(command=lambda: self.ajustar_nivel(-1))
        # --- CONFIGURACIÓN DE GUARDADO AL SALIR ---
        self.vista.protocol("WM_DELETE_WINDOW", self.auto_guardar)
        self.vista.botonSalir.config(command=self.auto_guardar)

    def auto_guardar(self):
        """Función que se ejecuta al cerrar la app para persistir los datos."""
        nombre_fichero = self.vista.entradaNombreFichero.get()
        try:
            with open(nombre_fichero, 'wb') as f:
                pickle.dump(self.habitaciones, f)
            print(f"Datos guardados automáticamente en {nombre_fichero}")
        except Exception as e:
            print(f"Error al guardar: {e}")

        self.vista.destroy()  # Cierra la ventana definitivamente

    def cargar_datos(self):
        """Carga las habitaciones desde el archivo indicado en el campo de texto."""
        fichero = self.vista.entradaNombreFichero.get()
        if os.path.exists(fichero):
            try:
                with open(fichero, 'rb') as f:
                    self.habitaciones = pickle.load(f)
                self.actualizar_interfaz(f"Éxito: Se han cargado {len(self.habitaciones)} habitaciones.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        else:
            messagebox.showwarning("Archivo no encontrado", f"El archivo '{fichero}' no existe. Se iniciará vacío.")
            self.habitaciones = []
            self.actualizar_interfaz()
    def crear_habitacion(self):
        nombre = simpledialog.askstring("Nueva Habitación", "¿Nombre de la habitación?")
        if nombre:
            if any(h._tipo_habitacion == nombre for h in self.habitaciones):
                messagebox.showerror("Error", "Ya existe esa habitación.")
            else:
                nueva_hab = Habitacion(nombre)
                self.habitaciones.append(nueva_hab)
                self.actualizar_interfaz(f"Habitación '{nombre}' creada.")

    def crear_dispositivo(self):
        idx_hab = self.vista.comboHabitaciones.current()
        if idx_hab == -1:
            messagebox.showwarning("Atención", "Selecciona primero una habitación.")
            return

        hab = self.habitaciones[idx_hab]
        tipo = simpledialog.askinteger("Nuevo Dispositivo", "1: Bombilla\n2: Aire Acondicionado", minvalue=1,
                                       maxvalue=2)
        if not tipo: return

        nombre = simpledialog.askstring("Nombre", "¿Nombre del dispositivo?")
        if not nombre: return

        if tipo == 1:
            hab.agregar_bombilla(nombre)
        else:
            hab.agregar_aire(nombre)

        self.actualizar_interfaz(f"Dispositivo {nombre} añadido.")
        self.actualizar_lista_dispositivos(None)

    def cargar_datos(self):
        fichero = self.vista.entradaNombreFichero.get()
        if os.path.exists(fichero):
            try:
                with open(fichero, 'rb') as f:
                    self.habitaciones = pickle.load(f)
                self.actualizar_interfaz("Datos cargados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Fichero corrupto: {e}")
        else:
            messagebox.showinfo("Info", "Iniciando sistema vacío.")
            self.habitaciones = []
            self.actualizar_interfaz()

    def actualizar_interfaz(self, mensaje=""):
        # Actualizar Dropdown de habitaciones
        nombres_hab = [h._tipo_habitacion for h in self.habitaciones]
        self.vista.comboHabitaciones['values'] = nombres_hab

        # Actualizar Log Visual
        self.vista.cajaTextoInfHabitaciones.delete(1.0, tk.END)
        if mensaje:
            self.vista.cajaTextoInfHabitaciones.insert(tk.END, f"SISTEMA: {mensaje}\n" + "-" * 30 + "\n")

        for h in self.habitaciones:
            info = f"\nHABITACIÓN: {h._tipo_habitacion}\n"
            dispositivos = h._lista_bombillas + h._lista_aires
            if not dispositivos:
                info += "  (Vacía)\n"
            for d in dispositivos:
                info += f"  - {d._id}: {d._nombre} | {d.obtener_estado()}\n"
            self.vista.cajaTextoInfHabitaciones.insert(tk.END, info)

    def actualizar_lista_dispositivos(self, event):
        idx = self.vista.comboHabitaciones.current()
        if idx != -1:
            hab = self.habitaciones[idx]
            todos = hab._lista_bombillas + hab._lista_aires
            self.vista.comboDispositivos['values'] = [f"{d._id} - {d._nombre}" for d in todos]
            self.vista.comboDispositivos.set("")

    def cambiar_estado(self, encender):
        disp = self.get_selected_obj()
        if disp:
            disp.encender() if encender else disp.apagar()
            self.actualizar_interfaz()

    def ajustar_nivel(self, direccion):
        disp = self.get_selected_obj()
        if disp:
            try:
                disp.aumentarIntensidad() if direccion > 0 else disp.disminuirIntensidad()
                self.actualizar_interfaz()
            except ValueError as e:
                messagebox.showerror("Límite", str(e))

    def get_selected_obj(self):
        h_idx = self.vista.comboHabitaciones.current()
        d_idx = self.vista.comboDispositivos.current()
        if h_idx != -1 and d_idx != -1:
            hab = self.habitaciones[h_idx]
            return (hab._lista_bombillas + hab._lista_aires)[d_idx]
        return None