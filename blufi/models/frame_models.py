"""frame_models.py"""

from typing import Any

from pydantic import BaseModel

from ..errors import GenerateCommandException
from ..security import CRC16
from .base_models import Ack, ControlAddress, CrcCheck, DataAddress, Direction, Encryption, Sector_Data, TypeField


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

    def __str__(self) -> str:
        """__str__"""
        return f"{self.__class__.__name__}(type_field={self.type_field}, func_code={self.func_code})"


class FrameControl(BaseModel):  # type: ignore[misc]
    """Frame Control"""

    encryption: Encryption
    crc_check: CrcCheck
    direction: Direction
    ack: Ack
    sector_data: Sector_Data

    def hex(self) -> str:
        """hex to str"""
        value = (
            self.encryption.value
            | self.crc_check.value
            | self.direction.value
            | self.ack.value
            | self.sector_data.value
        )
        return f"{value:02X}"

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.__class__.__name__}("
            f"encryption={self.encryption}, "
            f"crc_check={self.crc_check}, "
            f"direction={self.direction}, "
            f"ack={self.ack}, "
            f"sector_data={self.sector_data}"
            f")"
        )


class BaseDataModels(BaseModel):  # type: ignore[misc]
    """Base Data Model"""

    pocket_type: PocketType
    frame_control: FrameControl
    data_length: int = 0
    sn: str
    crc: str | None = None

    def model_post_init(self, context: Any, /) -> None:
        """model_post_init"""
        assert self.frame_control.sector_data is Sector_Data.disable
        if self.frame_control.crc_check is CrcCheck.enable:
            self.generate_crc()

    def generate_crc(self) -> None:
        """generate crc"""
        self.crc = CRC16.calculate(
            f"{self.pocket_type.hex()}{self.frame_control.hex()}{self.sn}{self.data_length_hex()}"
        )
        assert len(self.crc) == 4

    def data_length_hex(self) -> str:
        """hex data length to str"""
        try:
            result = int.to_bytes(self.data_length, byteorder="little", length=1).hex()
        except OverflowError:
            result = "ff"
        return result

    def hex(self) -> str:
        """hex"""
        if self.frame_control.crc_check is CrcCheck.disable:
            return f"{self.pocket_type.hex()}{self.frame_control.hex()}{self.sn}{self.data_length_hex()}".lower()
        return (
            f"{self.pocket_type.hex()}"
            f"{self.frame_control.hex()}"
            f"{self.sn}"
            f"{self.data_length_hex()}"
            f"{self.crc}"
        ).lower()

    def __str__(self) -> str:
        """__str__"""
        if self.frame_control.crc_check is CrcCheck.enable:
            return (
                f"{self.__class__.__name__}("
                f"pocket_type={self.pocket_type}, "
                f"frame_control={self.frame_control}, "
                f"data_length={self.data_length}, "
                f"sn={self.sn}, "
                f"crc={self.crc}"
                f")"
            )
        else:
            return (
                f"{self.__class__.__name__}("
                f"pocket_type={self.pocket_type}, "
                f"frame_control={self.frame_control}, "
                f"data_length={self.data_length}, "
                f"sn={self.sn}"
                f")"
            )


class ControlCommand(BaseDataModels):
    """Control Command"""


class ControlCommandWithData(BaseDataModels):
    """Control Command With Data"""

    data: str

    def model_post_init(self, context: Any, /) -> None:
        """model_post_init"""
        assert self.frame_control.sector_data is Sector_Data.disable
        self.data_length = int(len(self.data) / 2)
        if self.frame_control.crc_check is CrcCheck.enable:
            self.generate_crc()

    def generate_crc(self) -> None:
        """generate crc"""
        self.crc = CRC16.calculate(
            f"{self.pocket_type.hex()}{self.frame_control.hex()}{self.sn}{self.data_length_hex()}{self.data}"
        )
        assert len(self.crc) == 4

    def hex(self) -> str:
        """hex"""
        if self.frame_control.crc_check is CrcCheck.disable:
            return (
                f"{self.pocket_type.hex()}"
                f"{self.frame_control.hex()}"
                f"{self.sn}"
                f"{self.data_length_hex()}"
                f"{self.data}"
            ).lower()
        return (
            f"{self.pocket_type.hex()}"
            f"{self.frame_control.hex()}"
            f"{self.sn}"
            f"{self.data_length_hex()}"
            f"{self.data}{self.crc}"
        ).lower()

    def __str__(self) -> str:
        """__str__"""
        if self.frame_control.crc_check is CrcCheck.enable:
            return (
                f"{self.__class__.__name__}("
                f"pocket_type={self.pocket_type}, "
                f"frame_control={self.frame_control}, "
                f"data_length={self.data_length}, "
                f"sn={self.sn}, "
                f"data={self.data}"
                f"crc={self.crc}"
                f")"
            )
        else:
            return (
                f"{self.__class__.__name__}("
                f"pocket_type={self.pocket_type}, "
                f"frame_control={self.frame_control}, "
                f"data_length={self.data_length}, "
                f"sn={self.sn}, "
                f"data={self.data}"
                f")"
            )


class ControlCommandWithLargeData(BaseDataModels):
    """Control Command With Large Data"""

    remain_length: int
    data: str

    def model_post_init(self, context: Any, /) -> None:
        """model_post_init"""
        assert self.frame_control.sector_Data is Sector_Data.enable
        self.data_length = int(len(self.data) / 2) + 4
        if self.frame_control.crc_check is CrcCheck.enable:
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

    def hex(self) -> str:
        """hex"""
        if self.frame_control.crc_check is CrcCheck.disable:
            return (
                f"{self.pocket_type.hex()}"
                f"{self.frame_control.hex()}"
                f"{self.sn}"
                f"{self.data_length_hex()}"
                f"{self.remain_data_length_hex()}"
                f"{self.data_hex()}"
            ).lower()
        return (
            f"{self.pocket_type.hex()}"
            f"{self.frame_control.hex()}"
            f"{self.sn}"
            f"{self.data_length_hex()}"
            f"{self.remain_data_length_hex()}"
            f"{self.data_hex()}{self.crc}"
        ).lower()

    def __str__(self) -> str:
        """__str__"""
        if self.frame_control.crc_check is CrcCheck.enable:
            return (
                f"{self.__class__.__name__}("
                f"pocket_type={self.pocket_type}, "
                f"frame_control={self.frame_control}, "
                f"data_length={self.data_length}, "
                f"sn={self.sn}, "
                f"remain_length={self.remain_length}, "
                f"data={self.data}"
                f"crc={self.crc}"
                f")"
            )
        else:
            return (
                f"{self.__class__.__name__}("
                f"pocket_type={self.pocket_type}, "
                f"frame_control={self.frame_control}, "
                f"data_length={self.data_length}, "
                f"sn={self.sn}, "
                f"remain_length={self.remain_length}, "
                f"data={self.data}"
                f")"
            )
