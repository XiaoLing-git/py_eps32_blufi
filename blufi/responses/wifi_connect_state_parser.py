""""""

from ..models.base_models import WifiConnectState, WifiOpMode
from .parser import Parser


class WifiConnectStateParser(Parser):
    """Wifi Connect State Parser"""

    @property
    def mode(self) -> WifiOpMode:
        """mode"""
        value = int.from_bytes(bytes.fromhex(self.content[:2]), byteorder="little")
        return WifiOpMode.map_obj(value)

    @property
    def state(self) -> WifiConnectState:
        """state"""
        value = int.from_bytes(bytes.fromhex(self.content[2:4]), byteorder="little")
        return WifiConnectState.map_obj(value)

    @property
    def device_count(self) -> int:
        """device count"""
        return int.from_bytes(bytes.fromhex(self.content[4:6]), byteorder="little")

    @property
    def info(self) -> str:
        """info"""
        if len(self.content) > 6:
            return self.content[6:]
        return ""
