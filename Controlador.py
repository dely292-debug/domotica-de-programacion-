import pickle
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, ttk, filedialog
from libreria_Dispositivos.libreria_Habitaciones import Habitacion


class ControladorDomotica:
    def __init__(self, vista):
        self.vista = vista
        self.habitaciones = []

        # Enlaces de la interfaz
        self.vista.botonCargarHabitaciones.config(command=self.cargar_datos)
        self.vista.botonExaminar.config(command=self.examinar_archivo)
        self.vista.botonNuevaHabitacion.config(command=self.crear_habitacion)
        self.vista.botonNuevoDispositivo.config(command=self.crear_dispositivo)
        self.vista.botonGenerarLog.config(command=self.ejecutar_log_historico)
        self.vista.botonEliminarDispositivo.config(command=self.abrir_ventana_eliminacion)
        self.vista.botonSalir.config(command=self.auto_guardar)

        self.vista.botonVerLog.config(command=self.ejecutar_ver_log)

        self.vista.comboHabitaciones.bind("<<ComboboxSelected>>", self.dibujar_paneles_dispositivos)
        self.vista.protocol("WM_DELETE_WINDOW", self.auto_guardar)

    def examinar_archivo(self):
        ruta = filedialog.askopenfilename(
            initialdir=".",
            title="Seleccionar archivo .pkl",
            filetypes=(("Archivos Pickle", "*.pkl"), ("Todos los archivos", "*.*")),
            parent=self.vista
        )
        if ruta:
            self.vista.entradaNombreFichero.delete(0, tk.END)
            self.vista.entradaNombreFichero.insert(0, ruta)

    def cargar_datos(self):
        fichero = self.vista.entradaNombreFichero.get()
        if os.path.exists(fichero):
            try:
                with open(fichero, 'rb') as f:
                    self.habitaciones = pickle.load(f)
                self.vista.comboHabitaciones['values'] = [h._tipo_habitacion for h in self.habitaciones]
                if self.habitaciones:
                    self.vista.comboHabitaciones.current(0)
                    self.dibujar_paneles_dispositivos()
                self.actualizar_interfaz("Datos cargados correctamente.")
            except:
                messagebox.showerror("Error", "No se pudo cargar el archivo.")

    def dibujar_paneles_dispositivos(self, event=None):
        idx = self.vista.comboHabitaciones.current()
        if idx == -1: return
        self.vista.canvas_scroll.yview_moveto(0)
        hab = self.habitaciones[idx]

        for w in self.vista.columna_bombillas.winfo_children(): w.destroy()
        for w in self.vista.columna_aires.winfo_children(): w.destroy()

        # DIBUJAR BOMBILLAS
        for b in hab._lista_bombillas:
            f = tk.Frame(self.vista.columna_bombillas, bd=2, relief="ridge", pady=10)
            f.pack(fill="x", padx=10, pady=5)
            cv_b = tk.Canvas(f, width=60, height=80, highlightthickness=0)
            cv_b.pack(side="left", padx=10)

            info = tk.Frame(f)
            info.pack(side="left", fill="both", expand=True)
            tk.Label(info, text=b._nombre, font=('Arial', 10, 'bold')).pack(anchor="w")

            s = tk.Scale(info, from_=0, to=100, orient="horizontal", label="Intensidad %")
            s.set(b._nivel_principal)
            s.config(command=lambda val, obj=b, cv=cv_b: self.act_bombilla(obj, val, cv))
            s.pack(fill="x")

            tk.Button(info, text="🎨 Color", command=lambda obj=b, cv=cv_b: self.sel_color(obj, cv)).pack(anchor="w")
            self.dibujar_bombilla_vector(cv_b, b)

        # DIBUJAR AIRES
        for a in hab._lista_aires:
            f = tk.Frame(self.vista.columna_aires, bd=2, relief="ridge", pady=10)
            f.pack(fill="x", padx=10, pady=5)
            cv_t = tk.Canvas(f, width=40, height=110, highlightthickness=0)
            cv_t.pack(side="left", padx=10)
            l_t = tk.Label(f, text=f"{a._nivel_principal} ºC", font=('Arial', 12, 'bold'))
            l_t.pack()
            s_t = tk.Scale(f, from_=16, to=30, orient="horizontal")
            s_t.set(a._nivel_principal)
            s_t.config(command=lambda val, obj=a, lbl=l_t, cv=cv_t: self.act_aire(obj, val, lbl, cv))
            s_t.pack(fill="x", padx=10)
            self.actualizar_termometro_visual(cv_t, a._nivel_principal)

    def dibujar_bombilla_vector(self, canvas, obj):
        canvas.delete("all")
        intensidad = int(obj._nivel_principal)
        color = self.calcular_brillo(self.rgb_to_hex(obj._color), intensidad) if intensidad > 0 else "#444444"
        # Cristal de la bombilla
        canvas.create_oval(15, 5, 45, 35, fill=color, outline="black", width=2)
        # Cuello
        canvas.create_polygon(20, 30, 40, 30, 35, 50, 25, 50, fill=color, outline="black", width=2)
        # Base metálica
        canvas.create_rectangle(23, 50, 37, 65, fill="#888888", outline="black")

    def calcular_brillo(self, hex_color, porcentaje):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        f = porcentaje / 100
        return f'#{int(r * f):02x}{int(g * f):02x}{int(b * f):02x}'

    def act_bombilla(self, obj, val, cv):
        obj._nivel_principal = int(float(val))
        self.dibujar_bombilla_vector(cv, obj)
        self.guardar_en_disco()

    def sel_color(self, obj, cv):
        color_data = colorchooser.askcolor(initialcolor=self.rgb_to_hex(obj._color), parent=self.vista)
        if color_data[1]:
            r, g, b = map(int, color_data[0])
            obj._color = f"{r} {g} {b}"
            self.dibujar_bombilla_vector(cv, obj)
            self.guardar_en_disco()

    def rgb_to_hex(self, color_data):
        try:
            if isinstance(color_data, str):
                r, g, b = map(int, color_data.split())
            else:
                r, g, b = color_data
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return "#ffffff"

    def act_aire(self, obj, val, lbl, cv):
        t = int(float(val))
        obj._nivel_principal = t
        lbl.config(text=f"{t} ºC", fg="red" if t > 24 else "blue")
        self.actualizar_termometro_visual(cv, t)
        self.guardar_en_disco()

    def actualizar_termometro_visual(self, canvas, temp):
        canvas.delete("all")
        canvas.create_rectangle(15, 5, 25, 85, outline="black")
        canvas.create_oval(10, 80, 30, 100, fill="white", outline="black")
        f = max(0, min(1, (temp - 16) / 14))
        c = "red" if temp > 24 else "blue"
        canvas.create_rectangle(17, 85 - (f * 75), 23, 85, fill=c, outline="")
        canvas.create_oval(12, 82, 28, 98, fill=c, outline="")

    def crear_habitacion(self):
        n = simpledialog.askstring("Nuevo", "Nombre habitación:", parent=self.vista)
        if n:
            self.habitaciones.append(Habitacion(n))
            self.vista.comboHabitaciones['values'] = [h._tipo_habitacion for h in self.habitaciones]
            self.guardar_en_disco()

    def crear_dispositivo(self):
        idx = self.vista.comboHabitaciones.current()
        if idx == -1: return
        t = simpledialog.askinteger("Tipo", "1: Bombilla, 2: Aire", parent=self.vista, minvalue=1, maxvalue=2)
        if t:
            nom = simpledialog.askstring("Nombre", "Nombre del dispositivo:", parent=self.vista)
            if nom:
                if t == 1:
                    self.habitaciones[idx].agregar_bombilla(nom)
                else:
                    self.habitaciones[idx].agregar_aire(nom)
                self.dibujar_paneles_dispositivos()
                self.guardar_en_disco()

    def guardar_en_disco(self):
        f = self.vista.entradaNombreFichero.get()
        try:
            with open(f, 'wb') as file:
                pickle.dump(self.habitaciones, file)
            self.actualizar_interfaz()
        except:
            pass

    def actualizar_interfaz(self, m=""):
        self.vista.cajaTextoInfHabitaciones.delete(1.0, tk.END)
        for h in self.habitaciones:
            res = f"HABITACIÓN: {h._tipo_habitacion}\n"
            for d in (h._lista_bombillas + h._lista_aires):
                res += f"  - {d._nombre}: {d.obtener_estado()}\n"
            self.vista.cajaTextoInfHabitaciones.insert(tk.END, res + "\n")

    def auto_guardar(self):
        self.guardar_en_disco()
        self.vista.destroy()

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
        tk.Button(self.win_del, text="Confirmar", command=lambda: self.confirmar_eliminacion(hab)).pack(pady=5)

    def confirmar_eliminacion(self, hab):
        sel = self.combo_del.get()
        if any(b._nombre == sel for b in hab._lista_bombillas):
            hab.eliminar_bombilla(sel)
        else:
            hab.eliminar_aire(sel)
        self.win_del.destroy()
        self.dibujar_paneles_dispositivos()
        self.guardar_en_disco()

    def ejecutar_log_historico(self):
        """
        Este es el metodo que llama el botón.
        Aquí gestionamos qué hacer si la habitación lanza un error.
        """
        fichero = "log_Dormitorio.txt"
        try:
            # Llamamos al metodo de la habitación (que ahora lanza RuntimeError)
            self.habitacion.guarda_log(fichero)

            # Si quieres que el usuario sepa que funcionó, podrías usar un diálogo
            # pero el metodo guarda_log ya no hace print por sí solo.
            print(f"Éxito: Log guardado en {fichero}")

        except RuntimeError as e:
            # Aquí es donde capturamos el error generado en Habitacion.py
            # Puedes enviarlo a la vista para que lo muestre en una etiqueta o ventana
            self.vista.mostrar_error_en_interfaz(str(e))
        except Exception as e:
            # Error genérico por si ocurre algo no previsto
            print(f"Error inesperado: {e}")

    def mostrar_log_en_interfaz(self):
        fichero = "log_Dormitorio.txt"
        try:
            # 1. Leer el contenido del archivo con la codificación correcta
            with open(fichero, "r", encoding="utf-8") as f:
                contenido = f.read()

            # 2. Enviar el contenido a la Vista para que lo dibuje
            self.vista.actualizar_area_texto_log(contenido)

        except FileNotFoundError:
            self.vista.mostrar_error_en_interfaz("El archivo de log aún no ha sido creado.")
        except Exception as e:
            self.vista.mostrar_error_en_interfaz(f"Error al leer el log: {e}")