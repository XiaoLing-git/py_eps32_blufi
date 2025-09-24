""""""

from typing import Union

from .ack_parser import AckParser
from .custom_data_parser import CustomDataParser
from .error_parser import ErrorParser
from .parser import Parser
from .response import BlufiResponse
from .version_parser import VersionParser
from .wifi_status_parser import WifiStatusParser

Response_Parser_Type = Union[
    AckParser,
    CustomDataParser,
    ErrorParser,
    Parser,
    VersionParser,
    WifiStatusParser,
    BlufiResponse,
]


__all__ = (
    "AckParser",
    "CustomDataParser",
    "ErrorParser",
    "Parser",
    "VersionParser",
    "WifiStatusParser",
    "BlufiResponse",
)
