""""""

from typing import Any

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

    def assert_status(self) -> None:
        """assert status"""
        if self.pocket_type.func_code is DataAddress.ERROR:
            data = int.from_bytes(bytes.fromhex(self.__content[8:10]), byteorder="little")
            error_code = ErrorCode.map_obj(data)
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
        if self.data_length == 0:
            return ""
        return self.__content[8 : (8 + 2 * self.data_length)]


class ResponseParser(BlufiResponse):
    """Response Parser"""

    def parser(self) -> Any:
        """parse"""
        self.assert_status()
        match self.pocket_type.func_code:
            case ControlAddress.ACK:
                return self.data
            case ControlAddress.SET_SEC_MODE:
                return None
            case ControlAddress.SET_OP_MODE:
                return None
            case ControlAddress.CONNECT_WIFI:
                return None
            case ControlAddress.GET_WIFI_STATUS:
                return None
            case ControlAddress.DEAUTHENTICATE:
                return None
            case ControlAddress.GET_VERSION:
                return None
            case ControlAddress.CLOSE_CONNECTION:
                return None
            case ControlAddress.GET_WIFI_LIST:
                return None

            case DataAddress.NEG:
                return None
            case DataAddress.STA_WIFI_BSSID:
                return None
            case DataAddress.STA_WIFI_SSID:
                return None
            case DataAddress.STA_WIFI_PASSWORD:
                return None
            case DataAddress.SOFTAP_WIFI_SSID:
                return None
            case DataAddress.SOFTAP_WIFI_PASSWORD:
                return None
            case DataAddress.SOFTAP_MAX_CONNECTION_COUNT:
                return None
            case DataAddress.SOFTAP_AUTH_MODE:
                return None
            case DataAddress.SOFTAP_CHANNEL:
                return None

            case DataAddress.USERNAME:
                return None
            case DataAddress.CA_CERTIFICATION:
                return None
            case DataAddress.CLIENT_CERTIFICATION:
                return None
            case DataAddress.SERVER_CERTIFICATION:
                return None
            case DataAddress.CLIENT_PRIVATE_KEY:
                return None
            case DataAddress.SERVER_PRIVATE_KEY:
                return None
            case DataAddress.WIFI_CONNECTION_STATE:
                return None
            case DataAddress.VERSION:
                return None
            case DataAddress.WIFI_LIST:
                return None
            case DataAddress.ERROR:
                return None
            case DataAddress.CUSTOM_DATA:
                return None
            case DataAddress.WIFI_STA_MAX_CONN_RETRY:
                return None
            case DataAddress.WIFI_STA_CONN_END_REASON:
                return None
            case DataAddress.WIFI_STA_CONN_RSSI:
                return None
        return None


if __name__ == "__main__":
    res = ResponseParser()
    print(res.pocket_type)
    print(res.frame_control)
    print(res.data_length)
    print(res.sn)
    print(res.data)
    res.parser()
