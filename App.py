from Vista import VentanaPrincipal
from Controlador import ControladorDomotica

if __name__ == "__main__":
    # 1. Creamos la Vista (Ventana)
    app_vista = VentanaPrincipal()

    # 2. Creamos el Controlador y le pasamos la vista
    app_controlador = ControladorDomotica(app_vista)

    # 3. Iniciamos el bucle de la aplicación
    app_vista.mainloop()