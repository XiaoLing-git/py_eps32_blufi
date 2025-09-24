""""""

from ..models import Ack, ControlAddress, CrcCheck, Direction, Encryption, Sector_Data, TypeField
from ..serial_number import SerialNumber
from .commands_models import ControlCommand, FrameControl, PocketType


class GetWifiListCommand:
    """GetWifiListCommand"""

    __slots__ = ("__cmd",)

    def __init__(
        self,
        encryption: Encryption = Encryption.disable,
        crc_check: CrcCheck = CrcCheck.disable,
        direction: Direction = Direction.device_to_esp,
        ack: Ack = Ack.enable,
        sector_data: Sector_Data = Sector_Data.disable,
    ) -> None:
        """init."""

        self.__cmd = ControlCommand(
            pocket_type=PocketType(type_field=TypeField.Control, func_code=ControlAddress.GET_WIFI_LIST),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_Data=sector_data,
            ),
            sn=SerialNumber().obj,
        )

    def __str__(self) -> str:
        """__str__"""
        return self.__cmd.hex()
