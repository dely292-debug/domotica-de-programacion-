import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Domótico Integral v3.0")
        self.geometry("850x700")

        # --- SECCIÓN CARGA ---
        frame_superior = tk.Frame(self)
        frame_superior.pack(pady=10, fill="x")

        tk.Label(frame_superior, text="Fichero:").pack(side="left", padx=5)
        self.entradaNombreFichero = tk.Entry(frame_superior, width=20)
        self.entradaNombreFichero.insert(0, "habitaciones_data.pkl")
        self.entradaNombreFichero.pack(side="left", padx=5)

        self.botonCargarHabitaciones = tk.Button(frame_superior, text="Cargar Datos")
        self.botonCargarHabitaciones.pack(side="left", padx=5)

        # --- SECCIÓN EDICIÓN (NUEVA) ---
        frame_edicion = tk.LabelFrame(self, text="Gestión de Estructura")
        frame_edicion.pack(pady=5, padx=20, fill="x")

        self.botonNuevaHabitacion = tk.Button(frame_edicion, text="+ Nueva Habitación", bg="#e3f2fd")
        self.botonNuevaHabitacion.pack(side="left", padx=10, pady=5)

        self.botonNuevoDispositivo = tk.Button(frame_edicion, text="+ Añadir Dispositivo", bg="#e3f2fd")
        self.botonNuevoDispositivo.pack(side="left", padx=10, pady=5)

        # --- SECCIÓN VISUALIZACIÓN ---
        self.cajaTextoInfHabitaciones = scrolledtext.ScrolledText(self, width=95, height=12)
        self.cajaTextoInfHabitaciones.pack(pady=10)

        # --- PANEL DE CONTROL ---
        frame_control = tk.LabelFrame(self, text="Control en Tiempo Real")
        frame_control.pack(pady=10, padx=20, fill="both", expand=True)

        tk.Label(frame_control, text="Habitación:").grid(row=0, column=0, padx=5, pady=5)
        self.comboHabitaciones = ttk.Combobox(frame_control, state="readonly")
        self.comboHabitaciones.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_control, text="Dispositivo:").grid(row=0, column=2, padx=5, pady=5)
        self.comboDispositivos = ttk.Combobox(frame_control, state="readonly")
        self.comboDispositivos.grid(row=0, column=3, padx=5, pady=5)

        # Botones de acción
        self.botonEncender = tk.Button(frame_control, text="Encender", bg="#d4edda", width=15)
        self.botonEncender.grid(row=1, column=0, columnspan=2, pady=5)
        self.botonApagar = tk.Button(frame_control, text="Apagar", bg="#f8d7da", width=15)
        self.botonApagar.grid(row=1, column=2, columnspan=2, pady=5)

        self.botonSubir = tk.Button(frame_control, text="Aumentar (Intensidad/Temp)", width=25)
        self.botonSubir.grid(row=2, column=0, columnspan=2, pady=5)
        self.botonBajar = tk.Button(frame_control, text="Disminuir (Intensidad/Temp)", width=25)
        self.botonBajar.grid(row=2, column=2, columnspan=2, pady=5)

        self.botonSalir = tk.Button(self, text="Salir y Guardar Todo", command=self.destroy, height=2, bg="#eee")
        self.botonSalir.pack(pady=10, fill="x", padx=20)