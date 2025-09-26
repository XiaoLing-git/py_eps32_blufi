""""""

from ..models import (
    Ack,
    ControlCommandWithData,
    CrcCheck,
    DataAddress,
    Direction,
    Encryption,
    FrameControl,
    PocketType,
    Sector_Data,
    TypeField,
)
from ..serial_number import SerialNumber
from ..utils import assert_hex_str
from . import AckCommand


class StaWifiSSIDCommand(AckCommand):
    """StaWifiSSIDCommand"""

    __slots__ = (
        "__cmd",
        "__content",
    )

    def __init__(
        self,
        content: str,
        encryption: Encryption = Encryption.disable,
        crc_check: CrcCheck = CrcCheck.disable,
        direction: Direction = Direction.device_to_esp,
        ack: Ack = Ack.enable,
        sector_data: Sector_Data = Sector_Data.disable,
    ) -> None:
        """init."""
        self.__content = content
        self.__cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Data, func_code=DataAddress.STA_WIFI_SSID),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_Data=sector_data,
            ),
            sn=SerialNumber().obj,
            data=self.ssid,
        )

    @property
    def ssid(self) -> str:
        """ssid"""
        data = self.__content.encode().hex()
        assert_hex_str(data)
        return data

    def __str__(self) -> str:
        """__str__"""
        return self.__cmd.hex()
