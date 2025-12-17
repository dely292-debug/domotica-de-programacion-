import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from tkinter import colorchooser

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Domótico Integral v3.0")
        self.geometry("950x850") # Aumentamos un poco el ancho para las dos columnas

        # --- 1. SECCIÓN CARGA ---
        frame_superior = tk.Frame(self)
        frame_superior.pack(pady=10, fill="x")

        tk.Label(frame_superior, text="Fichero:").pack(side="left", padx=5)
        self.entradaNombreFichero = tk.Entry(frame_superior, width=20)
        self.entradaNombreFichero.insert(0, "habitaciones_data.pkl")
        self.entradaNombreFichero.pack(side="left", padx=5)

        self.botonCargarHabitaciones = tk.Button(frame_superior, text="Cargar Datos")
        self.botonCargarHabitaciones.pack(side="left", padx=5)

        # --- 2. SECCIÓN EDICIÓN ---
        frame_edicion = tk.LabelFrame(self, text="Gestión de Estructura")
        frame_edicion.pack(pady=5, padx=20, fill="x")

        self.botonNuevaHabitacion = tk.Button(frame_edicion, text="+ Nueva Habitación", bg="#e3f2fd")
        self.botonNuevaHabitacion.pack(side="left", padx=10, pady=5)

        self.botonNuevoDispositivo = tk.Button(frame_edicion, text="+ Añadir Dispositivo", bg="#e3f2fd")
        self.botonNuevoDispositivo.pack(side="left", padx=10, pady=5)

        # --- 3. SECCIÓN VISUALIZACIÓN (LOG DE TEXTO) ---
        self.cajaTextoInfHabitaciones = scrolledtext.ScrolledText(self, width=110, height=10)
        self.cajaTextoInfHabitaciones.pack(pady=10)

        # --- 4. PANEL DE SELECCIÓN DE HABITACIÓN Y LOG TXT ---
        frame_seleccion = tk.Frame(self)
        frame_seleccion.pack(pady=5, padx=20, fill="x")

        tk.Label(frame_seleccion, text="Seleccione Habitación para controlar:").pack(side="left", padx=5)
        self.comboHabitaciones = ttk.Combobox(frame_seleccion, state="readonly", width=30)
        self.comboHabitaciones.pack(side="left", padx=5)

        self.botonGenerarLog = tk.Button(frame_seleccion, text="📑 Generar Log .txt", bg="#fff3cd")
        self.botonGenerarLog.pack(side="right", padx=5)

        # --- 5. PANEL DE CONTROL DINÁMICO (DOS COLUMNAS) ---
        # Este es el contenedor que el controlador vaciará y llenará
        self.contenedor_columnas = tk.Frame(self)
        self.contenedor_columnas.pack(pady=10, padx=20, fill="both", expand=True)

        # Sub-frame Izquierdo: Bombillas
        self.columna_bombillas = tk.LabelFrame(self.contenedor_columnas, text="💡 BOMBILLAS", fg="blue")
        self.columna_bombillas.pack(side="left", fill="both", expand=True, padx=5)
        self.columna_bombillas.config(minwidth=300, minheight=200)  # Evita que colapse a 0 píxeles
        # Sub-frame Derecho: Aires
        self.columna_aires = tk.LabelFrame(self.contenedor_columnas, text="❄️ AIRES ACONDICIONADOS", fg="red")
        self.columna_aires.pack(side="right", fill="both", expand=True, padx=5)
        self.columna_aires.config(minwidth=300, minheight=200)

        # --- 6. BOTÓN SALIR ---
        self.botonSalir = tk.Button(self, text="Salir y Guardar Todo", height=2, bg="#eee")
        self.botonSalir.pack(pady=10, fill="x", padx=20)