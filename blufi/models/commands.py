""""""

from typing import Any

from pydantic import BaseModel

from blufi.crc import CRC16
from blufi.errors import GenerateCommandException
from blufi.models.base_models import (
    Ack,
    ControlAddress,
    CrcCheck,
    DataAddress,
    Direction,
    Encryption,
    Sector_Data,
    TypeField,
)
from blufi.serial_number import SerialNumber


class PocketType(BaseModel):  # type: ignore[misc]
    """Pocket Type"""

    type_field: TypeField
    func_code: ControlAddress | DataAddress

    def model_post_init(self, context: Any, /) -> None:
        """model post init"""
        if self.type_field is TypeField.Control:
            if not isinstance(self.func_code, ControlAddress):
                raise GenerateCommandException(f"{self.func_code} is not {ControlAddress}")
        if self.type_field is TypeField.Data:
            if not isinstance(self.func_code, DataAddress):
                raise GenerateCommandException(f"{self.func_code} is not {DataAddress}")

    def hex(self) -> str:
        """hex to str"""
        value = self.type_field.value | self.func_code.value
        return f"{value:02X}"


class FrameControl(BaseModel):  # type: ignore[misc]
    """Frame Control"""

    encryption: Encryption
    crc_check: CrcCheck
    direction: Direction
    ack: Ack
    sector_Data: Sector_Data

    def hex(self) -> str:
        """hex to str"""
        value = (
            self.encryption.value
            | self.crc_check.value
            | self.direction.value
            | self.ack.value
            | self.sector_Data.value
        )
        return f"{value:02X}"


class BaseDataModels(BaseModel):  # type: ignore[misc]
    """Base Data Model"""

    pocket_type: PocketType
    frame_control: FrameControl
    data_length: int = 0
    sn: str
    crc: str | None = None

    def model_post_init(self, context: Any, /) -> None:
        """model_post_init"""
        assert self.frame_control.sector_Data is Sector_Data.disable
        self.generate_crc()

    def generate_crc(self) -> None:
        """generate crc"""
        self.crc = CRC16.calculate(
            f"{self.pocket_type.hex()}{self.frame_control.hex()}{self.sn}{self.data_length_hex()}"
        )
        assert len(self.crc) == 4

    def data_length_hex(self) -> str:
        """hex data length to str"""
        return int.to_bytes(self.data_length, byteorder="little", length=1).hex()

    def __str__(self) -> str:
        """__str__"""
        return f"{self.pocket_type.hex()}{self.frame_control.hex()}{self.sn}{self.data_length_hex()}{self.crc}".lower()


class ControlCommand(BaseDataModels):
    """Control Command"""

    def __str__(self) -> str:
        """__str__"""
        return f"{self.pocket_type.hex()}{self.frame_control.hex()}{self.sn}{self.data_length_hex()}{self.crc}".lower()


class ControlCommandWithData(BaseDataModels):
    """Control Command With Data"""

    data: str

    def model_post_init(self, context: Any, /) -> None:
        """model_post_init"""
        assert self.frame_control.sector_Data is Sector_Data.disable
        self.data_length = len(self.data)
        self.generate_crc()

    def generate_crc(self) -> None:
        """generate crc"""
        self.crc = CRC16.calculate(
            f"{self.pocket_type.hex()}{self.frame_control.hex()}{self.sn}{self.data_length_hex()}{self.data_hex()}"
        )
        assert len(self.crc) == 4

    def data_hex(self) -> str:
        """hex data to str"""
        return self.data.encode().hex()

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.pocket_type.hex()}"
            f"{self.frame_control.hex()}"
            f"{self.sn}"
            f"{self.data_length_hex()}"
            f"{self.data_hex()}{self.crc}"
        ).lower()


class ControlCommandWithLargeData(BaseDataModels):
    """Control Command With Large Data"""

    remain_length: int
    data: str

    def model_post_init(self, context: Any, /) -> None:
        """model_post_init"""
        assert self.frame_control.sector_Data is Sector_Data.enable
        self.data_length = len(self.data) - 2
        self.generate_crc()

    def generate_crc(self) -> None:
        """generate crc"""
        self.crc = CRC16.calculate(
            f"{self.pocket_type.hex()}"
            f"{self.frame_control.hex()}"
            f"{self.sn}"
            f"{self.data_length_hex()}"
            f"{self.remain_data_length_hex()}"
            f"{self.data_hex()}"
        )
        assert len(self.crc) == 4

    def remain_data_length_hex(self) -> str:
        """hex data length to str"""
        return int.to_bytes(self.remain_length, byteorder="little", length=2).hex()

    def data_length_hex(self) -> str:
        """hex data length to str"""
        return int.to_bytes(self.data_length, byteorder="little", length=1).hex()

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.pocket_type.hex()}"
            f"{self.frame_control.hex()}"
            f"{self.sn}"
            f"{self.data_length_hex()}"
            f"{self.remain_data_length_hex()}"
            f"{self.data_hex()}"
            f"{self.crc}"
        ).lower()


class BaseResponse(BaseDataModels):
    """Base response"""


if __name__ == "__main__":

    bc = ControlCommandWithData(
        pocket_type=PocketType(type_field=TypeField.Data, func_code=DataAddress.STA_WIFI_BSSID),
        frame_control=FrameControl(
            encryption=Encryption.enable,
            crc_check=CrcCheck.disable,
            direction=Direction.device_to_esp,
            ack=Ack.disable,
            sector_Data=Sector_Data.enable,
        ),
        data="hello world",
    )
    print(bc)
