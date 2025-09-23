""""""

from typing import Any

from blufi.commands.commands_models import FrameControl, PocketType
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
from blufi.responses.ack_parser import AckParser
from blufi.responses.custom_data_parser import CustomDataParser
from blufi.responses.parser import Parser
from blufi.responses.version_parser import VersionParser
from blufi.responses.wifi_status_parser import WifiStatusParser


class BlufiResponse:
    """Blufi Response"""

    def __init__(self, content: str):
        """BlufiResponse init"""
        self.__content = content
        # print("response: ", self.__content, self.data)

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
        return self.__content[4:6]

    @property
    def data_length(self) -> int:
        """data length"""
        return int.from_bytes(bytes.fromhex(self.__content[6:8]), byteorder="little")

    @property
    def data(self) -> str:
        """data"""
        if self.data_length == 0:
            return ""
        else:
            if self.frame_control.crc_check is CrcCheck.enable:
                temp_data = self.__content[8:-4]
            else:
                temp_data = self.__content[8:]
            return temp_data

    def is_vector(self) -> bool:
        """is_vector"""
        if self.frame_control.sector_Data is Sector_Data.enable:
            return True
        else:
            return False

    def __str__(self) -> str:
        """__str__"""
        if self.data_length == 0:
            return (
                f"{self.__class__.__name__}("
                f"pocket_type = {self.pocket_type}, "
                f"frame_control = {self.frame_control}, "
                f"length = {self.data_length}, "
                f"sn = {self.sn}"
                f")"
            )
        return (
            f"{self.__class__.__name__}("
            f"pocket_type = {self.pocket_type}, "
            f"frame_control = {self.frame_control}, "
            f"length = {self.data_length}, "
            f"sn = {self.sn}, "
            f"data = {self.data}"
            f")"
        )

    def parser(self) -> Any:
        """parse"""
        match self.pocket_type.func_code:
            case ControlAddress.ACK:
                return AckParser(self.data)
            case DataAddress.VERSION:
                return VersionParser(self.data)
            case DataAddress.CUSTOM_DATA:
                return CustomDataParser(self.data)
            case DataAddress.WIFI_CONNECTION_STATE:
                return WifiStatusParser(self.data)

        return Parser(self.data)
