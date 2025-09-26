""""""

from ..models import SoftAPMode, WifiConnectState, WifiOpMode
from .parser import Parser


class WifiStatusParser(Parser):
    """Wifi Status Parser"""

    def __init__(self, data: str) -> None:
        """init."""
        super().__init__(data)

    @property
    def op_mode(self) -> WifiOpMode:
        """op_mode"""
        return WifiOpMode.map_obj(int.from_bytes(bytes.fromhex(self.content[:2]), byteorder="little"))

    @property
    def sta_status(self) -> WifiConnectState:
        """op_mode"""
        return WifiConnectState.map_obj(int.from_bytes(bytes.fromhex(self.content[2:4]), byteorder="little"))

    @property
    def soft_ap_status(self) -> SoftAPMode:
        """op_mode"""
        return SoftAPMode.map_obj(int.from_bytes(bytes.fromhex(self.content[4:6]), byteorder="little"))

    @property
    def info(self) -> bytes | None:
        """info"""
        if len(self.content[6:]) > 0:
            data = bytes.fromhex(self.content[6:])
        else:
            data = None
        return data

    def __str__(self) -> str:
        """str"""
        return (
            f"{self.__class__.__name__}("
            f"op_mode={self.op_mode}, "
            f"soft_ap_status={self.soft_ap_status}, "
            f"sta_status={self.sta_status}, "
            f"info={self.info!r}"
            f")"
        )
