import pickle
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
from libreria_Dispositivos.libreria_Habitaciones import Habitacion


class ControladorDomotica:
    def __init__(self, vista):
        self.vista = vista
        self.habitaciones = []

        # 1. Enlaces de archivos y estructura
        self.vista.botonCargarHabitaciones.config(command=self.cargar_datos)
        self.vista.botonNuevaHabitacion.config(command=self.crear_habitacion)
        self.vista.botonNuevoDispositivo.config(command=self.crear_dispositivo)
        self.vista.botonGenerarLog.config(command=self.ejecutar_log_historico)

        # 2. Enlace de selección de habitación (Esto ahora dispara el dibujo de columnas)
        self.vista.comboHabitaciones.bind("<<ComboboxSelected>>", self.dibujar_paneles_dispositivos)

        # 3. Configuración de salida
        self.vista.protocol("WM_DELETE_WINDOW", self.auto_guardar)
        self.vista.botonSalir.config(command=self.auto_guardar)

    def dibujar_paneles_dispositivos(self, event=None):
        """Borra las columnas y crea sliders/botones para cada dispositivo de la habitación."""
        idx = self.vista.comboHabitaciones.current()
        if idx == -1: return

        hab = self.habitaciones[idx]

        # Limpiar columnas actuales
        for widget in self.vista.columna_bombillas.winfo_children():
            widget.destroy()
        for widget in self.vista.columna_aires.winfo_children():
            widget.destroy()

        # Dibujar BOMBILLAS (Izquierda)
        for b in hab._lista_bombillas:
            frame = tk.Frame(self.vista.columna_bombillas, bd=2, relief="groove", pady=5)
            frame.pack(fill="x", padx=5, pady=5)

            tk.Label(frame, text=f"💡 {b._nombre}", font=('Arial', 10, 'bold')).pack()

            # Slider de Intensidad
            s = tk.Scale(frame, from_=b.UMBRAL_MIN, to=b.UMBRAL_MAX, orient="horizontal", label="Intensidad %")
            s.set(b._nivel_principal)
            # Lambda para vincular el slider a esta bombilla específica
            s.config(command=lambda val, obj=b: self.actualizar_valor_directo(obj, val))
            s.pack(fill="x", padx=10)

            # Botón de Color
            btn_c = tk.Button(frame, text="Elegir Color", command=lambda obj=b: self.seleccionar_color_directo(obj))
            btn_c.pack(pady=2)

        # Dibujar AIRES (Derecha)
        for a in hab._lista_aires:
            frame = tk.Frame(self.vista.columna_aires, bd=2, relief="groove", pady=5)
            frame.pack(fill="x", padx=5, pady=5)

            tk.Label(frame, text=f"❄️ {a._nombre}", font=('Arial', 10, 'bold')).pack()

            # Slider de Temperatura
            s = tk.Scale(frame, from_=a.UMBRAL_MIN, to=a.UMBRAL_MAX, orient="horizontal", label="Temperatura ºC")
            s.set(a._nivel_principal)
            s.config(command=lambda val, obj=a: self.actualizar_valor_directo(obj, val))
            s.pack(fill="x", padx=10)

    def actualizar_valor_directo(self, dispositivo, valor):
        """Actualiza el nivel de un dispositivo y refresca la caja de texto."""
        dispositivo._nivel_principal = int(float(valor))
        self.actualizar_interfaz()

    def seleccionar_color_directo(self, bombilla):
        color = colorchooser.askcolor(initialcolor=bombilla._color, title=f"Color {bombilla._nombre}")
        if color[0]:
            r, g, b = map(int, color[0])
            bombilla.set_color(r, g, b)
            self.actualizar_interfaz()

    def actualizar_interfaz(self, mensaje=""):
        """Refresca la caja de texto central."""
        self.vista.cajaTextoInfHabitaciones.delete(1.0, tk.END)
        if mensaje:
            self.vista.cajaTextoInfHabitaciones.insert(tk.END, f"SISTEMA: {mensaje}\n" + "-" * 30 + "\n")

        for h in self.habitaciones:
            info = f"\nHABITACIÓN: {h._tipo_habitacion}\n"
            for d in (h._lista_bombillas + h._lista_aires):
                info += f"  - {d._id}: {d._nombre} | {d.obtener_estado()}\n"
            self.vista.cajaTextoInfHabitaciones.insert(tk.END, info)

    # --- MÉTODOS DE PERSISTENCIA Y CREACIÓN ---
    def cargar_datos(self):
        fichero = self.vista.entradaNombreFichero.get()
        if os.path.exists(fichero):
            with open(fichero, 'rb') as f:
                self.habitaciones = pickle.load(f)
            # Actualizar combo de habitaciones
            self.vista.comboHabitaciones['values'] = [h._tipo_habitacion for h in self.habitaciones]
            self.actualizar_interfaz("Datos cargados.")
        else:
            messagebox.showwarning("Aviso", "Archivo no encontrado.")

    def auto_guardar(self):
        nombre = self.vista.entradaNombreFichero.get()
        try:
            with open(nombre, 'wb') as f:
                pickle.dump(self.habitaciones, f)
        except:
            pass
        self.vista.destroy()

    def crear_habitacion(self):
        nombre = simpledialog.askstring("Nuevo", "Nombre habitación:")
        if nombre:
            self.habitaciones.append(Habitacion(nombre))
            self.vista.comboHabitaciones['values'] = [h._tipo_habitacion for h in self.habitaciones]
            self.actualizar_interfaz()

    def crear_dispositivo(self):
        # 1. Verificar habitación seleccionada
        h_idx = self.vista.comboHabitaciones.current()
        if h_idx == -1:
            messagebox.showwarning("Aviso", "Selecciona una habitación primero.")
            return

        # 2. Obtener tipo de dispositivo
        tipo = simpledialog.askinteger("Tipo de Dispositivo", "1: Bombilla\n2: Aire Acondicionado",
                                       parent=self.vista, minvalue=1, maxvalue=2)
        if tipo is None: return  # El usuario canceló

        # 3. Obtener nombre del dispositivo
        nom = simpledialog.askstring("Nombre", "¿Cómo se llama el dispositivo?", parent=self.vista)

        # 4. Validar y añadir solo si tenemos el nombre
        if nom and nom.strip():
            hab = self.habitaciones[h_idx]
            if tipo == 1:
                hab.agregar_bombilla(nom.strip())
            else:
                hab.agregar_aire(nom.strip())

            # 5. ACTUALIZACIÓN FINAL: Refrescamos todo el panel
            self.dibujar_paneles_dispositivos()
            self.actualizar_interfaz(f"Dispositivo '{nom}' añadido con éxito.")
        else:
            messagebox.showwarning("Error", "El nombre no puede estar vacío.")
    def ejecutar_log_historico(self):
        h_idx = self.vista.comboHabitaciones.current()
        if h_idx != -1:
            hab = self.habitaciones[h_idx]
            nom = simpledialog.askstring("Log", "Nombre archivo .txt:", initialvalue=f"log_{hab._tipo_habitacion}.txt")
            if nom:
                hab.guardaLog(nom)
                messagebox.showinfo("Log", "Log generado.")