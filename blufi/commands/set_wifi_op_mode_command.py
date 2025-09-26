""""""

from ..models import (
    Ack,
    ControlAddress,
    ControlCommandWithData,
    CrcCheck,
    Direction,
    Encryption,
    FrameControl,
    PocketType,
    Sector_Data,
    TypeField,
    WifiOpMode,
)
from ..serial_number import SerialNumber
from . import AckCommand


class SetWifiOpModeCommand(AckCommand):
    """SetWifiOpModeCommand"""

    __slots__ = ("cmd",)

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

        self.cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Control, func_code=ControlAddress.SET_OP_MODE),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_data=sector_data,
            ),
            sn=SerialNumber().obj,
            data=int.to_bytes(wifi_mode.value, byteorder="little", length=1).hex(),
        )

    @property
    def sn(self) -> str:
        """SN"""
        return self.cmd.sn

    @property
    def data_length(self) -> int:
        """data_length"""
        return self.cmd.data_length
