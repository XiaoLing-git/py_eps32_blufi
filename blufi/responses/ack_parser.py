""""""

from .parser import Parser


class AckParser(Parser):
    """Ack Parser"""

    @property
    def response_sn(self) -> str:
        """sn"""
        return self.content

    def __str__(self) -> str:
        """str"""
        return f"{self.__class__.__name__}(response_sn={self.response_sn}, content={self.content})"
