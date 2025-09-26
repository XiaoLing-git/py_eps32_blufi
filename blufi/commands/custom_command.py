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


class CustomDataCommand(AckCommand):
    """CustomDataCommand"""

    __slots__ = ("cmd",)

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
        content = content.encode().hex()
        assert_hex_str(content)
        self.cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Data, func_code=DataAddress.CUSTOM_DATA),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_data=sector_data,
            ),
            sn=SerialNumber().obj,
            data=content,
        )

    @property
    def sn(self) -> str:
        """SN"""
        return self.cmd.sn

    @property
    def data_length(self) -> int:
        """data_length"""
        return self.cmd.data_length
