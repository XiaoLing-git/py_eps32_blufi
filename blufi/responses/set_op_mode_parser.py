""""""

from ..models.base_models import WifiOpMode
from .parser import Parser


class SetWifiOpModeParser(Parser):
    """Set Wifi Op Mode Parser"""

    @property
    def mode(self) -> WifiOpMode:
        """mode"""
        value = int.from_bytes(bytes.fromhex(self.content), byteorder="little")
        return WifiOpMode.map_obj(value)
