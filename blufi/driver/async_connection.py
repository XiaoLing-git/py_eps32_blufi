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

    __slots__ = (
        "__format_address",
        "__client",
    )

    def __init__(self, device_address: str) -> None:
        """AsyncBlufiConnection init"""
        self.__format_address = format_mac_address(device_address.strip().upper())
        self.__client: BleakClient | None = None

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
        logger.info(f"Try to establish a Bluetooth connection, address:{self.address}")
        try:
            if self.__client is None:
                self.__client = BleakClient(self.address)

                await self.__client.connect()
                logger.info("New connection established successfully")
                return
            if isinstance(self.__client, BleakClient):
                if self.__client.is_connected:
                    logger.info("Bluetooth is already connected, no need to connect again")
                    return
                else:
                    logger.info("Bluetooth has been disconnected, reconnecting~~~")
                    await self.__client.connect()
                    logger.info("Bluetooth connection successful")
                    return
        except Exception as e:
            logger.info(f"Abnormality during Bluetooth connection:{e}")
            raise AsyncBlufiConnectionError(str(e)) from e

    async def async_disconnect(self) -> None:
        """async disconnect"""
        try:
            if self.__client is None:
                logger.info("No connection established, no need to disconnect")
                return
            if self.__client.is_connected:
                logger.info("Bluetooth is connected, disconnecting~~~")
                try:
                    async with as_timeout(0.5):
                        await self.__client.disconnect()
                        await self.__client.unpair()
                        logger.info("Bluetooth is connected and disconnected successfully")
                except asyncio.TimeoutError:
                    self.__del_client()
                    logger.info("Bluetooth is connected, force disconnect")
        except Exception as e:
            msg: str = f"{self.address} Disconnection failed, please try restarting the software: {e}"
            logger.info(msg)
            raise AsyncBlufiDisconnectionError(msg) from e
