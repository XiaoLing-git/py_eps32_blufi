""""""

from ..models.base_models import (
    Ack,
    ControlAddress,
    CrcCheck,
    Direction,
    Encryption,
    Sector_Data,
    TypeField,
    WifiOpMode,
)
from ..models.commands_models import ControlCommandWithData, FrameControl, PocketType
from ..serial_number import SerialNumber


class SetWifiOpModeCommand:
    """SetWifiOpModeCommand"""

    __slots__ = ("__cmd",)

    def __init__(
        self,
        wifi_mode: WifiOpMode = WifiOpMode.NULL,
        encryption: Encryption = Encryption.disable,
        crc_check: CrcCheck = CrcCheck.disable,
        direction: Direction = Direction.device_to_esp,
        ack: Ack = Ack.enable,
        sector_data: Sector_Data = Sector_Data.disable,
    ) -> None:
        """init."""

        self.__cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Control, func_code=ControlAddress.SET_OP_MODE),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_Data=sector_data,
            ),
            sn=SerialNumber().obj,
            data=int.to_bytes(wifi_mode.value, byteorder="little", length=1).hex(),
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
