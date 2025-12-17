import pickle
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, ttk
from libreria_Dispositivos.libreria_Habitaciones import Habitacion


class ControladorDomotica:
    def __init__(self, vista):
        self.vista = vista
        self.habitaciones = []

        # 1. Enlaces de la interfaz
        self.vista.botonCargarHabitaciones.config(command=self.cargar_datos)
        self.vista.botonNuevaHabitacion.config(command=self.crear_habitacion)
        self.vista.botonNuevoDispositivo.config(command=self.crear_dispositivo)
        self.vista.botonGenerarLog.config(command=self.ejecutar_log_historico)
        self.vista.botonEliminarDispositivo.config(command=self.abrir_ventana_eliminacion)
        self.vista.botonSalir.config(command=self.auto_guardar)

        # 2. Vinculación del evento de selección
        self.vista.comboHabitaciones.bind("<<ComboboxSelected>>", self.dibujar_paneles_dispositivos)

        # 3. Protocolo de cierre
        self.vista.protocol("WM_DELETE_WINDOW", self.auto_guardar)

    def cargar_datos(self):
        fichero = self.vista.entradaNombreFichero.get()
        if os.path.exists(fichero):
            try:
                with open(fichero, 'rb') as f:
                    self.habitaciones = pickle.load(f)
                nombres = [h._tipo_habitacion for h in self.habitaciones]
                self.vista.comboHabitaciones['values'] = nombres
                if nombres:
                    self.vista.comboHabitaciones.current(0)
                    self.dibujar_paneles_dispositivos()
                self.actualizar_interfaz(f"Éxito: {len(nombres)} habitaciones cargadas.")
                messagebox.showinfo("Carga Completa", f"Se han cargado {len(nombres)} habitaciones.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al leer el archivo: {e}")
        else:
            messagebox.showwarning("Error", "El archivo no existe.")

    def dibujar_paneles_dispositivos(self, event=None):
        idx = self.vista.comboHabitaciones.current()
        if idx == -1: return

        # Volver al inicio del scroll al cambiar de habitación
        self.vista.canvas_dispositivos.yview_moveto(0)

        hab = self.habitaciones[idx]

        # Limpiar columnas anteriores
        for w in self.vista.columna_bombillas.winfo_children(): w.destroy()
        for w in self.vista.columna_aires.winfo_children(): w.destroy()

        # Dibujar Bombillas
        for b in hab._lista_bombillas:
            f = tk.Frame(self.vista.columna_bombillas, bd=2, relief="ridge", pady=10)
            f.pack(fill="x", padx=10, pady=5)
            header = tk.Frame(f)
            header.pack(fill="x")

            color_hex = self.rgb_to_hex(b._color)
            cv = tk.Canvas(header, width=15, height=15, bg=color_hex, highlightthickness=1)
            cv.pack(side="left", padx=5)
            tk.Label(header, text=b._nombre, font=('Arial', 10, 'bold')).pack(side="left")

            s = tk.Scale(f, from_=b.UMBRAL_MIN, to=b.UMBRAL_MAX, orient="horizontal",
                         label=f"Intensidad: {b._nivel_principal}%")
            s.set(b._nivel_principal)
            s.config(command=lambda val, obj=b, lbl=s, cv_obj=cv: self.act_bombilla(obj, val, lbl, cv_obj))
            s.pack(fill="x", padx=10)

            tk.Button(f, text="Elegir Color", command=lambda obj=b, c=cv: self.sel_color(obj, c)).pack(pady=5)
            self.actualizar_estado_visual_bombilla(b, cv)

        # Dibujar Aires
        for a in hab._lista_aires:
            f = tk.Frame(self.vista.columna_aires, bd=2, relief="ridge", pady=10)
            f.pack(fill="x", padx=10, pady=5)
            header = tk.Frame(f)
            header.pack(fill="x")

            cv_termo = tk.Canvas(header, width=40, height=110, highlightthickness=0)
            cv_termo.pack(side="left", padx=10)
            tk.Label(header, text=f"❄️ {a._nombre}", font=('Arial', 10, 'bold')).pack(side="left")

            l_temp = tk.Label(f, text=f"{a._nivel_principal} ºC", font=('Arial', 14, 'bold'))
            l_temp.pack()

            self.actualizar_termometro_visual(cv_termo, a._nivel_principal)

            s_temp = tk.Scale(f, from_=a.UMBRAL_MIN, to=a.UMBRAL_MAX, orient="horizontal")
            s_temp.set(a._nivel_principal)
            s_temp.config(command=lambda val, obj=a, lbl=l_temp, cv=cv_termo: self.act_aire(obj, val, lbl, cv))
            s_temp.pack(fill="x", padx=10)

    # --- FUNCIONES DE APOYO Y ACCIONES ---
    def rgb_to_hex(self, color_data):
        try:
            if isinstance(color_data, str):
                r, g, b = map(int, color_data.split())
            else:
                r, g, b = color_data
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return "#ffffff"

    def actualizar_estado_visual_bombilla(self, bombilla_obj, canvas_widget):
        try:
            color_base_hex = self.rgb_to_hex(bombilla_obj._color)
            intensidad = int(bombilla_obj._nivel_principal)
            if intensidad > 0:
                # Lógica simple de brillo multiplicando por el factor de intensidad
                canvas_widget.config(bg=color_base_hex, relief="raised", bd=2)
            else:
                canvas_widget.config(bg="#222222", relief="sunken", bd=1)
        except:
            pass

    def act_bombilla(self, obj, val, lbl, cv_obj):
        obj._nivel_principal = int(float(val))
        lbl.config(label=f"Intensidad: {obj._nivel_principal}%")
        self.actualizar_estado_visual_bombilla(obj, cv_obj)
        self.guardar_en_disco()

    def act_aire(self, obj, val, lbl, cv_termo):
        temp = int(float(val))
        obj._nivel_principal = temp
        lbl.config(text=f"{temp} ºC")
        self.actualizar_termometro_visual(cv_termo, temp)
        self.guardar_en_disco()

    def sel_color(self, obj, canvas):
        color_data = colorchooser.askcolor(initialcolor=self.rgb_to_hex(obj._color))
        if color_data[1]:
            r, g, b = map(int, color_data[0])
            obj._color = f"{r} {g} {b}"
            self.actualizar_estado_visual_bombilla(obj, canvas)
            self.guardar_en_disco()

    def guardar_en_disco(self):
        fichero = self.vista.entradaNombreFichero.get()
        try:
            with open(fichero, 'wb') as f:
                pickle.dump(self.habitaciones, f)
            self.actualizar_interfaz()
        except Exception as e:
            print(f"Error al guardar: {e}")

    def actualizar_interfaz(self, mensaje=""):
        self.vista.cajaTextoInfHabitaciones.delete(1.0, tk.END)
        if mensaje: self.vista.cajaTextoInfHabitaciones.insert(tk.END, f"SISTEMA: {mensaje}\n\n")
        for h in self.habitaciones:
            info = f"HABITACIÓN: {h._tipo_habitacion}\n"
            for d in (h._lista_bombillas + h._lista_aires):
                info += f"  - {d._nombre}: {d.obtener_estado()}\n"
            self.vista.cajaTextoInfHabitaciones.insert(tk.END, info + "\n")

    def auto_guardar(self):
        self.guardar_en_disco()
        self.vista.destroy()

    def crear_habitacion(self):
        nombre = simpledialog.askstring("Nuevo", "Nombre habitación:", parent=self.vista)
        if nombre:
            self.habitaciones.append(Habitacion(nombre))
            self.vista.comboHabitaciones['values'] = [h._tipo_habitacion for h in self.habitaciones]
            self.guardar_en_disco()

    def crear_dispositivo(self):
        h_idx = self.vista.comboHabitaciones.current()
        if h_idx == -1: return
        tipo = simpledialog.askinteger("Tipo", "1: Bombilla, 2: Aire", parent=self.vista, minvalue=1, maxvalue=2)
        nom = simpledialog.askstring("Nombre", "Nombre del dispositivo:", parent=self.vista)
        if nom:
            hab = self.habitaciones[h_idx]
            if tipo == 1:
                hab.agregar_bombilla(nom)
            else:
                hab.agregar_aire(nom)
            self.dibujar_paneles_dispositivos()
            self.guardar_en_disco()

    def ejecutar_log_historico(self):
        idx = self.vista.comboHabitaciones.current()
        if idx != -1:
            hab = self.habitaciones[idx]
            nom = simpledialog.askstring("Log", "Archivo .txt:", initialvalue=f"log_{hab._tipo_habitacion}.txt")
            if nom: hab.guardaLog(nom)

    def abrir_ventana_eliminacion(self):
        idx = self.vista.comboHabitaciones.current()
        if idx == -1: return
        hab = self.habitaciones[idx]
        nombres = [b._nombre for b in hab._lista_bombillas] + [a._nombre for a in hab._lista_aires]
        if not nombres: return
        self.win_del = tk.Toplevel(self.vista)
        self.win_del.title("Eliminar")
        self.combo_del = ttk.Combobox(self.win_del, values=nombres, state="readonly")
        self.combo_del.pack(pady=10, padx=10)
        self.combo_del.current(0)
        tk.Button(self.win_del, text="Confirmar", command=lambda: self.confirmar_eliminacion(hab)).pack(pady=5)

    def confirmar_eliminacion(self, hab):
        nombre_sel = self.combo_del.get()
        if not nombre_sel: return
        es_bombilla = any(b._nombre == nombre_sel for b in hab._lista_bombillas)
        if es_bombilla:
            hab.eliminar_bombilla(nombre_sel)
        else:
            hab.eliminar_aire(nombre_sel)
        self.win_del.destroy()
        self.dibujar_paneles_dispositivos()
        self.guardar_en_disco()

    def actualizar_termometro_visual(self, canvas, temp):
        canvas.delete("all")
        canvas.create_rectangle(15, 5, 25, 85, outline="black", width=2)
        canvas.create_oval(10, 80, 30, 100, outline="black", width=2, fill="white")
        altura_max = 75
        factor = (temp - 16) / (30 - 16)
        factor = max(0, min(1, factor))
        altura_mercurio = factor * altura_max
        color = "red" if temp > 24 else "blue"
        canvas.create_rectangle(17, 85 - altura_mercurio, 23, 85, fill=color, outline="")
        canvas.create_oval(12, 82, 28, 98, fill=color, outline="")