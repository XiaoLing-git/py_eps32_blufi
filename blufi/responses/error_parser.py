""""""

from blufi.errors import BlufiBaseException
from blufi.models.base_models import ErrorCode


class ErrorParser:
    """Error Parser"""

    def __init__(self, data: str) -> None:
        """init."""
        self.__content = data
        assert len(self.content) == 2

    @property
    def content(self) -> str:
        """content"""
        return self.__content

    @property
    def error(self) -> None:
        """error"""
        value = int.from_bytes(bytes.fromhex(self.content), byteorder="little")
        raise BlufiBaseException(ErrorCode.map_obj(value).name)
