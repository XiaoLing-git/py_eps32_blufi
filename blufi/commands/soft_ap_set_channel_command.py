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
from . import AckCommand


class SoftApSetChannelCommand(AckCommand):
    """SoftApSetChannelCommand"""

    __slots__ = ("__cmd",)

    def __init__(
        self,
        count: int,
        encryption: Encryption = Encryption.disable,
        crc_check: CrcCheck = CrcCheck.disable,
        direction: Direction = Direction.device_to_esp,
        ack: Ack = Ack.enable,
        sector_data: Sector_Data = Sector_Data.disable,
    ) -> None:
        """init."""
        assert 0 < count < 15
        self.__cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Data, func_code=DataAddress.SOFTAP_CHANNEL),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_Data=sector_data,
            ),
            sn=SerialNumber().obj,
            data=int.to_bytes(count, byteorder="little", length=1).hex(),
        )

    def __str__(self) -> str:
        """__str__"""
        return self.__cmd.hex()
