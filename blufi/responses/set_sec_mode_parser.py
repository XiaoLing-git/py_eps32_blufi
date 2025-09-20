""""""

from ..models.base_models import SecurityMode
from .parser import Parser


class SetSecurityModeParser(Parser):
    """Set Security Mode Parser"""

    @property
    def control(self) -> SecurityMode:
        """control"""
        value = int.from_bytes(bytes.fromhex(self.content), byteorder="little")
        value = (0xF0 & value) >> 4
        return SecurityMode.map_obj(value)

    @property
    def data(self) -> SecurityMode:
        """data"""
        value = int.from_bytes(bytes.fromhex(self.content), byteorder="little")
        value = 0x0F & value
        return SecurityMode.map_obj(value)
