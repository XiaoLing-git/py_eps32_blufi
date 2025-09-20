""""""

from .parser import Parser


class AckParser(Parser):
    """Ack Parser"""

    def __init__(self, format_sn: str, data: str) -> None:
        """init."""
        super().__init__(data)
        self.__sn = format_sn

        assert len(self.content) == 2
        assert self.__sn == self.content

    def sn(self) -> str:
        """sn"""
        return self.__sn
