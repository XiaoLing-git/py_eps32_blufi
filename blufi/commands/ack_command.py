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


class AckCommand:
    """AckCommand"""

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
            pocket_type=PocketType(type_field=TypeField.Control, func_code=ControlAddress.ACK),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_data=sector_data,
            ),
            sn=SerialNumber().obj,
        )

    def hex(self) -> str:
        """hex to str"""
        return self.cmd.hex()

    def __str__(self) -> str:
        """__str__"""
        if isinstance(self.cmd, ControlCommand):
            if self.cmd.frame_control.crc_check is CrcCheck.enable:
                return (
                    f"{self.__class__.__name__}("
                    f"encryption={self.cmd.frame_control.encryption}, "
                    f"crc_check={self.cmd.frame_control.crc_check}, "
                    f"ack={self.cmd.frame_control.ack}, "
                    f"sn={self.cmd.sn}, "
                    f"crc={self.cmd.crc}"
                    f")"
                )
            else:
                return (
                    f"{self.__class__.__name__}("
                    f"encryption={self.cmd.frame_control.encryption}, "
                    f"crc_check={self.cmd.frame_control.crc_check}, "
                    f"ack={self.cmd.frame_control.ack}, "
                    f"sn={self.cmd.sn}"
                    f")"
                )
        else:
            if self.cmd.frame_control.crc_check is CrcCheck.enable:
                return (
                    f"{self.__class__.__name__}("
                    f"encryption={self.cmd.frame_control.encryption}, "
                    f"crc_check={self.cmd.frame_control.crc_check}, "
                    f"ack={self.cmd.frame_control.ack}, "
                    f"sn={self.cmd.sn}, "
                    f"data={self.cmd.data}, "
                    f"crc={self.cmd.crc}"
                    f")"
                )
            else:
                return (
                    f"{self.__class__.__name__}("
                    f"encryption={self.cmd.frame_control.encryption}, "
                    f"crc_check={self.cmd.frame_control.crc_check}, "
                    f"ack={self.cmd.frame_control.ack}, "
                    f"sn={self.cmd.sn}, "
                    f"data={self.cmd.data}"
                    f")"
                )
