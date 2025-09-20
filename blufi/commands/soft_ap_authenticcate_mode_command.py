""""""

from ..models.base_models import Ack, CrcCheck, DataAddress, Direction, Encryption, Sector_Data, SoftAPMode, TypeField
from ..models.commands_models import ControlCommandWithData, FrameControl, PocketType
from ..serial_number import SerialNumber
from ..utils import assert_hex_str


class SoftApAuthenticateModeCommand:
    """SoftApAuthenticateModeCommand"""

    __slots__ = ("__cmd",)

    def __init__(
        self,
        mode: SoftAPMode = SoftAPMode.OPEN,
        encryption: Encryption = Encryption.disable,
        crc_check: CrcCheck = CrcCheck.disable,
        direction: Direction = Direction.device_to_esp,
        ack: Ack = Ack.enable,
        sector_data: Sector_Data = Sector_Data.disable,
    ) -> None:
        """init."""
        self.__cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Data, func_code=DataAddress.SOFTAP_AUTH_MODE),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_Data=sector_data,
            ),
            sn=SerialNumber().obj,
            data=int.to_bytes(mode.value, byteorder="little", length=1).hex(),
        )

    def __str__(self) -> str:
        """__str__"""
        return self.__cmd.hex()
