""""""

from pydantic import BaseModel

# class BlufiBaseModel(BaseModel):
#     """base model for SecurityMode."""
#
#     pass


class ControlAddress(BaseModel):  # type: ignore[misc]
    """base model for SecurityMode."""

    ACK = 0x00
    SET_SEC_MODE = 0x01
    SET_OP_MODE = 0x02
    CONNECT_WIFI = 0x03
    DISCONNECT_WIFI = 0x04
    GET_WIFI_STATUS = 0x05
    DEAUTHENTICATE = 0x06
    GET_VERSION = 0x07
    CLOSE_CONNECTION = 0x08
    GET_WIFI_LIST = 0x09


class DataAddress(BaseModel):  # type: ignore[misc]
    """base model for SecurityMode."""

    NEG = 0x00
    STA_WIFI_BSSID = 0x01
    STA_WIFI_SSID = 0x02
    STA_WIFI_PASSWORD = 0x03
    SOFTAP_WIFI_SSID = 0x04
    SOFTAP_WIFI_PASSWORD = 0x05
    SOFTAP_MAX_CONNECTION_COUNT = 0x06
    SOFTAP_AUTH_MODE = 0x07
    SOFTAP_CHANNEL = 0x08
    USERNAME = 0x09
    CA_CERTIFICATION = 0x0A
    CLIENT_CERTIFICATION = 0x0B
    SERVER_CERTIFICATION = 0x0C
    CLIENT_PRIVATE_KEY = 0x0D
    SERVER_PRIVATE_KEY = 0x0E
    WIFI_CONNECTION_STATE = 0x0F
    VERSION = 0x10
    WIFI_LIST = 0x11
    ERROR = 0x12
    CUSTOM_DATA = 0x13
    WIFI_STA_MAX_CONN_RETRY = 0x14
    WIFI_STA_CONN_END_REASON = 0x15
    WIFI_STA_CONN_RSSI = 0x16


class ErrorCode(BaseModel):  # type: ignore[misc]
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


class SecurityMode(BaseModel):  # type: ignore[misc]
    """base model for SecurityMode."""

    No_Checksum_No_Encryption = 0x00
    Checksum_No_Encryption = 0x01
    No_Checksum_Encryption = 0x02
    Checksum_Encryption = 0x03


class WifiOpMode(BaseModel):  # type: ignore[misc]
    """base model for WifiOpMode."""

    NULL = 0x00
    STA = 0x01
    SOFT_AP = 0x02
    SOFT_AP_AND_STA = 0x03


class SoftAPMode(BaseModel):  # type: ignore[misc]
    """base model for SoftAPMode."""

    OPEN = 0x00
    WEP = 0x01
    WPA_PSK = 0x02
    WPA2_PSK = 0x03
    WPA_WPA2_PSK = 0x04
