""""""

import logging

logger = logging.getLogger(__name__)


class BlufiBaseException(Exception):
    """
    基础异常
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
