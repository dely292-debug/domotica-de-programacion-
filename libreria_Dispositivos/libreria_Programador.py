import time
from typing import List, Dict, Tuple, Any


class Programador:
    """
    Simula la clase Programador para agendar acciones de ON/OFF
    para cualquier Dispositivo (Bombilla o Aire).
    """
    _DIAS_SEMANA_MAP = {
        0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
        4: "Viernes", 5: "Sábado", 6: "Domingo"
    }

    def __init__(self, dispositivo_objetivo: Any):
        # Almacena el objeto Bombilla o Aire al que debe programar
        self.dispositivo_objetivo = dispositivo_objetivo
        # (Dia, Hora, Minuto, Segundo): Accion ('ON' o 'OFF')
        self.listaProgramacion: Dict[Tuple[str, int, int, int], str] = {}

    @staticmethod
    def _validar_tiempo(h, m, s) -> bool:
        """Función auxiliar para validar horas, minutos y segundos."""
        return 0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59

    @classmethod
    def getDiasSemana(cls) -> List[str]:
        """Devuelve una lista con los nombres válidos de los días de la semana."""
        return list(cls._DIAS_SEMANA_MAP.values())

    @classmethod
    def getHoraSistema(cls) -> str:
        """Devuelve la hora actual del sistema en formato: DiaDeLaSemana HH:MM:SS."""
        lt = time.localtime()
        dia = cls._DIAS_SEMANA_MAP.get(lt.tm_wday)
        hora = f"{lt.tm_hour:02d}:{lt.tm_min:02d}:{lt.tm_sec:02d}"
        return f"{dia} {hora}"

    def comienzo(self, diaSemana: str, hora: int, min: int, seg: int):
        """Programa el encendido (ON) del dispositivo."""
        dia_semana_normalizado = diaSemana.capitalize()
        if dia_semana_normalizado not in Programador.getDiasSemana():
            print(f" Error: Día '{diaSemana}' no válido.")
            return
        if not self._validar_tiempo(hora, min, seg):
            print(" Error: Hora, minuto o segundo fuera de rango.")
            return
        clave = (dia_semana_normalizado, hora, min, seg)
        self.listaProgramacion[clave] = 'ON'
        tiempo_str = f"{hora:02d}:{min:02d}:{seg:02d}"
        print(
            f" Programación añadida: '{self.dispositivo_objetivo}' ON el {dia_semana_normalizado} a las {tiempo_str}.")

    def fin(self, diaSemana: str, hora: int, min: int, seg: int):
        """Programa el apagado (OFF) del dispositivo."""
        dia_semana_normalizado = diaSemana.capitalize()
        if dia_semana_normalizado not in Programador.getDiasSemana():
            print(f"Error: Día '{diaSemana}' no válido.")
            return
        if not self._validar_tiempo(hora, min, seg):
            print("Error: Hora, minuto o segundo fuera de rango.")
            return
        clave = (dia_semana_normalizado, hora, min, seg)
        self.listaProgramacion[clave] = 'OFF'
        tiempo_str = f"{hora:02d}:{min:02d}:{seg:02d}"
        print(
            f"Programación añadida: '{self.dispositivo_objetivo}' OFF el {dia_semana_normalizado} a las {tiempo_str}.")

    def borrar(self, diaSemana: str, hora: int, min: int, seg: int):
        """Borra una programación específica."""
        clave = (diaSemana.capitalize(), hora, min, seg)
        tiempo_str = f"{hora:02d}:{min:02d}:{seg:02d}"
        if clave in self.listaProgramacion:
            accion = self.listaProgramacion.pop(clave)
            print(f" Programación borrada: '{self.dispositivo_objetivo}' {accion} el {clave[0]} a las {tiempo_str}.")
        else:
            print(f"No se encontró programación para el {clave[0]} a las {tiempo_str}.")

    def mostrar_programacion(self):
        """Muestra la programación actual."""
        if not self.listaProgramacion:
            print(f"No hay programaciones activas para '{self.dispositivo_objetivo}'.")
            return
        print(f"\n--- Programación de '{self.dispositivo_objetivo}' ---")
        for (dia, h, m, s), accion in sorted(self.listaProgramacion.items()):
            tiempo_str = f"{h:02d}:{m:02d}:{s:02d}"
            print(f"- {dia} {tiempo_str}: {accion}")

    def ejecutar_programacion(self):
        """Comprueba la hora actual y ejecuta la acción si coincide."""
        lt = time.localtime()
        dia_actual = Programador._DIAS_SEMANA_MAP.get(lt.tm_wday)
        clave_actual = (dia_actual, lt.tm_hour, lt.tm_min, lt.tm_sec)

        if clave_actual in self.listaProgramacion:
            accion = self.listaProgramacion[clave_actual]
            tiempo_str = f"{lt.tm_hour:02d}:{lt.tm_min:02d}:{lt.tm_sec:02d}"
            print(f"\n[PROGRAMADOR] ¡Hora de acción! {clave_actual[0]} {tiempo_str} -> {accion}")

            if accion == 'ON':
                self.dispositivo_objetivo.encender()
            elif accion == 'OFF':
                self.dispositivo_objetivo.apagar()