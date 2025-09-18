"""Async Blufi Connection."""

import asyncio
import logging

from async_timeout import timeout as as_timeout
from bleak import BleakClient

from ..errors import AsyncBlufiConnectionError, AsyncBlufiDisconnectionError
from ..utils import format_mac_address

logger = logging.getLogger(__name__)


class AsyncBlufiConnection:
    """"""

    def __init__(self, device_address: str) -> None:
        """"""
        self.__address = format_mac_address(device_address.strip().upper())
        self.__client: BleakClient | None = None

    @property
    def _client(self) -> BleakClient:
        """给子类调用,当前类不能直接使用"""
        if self.__client is None:
            raise AsyncBlufiConnectionError("设备没有连接")
        return self.__client

    def del_client(self) -> None:
        """"""
        del self.__client
        self.__client = None

    @property
    def address(self) -> str:
        """"""
        return self.__address

    async def async_connect(self) -> None:
        """"""
        logger.info(f"尝试建立蓝牙连接 address:{self.address}")
        try:
            if self.__client is None:
                self.__client = BleakClient(self.address)

                await self.__client.connect()
                logger.info("建立新的连接成功")
                return
            if isinstance(self.__client, BleakClient):
                if self.__client.is_connected:
                    logger.info("蓝牙已连接，无需再次连接")
                    return
                else:
                    logger.info("蓝牙已断开，再次连接中~~~")
                    await self.__client.connect()
                    logger.info("蓝牙连接成功")
                    return
        except Exception as e:
            logger.info(f"蓝牙连接过程中异常:{str(e)}")
            raise AsyncBlufiDisconnectionError(str(e))

    async def async_disconnect(self) -> None:
        """"""
        try:
            if self.__client is None:
                logger.info("未建立连接，无需断开")
                return
            if self.__client.is_connected:
                logger.info("蓝牙已连接，断开中~~~")
                try:
                    async with as_timeout(0.5):
                        await self.__client.disconnect()
                        await self.__client.unpair()
                        logger.info("蓝牙已连接，正常断开成功")
                except asyncio.TimeoutError:
                    self.del_client()
                    logger.info("蓝牙已连接，强制断开")
        except Exception as e:
            msg: str = f"{self.address} 断开连接失败,请尝试重启软件: {e}"
            logger.info(msg)
            raise AsyncBlufiDisconnectionError(msg)
