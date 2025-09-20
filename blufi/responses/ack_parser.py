""""""

from .parser import Parser


class AckParser(Parser):
    """Ack Parser"""

    @property
    def sn(self) -> str:
        """sn"""
        return self.content
