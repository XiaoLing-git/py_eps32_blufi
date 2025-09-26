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


class BleDisconnectCommand(AckCommand):
    """BleDisconnectCommand"""

    __slots__ = ("cmd",)

    def __init__(
        self,
        encryption: Encryption = Encryption.disable,
        crc_check: CrcCheck = CrcCheck.disable,
        direction: Direction = Direction.device_to_esp,
        ack: Ack = Ack.enable,
        sector_data: Sector_Data = Sector_Data.disable,
    ) -> None:
        """init."""

        self.cmd = ControlCommand(
            pocket_type=PocketType(type_field=TypeField.Control, func_code=ControlAddress.CLOSE_CONNECTION),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_data=sector_data,
            ),
            sn=SerialNumber().obj,
        )
