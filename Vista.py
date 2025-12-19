import tkinter as tk
from tkinter import scrolledtext, ttk

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Domótico Integral v3.0")
        self.geometry("950x850")

        # --- 1. SECCIÓN CARGA ---
        frame_superior = tk.Frame(self)
        frame_superior.pack(pady=10, fill="x")

        tk.Label(frame_superior, text="Fichero:").pack(side="left", padx=5)
        self.entradaNombreFichero = tk.Entry(frame_superior, width=40)
        self.entradaNombreFichero.insert(0, "habitaciones_data.pkl")
        self.entradaNombreFichero.pack(side="left", padx=5)

        # Botón para buscar archivos en Windows
        self.botonExaminar = tk.Button(frame_superior, text="📁 Examinar", bg="#f5f5f5")
        self.botonExaminar.pack(side="left", padx=5)

        self.botonCargarHabitaciones = tk.Button(frame_superior, text="Cargar Datos", bg="#dcedc8")
        self.botonCargarHabitaciones.pack(side="left", padx=5)

        # --- 2. SECCIÓN GESTIÓN (Estructura) ---
        frame_edicion = tk.LabelFrame(self, text="Gestión de Estructura")
        frame_edicion.pack(pady=5, padx=20, fill="x")

        self.botonNuevaHabitacion = tk.Button(frame_edicion, text="+ Nueva Habitación", bg="#e3f2fd")
        self.botonNuevaHabitacion.pack(side="left", padx=10, pady=5)

        self.botonNuevoDispositivo = tk.Button(frame_edicion, text="+ Añadir Dispositivo", bg="#e3f2fd")
        self.botonNuevoDispositivo.pack(side="left", padx=10, pady=5)

        self.botonEliminarDispositivo = tk.Button(frame_edicion, text="- Eliminar Dispositivo", bg="#ffcdd2")
        self.botonEliminarDispositivo.pack(side="left", padx=10, pady=5)



        # --- 3. LOG DE TEXTO ---
        self.cajaTextoInfHabitaciones = scrolledtext.ScrolledText(self, width=110, height=8)
        self.cajaTextoInfHabitaciones.pack(pady=10)

        # --- 4. PANEL SELECCIÓN ---
        frame_seleccion = tk.Frame(self)
        frame_seleccion.pack(pady=5, padx=20, fill="x")

        tk.Label(frame_seleccion, text="Seleccione Habitación:").pack(side="left", padx=5)
        self.comboHabitaciones = ttk.Combobox(frame_seleccion, state="readonly", width=30)
        self.comboHabitaciones.pack(side="left", padx=5)

        self.botonGenerarLog = tk.Button(frame_seleccion, text="📑 Generar Log .txt", bg="#fff3cd")
        self.botonGenerarLog.pack(side="right", padx=5)

        # --- 5. PANEL DINÁMICO CON SCROLL ---
        self.frame_scroll_container = tk.Frame(self)
        self.frame_scroll_container.pack(pady=10, padx=20, fill="both", expand=True)

        self.canvas_scroll = tk.Canvas(self.frame_scroll_container, highlightthickness=0)
        self.canvas_scroll.pack(side="left", fill="both", expand=True)

        self.scrollbar_v = ttk.Scrollbar(self.frame_scroll_container, orient="vertical", command=self.canvas_scroll.yview)
        self.scrollbar_v.pack(side="right", fill="y")
        self.canvas_scroll.configure(yscrollcommand=self.scrollbar_v.set)

        self.contenedor_columnas = tk.Frame(self.canvas_scroll)
        self.canvas_window = self.canvas_scroll.create_window((0, 0), window=self.contenedor_columnas, anchor="nw")

        self.contenedor_columnas.bind("<Configure>", lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all")))
        self.canvas_scroll.bind("<Configure>", lambda e: self.canvas_scroll.itemconfig(self.canvas_window, width=e.width))

        self.columna_bombillas = tk.LabelFrame(self.contenedor_columnas, text="💡 BOMBILLAS", fg="blue")
        self.columna_bombillas.pack(side="left", fill="both", expand=True, padx=5)

        self.columna_aires = tk.LabelFrame(self.contenedor_columnas, text="❄️ AIRES ACONDICIONADOS", fg="red")
        self.columna_aires.pack(side="right", fill="both", expand=True, padx=5)

        # --- 6. BOTÓN SALIR ---
        self.botonSalir = tk.Button(self, text="Salir y Guardar Todo", height=2, bg="#eee")
        self.botonSalir.pack(pady=10, fill="x", padx=20)

    def actualizar_area_texto_log(self, texto):
        # Suponiendo que tienes un widget de texto llamado 'self.area_log'
        self.area_log.config(state="normal")  # Habilitar edición
        self.area_log.delete("1.0", "end")  # Limpiar contenido previo
        self.area_log.insert("1.0", texto)  # Insertar el nuevo log
        self.area_log.config(state="disabled")  # Bloquear para que sea solo lectura

    def ejecutar_ver_log(self):
        """Lee el archivo y pide a la vista que abra la ventana de lectura."""
        fichero = "log_Dormitorio.txt"
        try:
            # Intentamos leer el archivo
            with open(fichero, "r", encoding="utf-8") as f:
                contenido = f.read()

            # Si hay contenido, abrimos la ventana
            self.vista.mostrar_ventana_log(contenido)

        except FileNotFoundError:
            # En lugar de print, podrías usar un messagebox de la vista
            from tkinter import messagebox
            messagebox.showwarning("Archivo no encontrado", "Aún no se ha generado ningún log histórico.")
        except Exception as e:
            raise RuntimeError(f"No se pudo leer el historial: {e}")

    def mostrar_ventana_log(self, contenido_log):
        """Crea una ventana emergente para visualizar el historial."""
        ventana_log = tk.Toplevel(self.root)  # 'self.root' o como se llame tu ventana principal
        ventana_log.title("Historial de Estados - Log")
        ventana_log.geometry("600x400")

        # Widget de texto con scroll integrado
        area_texto = scrolledtext.ScrolledText(ventana_log, wrap=tk.WORD, font=("Consolas", 10))
        area_texto.pack(expand=True, fill='both', padx=10, pady=10)

        # Insertar el texto y bloquear edición
        area_texto.insert(tk.INSERT, contenido_log)
        area_texto.config(state=tk.DISABLED)