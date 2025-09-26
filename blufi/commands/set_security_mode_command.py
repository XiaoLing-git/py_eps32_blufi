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
    SecurityMode,
    TypeField,
)
from ..serial_number import SerialNumber
from . import AckCommand


class SetSecurityModeCommand(AckCommand):
    """SetSecurityModeCommand"""

    __slots__ = ("cmd",)

    def __init__(
        self,
        data_frame: SecurityMode = SecurityMode.No_Checksum_No_Encryption,
        control_frame: SecurityMode = SecurityMode.No_Checksum_No_Encryption,
        encryption: Encryption = Encryption.disable,
        crc_check: CrcCheck = CrcCheck.disable,
        direction: Direction = Direction.device_to_esp,
        ack: Ack = Ack.enable,
        sector_data: Sector_Data = Sector_Data.disable,
    ) -> None:
        """init."""

        self.cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Control, func_code=ControlAddress.SET_SEC_MODE),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_data=sector_data,
            ),
            sn=SerialNumber().obj,
            data=self.__data(data_frame, control_frame),
        )

    def __data(self, data_frame: SecurityMode, control_frame: SecurityMode) -> str:
        """format data"""
        data_frame_value = (data_frame.value << 4) & 0xF0
        control_frame_value = control_frame.value & 0x0F
        value = data_frame_value | control_frame_value
        return int.to_bytes(value, byteorder="little", length=1).hex()

    @property
    def sn(self) -> str:
        """SN"""
        return self.cmd.sn

    @property
    def data_length(self) -> int:
        """data_length"""
        return self.cmd.data_length
