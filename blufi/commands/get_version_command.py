""""""

from ..models import (
    Ack,
    ControlAddress,
    ControlCommand,
    CrcCheck,
    Direction,
    Encryption,
    FrameControl,
    PocketType,
    Sector_Data,
    TypeField,
)
from ..serial_number import SerialNumber
from . import AckCommand


class GetVersionCommand(AckCommand):
    """GetVersionCommand"""

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
            pocket_type=PocketType(type_field=TypeField.Control, func_code=ControlAddress.GET_VERSION),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_Data=sector_data,
            ),
            sn=SerialNumber().obj,
        )

    @property
    def sn(self) -> str:
        """SN"""
        return self.__cmd.sn

    @property
    def data_length(self) -> int:
        """data_length"""
        return self.__cmd.data_length

    def __str__(self) -> str:
        """__str__"""
        return self.__cmd.hex()
