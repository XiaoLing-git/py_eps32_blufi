""""""

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
        return self._msg

    def __repr__(self) -> str:
        """exception __repr__"""
        return self._msg


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
