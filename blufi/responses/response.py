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
from blufi.responses.ack_parser import AckParser
from blufi.responses.de_authenticate_parser import DeAuthenticateParser
from blufi.responses.error_parser import ErrorParser
from blufi.responses.negotiation_parser import NegotiationParser
from blufi.responses.parser import DebugParser, Parser
from blufi.responses.set_op_mode_parser import SetWifiOpModeParser
from blufi.responses.set_sec_mode_parser import SetSecurityModeParser
from blufi.responses.wifi_connect_state_parser import WifiConnectStateParser


class BlufiResponse:
    """Blufi Response"""

    def __init__(self, content: str = "4904000100"):
        """BlufiResponse init"""
        self.__content = content
        print("response: ", self.__content, self.data)

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


class ResponseParser(BlufiResponse):
    """Response Parser"""

    def parser(self) -> Any:
        """parse"""
        match self.pocket_type.func_code:
            case ControlAddress.ACK:
                return AckParser(self.data)
            case ControlAddress.SET_SEC_MODE:
                return SetSecurityModeParser(self.data)
            case ControlAddress.SET_OP_MODE:
                return SetWifiOpModeParser(self.data)
            case ControlAddress.CONNECT_WIFI:
                return DebugParser(self.data)
            case ControlAddress.GET_WIFI_STATUS:
                return DebugParser(self.data)
            case ControlAddress.DEAUTHENTICATE:
                return DeAuthenticateParser(self.data, self.data_length)
            case ControlAddress.GET_VERSION:
                return DebugParser(self.data)
            case ControlAddress.CLOSE_CONNECTION:
                return DebugParser(self.data)
            case ControlAddress.GET_WIFI_LIST:
                return DebugParser(self.data)

            case DataAddress.NEG:
                return NegotiationParser(self.data, self.data_length)
            case DataAddress.STA_WIFI_BSSID:
                return DebugParser(self.data)
            case DataAddress.STA_WIFI_SSID:
                return DebugParser(self.data)
            case DataAddress.STA_WIFI_PASSWORD:
                return DebugParser(self.data)
            case DataAddress.SOFTAP_WIFI_SSID:
                return DebugParser(self.data)
            case DataAddress.SOFTAP_WIFI_PASSWORD:
                return DebugParser(self.data)
            case DataAddress.SOFTAP_MAX_CONNECTION_COUNT:
                return DebugParser(self.data)
            case DataAddress.SOFTAP_AUTH_MODE:
                return DebugParser(self.data)
            case DataAddress.SOFTAP_CHANNEL:
                return DebugParser(self.data)

            case DataAddress.USERNAME:
                return DebugParser(self.data)
            case DataAddress.CA_CERTIFICATION:
                return DebugParser(self.data)
            case DataAddress.CLIENT_CERTIFICATION:
                return DebugParser(self.data)
            case DataAddress.SERVER_CERTIFICATION:
                return DebugParser(self.data)
            case DataAddress.CLIENT_PRIVATE_KEY:
                return DebugParser(self.data)
            case DataAddress.SERVER_PRIVATE_KEY:
                return DebugParser(self.data)
            case DataAddress.WIFI_CONNECTION_STATE:
                p = WifiConnectStateParser(self.data)
                print("WifiConnectStateParser", p.content, p.mode, p.state, p.device_count)
                return WifiConnectStateParser(self.data)
            case DataAddress.VERSION:
                return DebugParser(self.data)
            case DataAddress.WIFI_LIST:
                return DebugParser(self.data)
            case DataAddress.ERROR:
                return ErrorParser(self.data)
            case DataAddress.CUSTOM_DATA:
                return DebugParser(self.data)
            case DataAddress.WIFI_STA_MAX_CONN_RETRY:
                return DebugParser(self.data)
            case DataAddress.WIFI_STA_CONN_END_REASON:
                return DebugParser(self.data)
            case DataAddress.WIFI_STA_CONN_RSSI:
                return DebugParser(self.data)
        return None


if __name__ == "__main__":
    res = ResponseParser()
    print(res.pocket_type)
    print(res.frame_control)
    print(res.data_length)
    print(res.sn)
    print(res.data)
    res.parser()
