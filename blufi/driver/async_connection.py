"""Async Blufi Connection."""

import asyncio
import logging

from async_timeout import timeout as as_timeout
from bleak import BleakClient

from ..errors import AsyncBlufiConnectionError, AsyncBlufiDisconnectionError
from ..utils import format_mac_address

logger = logging.getLogger(__name__)


class AsyncBlufiConnection:
    """Async Blufi Connection"""

    __slots__ = ("__format_address", "__client", "__debug_mode")

    def __init__(self, device_address: str, debug: bool = False) -> None:
        """AsyncBlufiConnection init"""
        self.__format_address = format_mac_address(device_address.strip().upper())
        self.__client: BleakClient | None = None
        self.__debug_mode = debug

    def set_debug_mode(self, mode: bool) -> None:
        """set_debug_mode"""
        self.__debug_mode = mode

    @property
    def debug_mode(self) -> bool:
        """debug mode"""
        return self.debug_mode

    @property
    def _client(self) -> BleakClient:
        """only for subclass"""
        if self.__client is None:
            raise AsyncBlufiConnectionError("Device not connected")
        return self.__client

    def __del_client(self) -> None:
        """"""
        del self.__client
        self.__client = None

    @property
    def address(self) -> str:
        """get formatted address"""
        return self.__format_address

    async def async_connect(self) -> None:
        """async connect"""

        logger.info(f"Try to establish a Bluetooth connection, address:{self.address}") if self.debug_mode else None
        try:
            if self.__client is None:
                self.__client = BleakClient(self.address)

                await self.__client.connect()
                logger.info("New connection established successfully") if self.debug_mode else None
                return
            if isinstance(self.__client, BleakClient):
                if self.__client.is_connected:
                    (
                        logger.info("Bluetooth is already connected, no need to connect again")
                        if self.debug_mode
                        else None
                    )
                    return
                else:
                    logger.info("Bluetooth has been disconnected, reconnecting~~~") if self.debug_mode else None
                    await self.__client.connect()
                    logger.info("Bluetooth connection successful") if self.debug_mode else None
                    return
        except Exception as e:
            logger.info(f"Abnormality during Bluetooth connection:{e}") if self.debug_mode else None
            raise AsyncBlufiConnectionError(str(e)) from e

    async def async_disconnect(self) -> None:
        """async disconnect"""
        try:
            if self.__client is None:
                logger.info("No connection established, no need to disconnect") if self.debug_mode else None
                return
            if self.__client.is_connected:
                logger.info("Bluetooth is connected, disconnecting~~~") if self.debug_mode else None
                try:
                    async with as_timeout(0.5):
                        await self.__client.disconnect()
                        await self.__client.unpair()
                        (
                            logger.info("Bluetooth is connected and disconnected successfully")
                            if self.debug_mode
                            else None
                        )
                except asyncio.TimeoutError:
                    self.__del_client()
                    logger.info("Bluetooth is connected, force disconnect") if self.debug_mode else None
        except Exception as e:
            msg: str = f"{self.address} Disconnection failed, please try restarting the software: {e}"
            logger.info(msg) if self.debug_mode else None
            raise AsyncBlufiDisconnectionError(msg) from e
