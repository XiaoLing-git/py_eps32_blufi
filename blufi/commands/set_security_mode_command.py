""""""

from ..models.base_models import (
    Ack,
    ControlAddress,
    CrcCheck,
    Direction,
    Encryption,
    Sector_Data,
    SecurityMode,
    TypeField,
)
from ..models.commands_models import ControlCommandWithData, FrameControl, PocketType
from ..serial_number import SerialNumber


class SetSecurityModeCommand:
    """SetSecurityModeCommand"""

    def __init__(
        self,
        encryption: Encryption = Encryption.disable,
        crc_check: CrcCheck = CrcCheck.disable,
        direction: Direction = Direction.device_to_esp,
        ack: Ack = Ack.enable,
        sector_data: Sector_Data = Sector_Data.disable,
        data_frame: SecurityMode = SecurityMode.No_Checksum_No_Encryption,
        control_frame: SecurityMode = SecurityMode.No_Checksum_No_Encryption,
    ) -> None:
        """init."""

        self.__cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Control, func_code=ControlAddress.ACK),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_Data=sector_data,
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

    def __str__(self) -> str:
        """__str__"""
        return self.__cmd.hex()
