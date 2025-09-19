""""""

from blufi.errors import ParseResponseException
from blufi.models.base_models import (
    Ack,
    ControlAddress,
    CrcCheck,
    DataAddress,
    Direction,
    Encryption,
    ErrorCode,
    Sector_Data,
    TypeField,
)
from blufi.models.commands import FrameControl, PocketType


class BlufiResponse:
    """Blufi Response"""

    def __init__(self, content: str = "4904000100"):
        """BlufiResponse init"""
        self.__content = content

    def parser(self) -> None:
        """parse"""
        self.assert_status()
        print(self.pocket_type)
        print(self.frame_control)
        print(self.sn)
        print(self.data_length)
        print(self.data)

    def assert_status(self) -> None:
        """assert status"""
        if self.pocket_type.func_code is DataAddress.ERROR:
            data = int.from_bytes(bytes.fromhex(self.__content[8:10]), byteorder="little")
            error_code = ErrorCode.map_obj(data)
            print(self.pocket_type.func_code)
            raise ParseResponseException(error_code.name)

    @property
    def pocket_type(self) -> PocketType:
        """pocket type"""
        value = int.from_bytes(bytes.fromhex(self.__content[0:2]), byteorder="little")
        type_field = TypeField.map_obj(value)
        if type_field is TypeField.Data:
            return PocketType(type_field=type_field, func_code=DataAddress.map_obj(value))
        else:
            return PocketType(type_field=type_field, func_code=ControlAddress.map_obj(value))

    @property
    def frame_control(self) -> FrameControl:
        """frame control"""
        value = int.from_bytes(bytes.fromhex(self.__content[2:4]), byteorder="little")
        return FrameControl(
            encryption=Encryption.map_obj(value),
            crc_check=CrcCheck.map_obj(value),
            direction=Direction.map_obj(value),
            ack=Ack.map_obj(value),
            sector_Data=Sector_Data.map_obj(value),
        )

    @property
    def sn(self) -> str:
        """sn"""
        return self.__content[6:8]

    @property
    def data_length(self) -> int:
        """data length"""
        return int.from_bytes(bytes.fromhex(self.__content[6:8]), byteorder="little")

    @property
    def data(self) -> str:
        """data"""
        return self.__content[8 : (8 + 2 * self.data_length)]


if __name__ == "__main__":
    res = BlufiResponse()
    print(res.pocket_type)
    print(res.frame_control)
    print(res.data_length)
    print(res.sn)
    print(res.data)
    res.parser()
