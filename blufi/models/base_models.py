""""""

from __future__ import annotations

from enum import Enum

from ..errors import EnumItemNotExistError


class TypeField(Enum):
    """
    Type Field
    """

    Control = 0x00
    Data = 0x01

    @classmethod
    def map_obj(cls, data: int) -> TypeField:
        """map obj"""
        data = data & 0x03
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class Encryption(Enum):
    """
    Encryption
    """

    disable = 0x00
    enable = 0x01

    @classmethod
    def map_obj(cls, data: int) -> Encryption:
        """map obj"""
        data = data & 0x01
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class CrcCheck(Enum):
    """
    Crc Check
    """

    disable = 0x00 << 1
    enable = 0x01 << 1

    @classmethod
    def map_obj(cls, data: int) -> CrcCheck:
        """map obj"""
        data = data & 0x02
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class Direction(Enum):
    """
    Direction
    """

    device_to_esp = 0x00 << 2
    esp_to_device = 0x01 << 2

    @classmethod
    def map_obj(cls, data: int) -> Direction:
        """map obj"""
        data = data & 0x04
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class Ack(Enum):
    """
    Ack
    """

    disable = 0x00 << 3
    enable = 0x01 << 3

    @classmethod
    def map_obj(cls, data: int) -> Ack:
        """map obj"""
        data = data & 0x08
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class Sector_Data(Enum):
    """
    Sector Data
    """

    disable = 0x00 << 4
    enable = 0x01 << 4

    @classmethod
    def map_obj(cls, data: int) -> Sector_Data:
        """map obj"""
        data = data & 0x10
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class BlufiBaseEnum(Enum):
    """base model for SecurityMode."""

    pass


class ControlAddress(BlufiBaseEnum):
    """base model for SecurityMode."""

    ACK = 0x00 << 2
    SET_SEC_MODE = 0x01 << 2
    SET_OP_MODE = 0x02 << 2
    CONNECT_WIFI = 0x03 << 2
    DISCONNECT_WIFI = 0x04 << 2
    GET_WIFI_STATUS = 0x05 << 2
    DEAUTHENTICATE = 0x06 << 2
    GET_VERSION = 0x07 << 2
    CLOSE_CONNECTION = 0x08 << 2
    GET_WIFI_LIST = 0x09 << 2

    @classmethod
    def map_obj(cls, data: int) -> ControlAddress:
        """map obj"""
        data = data & 0xFC
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class DataAddress(BlufiBaseEnum):
    """base model for SecurityMode."""

    NEG = 0x00 << 2
    STA_WIFI_BSSID = 0x01 << 2
    STA_WIFI_SSID = 0x02 << 2
    STA_WIFI_PASSWORD = 0x03 << 2
    SOFTAP_WIFI_SSID = 0x04 << 2
    SOFTAP_WIFI_PASSWORD = 0x05 << 2
    SOFTAP_MAX_CONNECTION_COUNT = 0x06 << 2
    SOFTAP_AUTH_MODE = 0x07 << 2
    SOFTAP_CHANNEL = 0x08 << 2
    USERNAME = 0x09 << 2
    CA_CERTIFICATION = 0x0A << 2
    CLIENT_CERTIFICATION = 0x0B << 2
    SERVER_CERTIFICATION = 0x0C << 2
    CLIENT_PRIVATE_KEY = 0x0D << 2
    SERVER_PRIVATE_KEY = 0x0E << 2
    WIFI_CONNECTION_STATE = 0x0F << 2
    VERSION = 0x10 << 2
    WIFI_LIST = 0x11 << 2
    ERROR = 0x12 << 2
    CUSTOM_DATA = 0x13 << 2
    WIFI_STA_MAX_CONN_RETRY = 0x14 << 2
    WIFI_STA_CONN_END_REASON = 0x15 << 2
    WIFI_STA_CONN_RSSI = 0x16 << 2

    @classmethod
    def map_obj(cls, data: int) -> DataAddress:
        """map obj"""
        data = data & 0xFC
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class ErrorCode(BlufiBaseEnum):
    """base model for SecurityMode."""

    sequence_error = 0x00
    checksum_error = 0x01
    decrypt_error = 0x02
    encrypt_error = 0x03
    init_security_error = 0x04
    dh_malloc_error = 0x05
    dh_param_error = 0x06
    read_param_error = 0x07
    make_public_error = 0x08
    data_format_error = 0x09
    calculate_md5_error = 0x0A
    wifi_scan_error = 0x0B

    @classmethod
    def map_obj(cls, data: int) -> ErrorCode:
        """map obj"""
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class SecurityMode(BlufiBaseEnum):
    """base model for SecurityMode."""

    No_Checksum_No_Encryption = 0x00
    Checksum_No_Encryption = 0x01
    No_Checksum_Encryption = 0x02
    Checksum_Encryption = 0x03

    @classmethod
    def map_obj(cls, data: int) -> SecurityMode:
        """map obj"""
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class WifiOpMode(BlufiBaseEnum):
    """base model for WifiOpMode."""

    NULL = 0x00
    STA = 0x01
    SOFT_AP = 0x02
    SOFT_AP_AND_STA = 0x03

    @classmethod
    def map_obj(cls, data: int) -> WifiOpMode:
        """map obj"""
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class WifiConnectState(BlufiBaseEnum):
    """Wifi Connect State."""

    Connected = 0x00
    Unconnected = 0x01
    Connecting = 0x02
    Connecting_no_ip = 0x03

    @classmethod
    def map_obj(cls, data: int) -> WifiConnectState:
        """map obj"""
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")


class SoftAPMode(BlufiBaseEnum):
    """base model for SoftAPMode."""

    OPEN = 0x00
    WEP = 0x01
    WPA_PSK = 0x02
    WPA2_PSK = 0x03
    WPA_WPA2_PSK = 0x04

    @classmethod
    def map_obj(cls, data: int) -> SoftAPMode:
        """map obj"""
        for item in cls:
            if item.value == data:
                return item
        raise EnumItemNotExistError(f"{cls.__name__} can't map {data:02X}")
