from abc import ABC, abstractmethod

class ILogHistorico(ABC):
    """Interfaz para clases que mantienen un log del estado en un fichero."""

    @abstractmethod
    def guardaLog(self, fichero: str):
        """
        Almacena la fecha actual y el estado de todos los dispositivos
        de la habitación en el fichero especificado.
        """
        pass