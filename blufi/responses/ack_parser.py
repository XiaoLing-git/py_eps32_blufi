""""""

from .parser import Parser


class AckParser(Parser):
    """Ack Parser"""

    def __init__(self, format_sn: str, data: str) -> None:
        """init."""
        super().__init__(data)
        self.__sn = format_sn

    def assert_sn(self) -> None:
        """assert sn"""
        assert self.__sn == self.content
