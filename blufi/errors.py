"""errors.py"""

import logging

logger = logging.getLogger(__name__)


class BlufiBaseException(Exception):
    """
    Base Exception For Blufi
    """

    def __init__(self, msg: str) -> None:
        """exception init"""
        self._msg = msg
        logger.error(f"{self.__class__.__name__} - {self._msg}")

    def __str__(self) -> str:
        """exception __str__"""
        return f"{self.__class__.__name__}(msg={self._msg})"

    def __repr__(self) -> str:
        """exception __repr__"""
        return f"{self.__class__.__name__}(msg={self._msg})"


class AsyncBlufiConnectionError(BlufiBaseException):
    """Async Blufi Connection Error."""


class AsyncBlufiDisconnectionError(BlufiBaseException):
    """Async Blufi Disconnection Error."""


class AsyncBlufiAddressFormatError(BlufiBaseException):
    """Async Blufi Address Format Error."""


class AsyncBlufiGetServiceException(BlufiBaseException):
    """Async Blufi Get Service Exception."""


class AsyncBlufiGetUUIDException(BlufiBaseException):
    """Async Blufi Get UUID Exception."""


class AsyncBlufiWriteReadException(BlufiBaseException):
    """Async Blufi Write Read Exception."""


class AsyncBlufiWriteException(AsyncBlufiWriteReadException):
    """Async Blufi Write Exception."""


class AsyncBlufiReadException(AsyncBlufiWriteReadException):
    """Async Blufi Read Exception."""


class HexStrException(BlufiBaseException):
    """Hex Str Exception."""


class GenerateCommandException(BlufiBaseException):
    """HGenerateCommandException."""


class EnumItemNotExistError(BlufiBaseException):
    """Enum Item Not Exist Error."""


class ParseResponseException(BlufiBaseException):
    """Parse Response Exception"""
