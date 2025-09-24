""""""

from ..models.base_models import Ack, ControlAddress, CrcCheck, Direction, Encryption, Sector_Data, TypeField
from ..serial_number import SerialNumber
from .commands_models import ControlCommandWithData, FrameControl, PocketType


class DeauthenticateCommand:
    """DeauthenticateCommand"""

    __slots__ = ("__cmd",)

    def __init__(
        self,
        devices_address: list[str],
        encryption: Encryption = Encryption.disable,
        crc_check: CrcCheck = CrcCheck.disable,
        direction: Direction = Direction.device_to_esp,
        ack: Ack = Ack.enable,
        sector_data: Sector_Data = Sector_Data.disable,
    ) -> None:
        """init."""

        self.__cmd = ControlCommandWithData(
            pocket_type=PocketType(type_field=TypeField.Control, func_code=ControlAddress.DEAUTHENTICATE),
            frame_control=FrameControl(
                encryption=encryption,
                crc_check=crc_check,
                direction=direction,
                ack=ack,
                sector_Data=sector_data,
            ),
            sn=SerialNumber().obj,
            data=self.format_devices_address(devices_address),
        )

    def format_devices_address(self, devices_address: list[str]) -> str:
        "format_devices_address"
        results: str = ""
        for address in devices_address:
            if isinstance(address, str):
                address = address.strip()
                address = address.replace(":", "")
                _length = len(address)
                if _length == 12:
                    results = results + address
                else:
                    raise ValueError(f"{self.__class__.__name__} > address[{address}] has wrong format")
            else:
                raise ValueError(f"{self.__class__.__name__} > address[{address}] has wrong format")
        return results

    def __str__(self) -> str:
        """__str__"""
        return self.__cmd.hex()
