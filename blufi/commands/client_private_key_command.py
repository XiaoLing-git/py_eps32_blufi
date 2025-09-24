""""""

from ..models.base_models import Ack, CrcCheck, DataAddress, Direction, Encryption, Sector_Data, TypeField
from ..serial_number import SerialNumber
from ..utils import assert_hex_str
from .commands_models import ControlCommandWithData, FrameControl, PocketType


class ClientPrivateKeyCommand:
    """ClientPrivateKeyCommand"""

    __slots__ = ("__cmd",)

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
        assert_hex_str(content)
        self.__cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Data, func_code=DataAddress.CLIENT_PRIVATE_KEY),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_Data=sector_data,
            ),
            sn=SerialNumber().obj,
            data=content,
        )

    def __str__(self) -> str:
        """__str__"""
        return self.__cmd.hex()
