""""""

import asyncio
import logging
import time
from typing import Any

from bleak import BleakGATTCharacteristic

from ..errors import (
    AsyncBlufiConnectionError,
    AsyncBlufiGetServiceException,
    AsyncBlufiGetUUIDException,
    AsyncBlufiReadException,
    AsyncBlufiWriteException,
    AsyncBlufiWriteReadException,
)
from ..models import ControlCommandWithData, Sector_Data
from ..responses import BlufiResponse
from .async_connection import AsyncBlufiConnection

logger = logging.getLogger(__name__)


class AsyncBlufiWriteRead(AsyncBlufiConnection):
    """Async Blufi Write Read"""

    __slots__ = ("__write_uuid", "__notify_uuid", "__response", "__cmd", "__timeout", "__sector_data")

    def __init__(self, device_address: str, timeout: float = 10, debug: bool = False):
        """
        AsyncBlufiWriteRead init
        """
        super().__init__(device_address, debug)

        self.__write_uuid: str | None = None
        self.__notify_uuid: str | None = None
        self.__response: bytearray | None = None
        self.__cmd: str = ""
        self.__timeout = timeout
        self.__sector_data: str | None = None

    @property
    def response(self) -> str:
        """only call in subclass"""
        if self.__response is None:
            raise AsyncBlufiWriteReadException("This method cannot be called during command sending")
        return self.__response.hex()

    @property
    def command(self) -> str:
        """only call in subclass"""
        return self.__cmd

    async def async_connect(self) -> None:
        """async connect."""
        await super().async_connect()
        self.__get_uuid()
        await self._start_notify()

    async def async_disconnect(self) -> None:
        """"""
        await self._stop_notify()
        await super().async_disconnect()

    def __get_device_services(self) -> dict[str, Any]:
        """
        get device services
        :return:
        """
        try:
            service_data: dict[str, Any] = {}
            services = self._client.services
            for service in services:
                service_data[service.description] = {service.uuid: ["service_uuid"]}
                for c in service.characteristics:
                    service_data[service.description][c.uuid] = c.properties
            logger.info("Succeed to obtained Bluetooth device service") if self.debug_mode else None
            return service_data
        except Exception as e:
            msg: str = f"Failed to obtain Bluetooth device service :{e}"
            logger.info(msg) if self.debug_mode else None
            raise AsyncBlufiGetServiceException(msg) from e

    def __get_uuid(self) -> tuple[str | None, str | None]:
        """
        get device uuid
        :return:
        """
        data = self.__get_device_services()
        try:
            uuids = data.get("Vendor specific")
            if uuids is None:
                raise AsyncBlufiGetUUIDException(
                    f" Failed to obtain Bluetooth device[{self.address}] specific (Vendor specific) service"
                )
            if uuids:
                for uuid in uuids:
                    if "write" in uuids[uuid]:
                        self.__write_uuid = uuid
                    if "notify" in uuids[uuid]:
                        self.__notify_uuid = uuid
                logger.info("get UUID succeed") if self.debug_mode else None
            return self.__write_uuid, self.__notify_uuid
        except AsyncBlufiGetUUIDException as e:
            logger.info(f"{e}") if self.debug_mode else None
            raise e
        except Exception as e:
            logger.info(f"{e}") if self.debug_mode else None
            raise AsyncBlufiGetUUIDException(f"Bluetooth device[{self.address}] Failed to obtain UUID: {e}")

    def __notification_handler(self, sender: BleakGATTCharacteristic, data: bytearray) -> None:
        """notification handler"""
        temp = BlufiResponse(data.hex())
        logger.info(f"Read: {temp}") if self.debug_mode else None
        if temp.frame_control.sector_data is Sector_Data.enable:
            if self.__sector_data is None:
                self.__sector_data = temp.data[4:]
            else:
                self.__sector_data = self.__sector_data + temp.data[4:]
        else:
            if self.__sector_data:
                self.__sector_data = self.__sector_data + temp.data
                value = ControlCommandWithData(
                    pocket_type=temp.pocket_type, frame_control=temp.frame_control, sn=temp.sn, data=self.__sector_data
                ).hex()
                self.__response = bytes.fromhex(value)  # type: ignore[assignment]
                self.__sector_data = None
            else:
                self.__response = data

    def __assert_connection_status(self) -> None:
        """
        assert connection status
        :return:
        """
        if self.__write_uuid is None or self.__notify_uuid is None:
            logger.info("UUID is none and you try to send a command.") if self.debug_mode else None
            raise AsyncBlufiWriteReadException(f"UUID is none and you try to send a command.")
        if not self._client.is_connected:
            logger.info("The device is not connected and you try to send a command.") if self.debug_mode else None
            raise AsyncBlufiConnectionError(f"Please make sure the device is connected when sending the command")

    async def _start_notify(self) -> None:
        try:
            await self._client.start_notify(self.__notify_uuid, callback=self.__notification_handler)
        except Exception as e:
            raise AsyncBlufiWriteReadException(f"{self.address} {self.__notify_uuid} start_notify fail msg: {e}")

    async def _stop_notify(self) -> None:
        try:
            await self._client.stop_notify(self.__notify_uuid)
        except Exception as e:
            raise AsyncBlufiReadException(f"{self.address} stop_notify fail: {e}")

    async def write(self, data: str, clear_response: bool = True) -> None:
        """
        write data to device
        :param data:
        :param clear_response:
        :return:
        """
        self.__cmd = data
        if clear_response:
            self.__response = None
            logger.info(f"Clear Response: {self.__response}") if self.debug_mode else None

        try:
            logger.info(f"Write: {data}") if self.debug_mode else None
            await self._client.write_gatt_char(self.__write_uuid, bytes.fromhex(data))
        except Exception as e:
            raise AsyncBlufiWriteException(f"Device: {self.address} write_gatt_char fail: {e}") from e

    async def read(self, clear_response: bool = True) -> bytearray:
        """
        read data from device
        :return:
        """
        if clear_response:
            self.__response = None
        try:

            response = await self.__read_until_timeout()
            logger.info(f"Read : {response.hex()}") if self.debug_mode else None
        except Exception as e:
            raise AsyncBlufiReadException(f"{self.address} Get response fail {e}") from e

        return response

    async def async_read_after_write(self, data: str) -> bytearray:
        """
        async read after write
        :param data:
        :return:
        """
        self.__cmd = data

        await self.write(data, clear_response=True)
        await self.read(clear_response=False)

        if self.__response is None:
            raise AsyncBlufiWriteReadException("No response received")

        logger.info(f"Data: {data} Response: {self.__response.hex()}") if self.debug_mode else None

        return self.__response

    async def __read_until_timeout(self) -> bytearray:
        """
        read until timeout
        :return:
        """
        start_time = time.time()
        while True:
            await asyncio.sleep(0.01)
            if self.__response:
                break
            if time.time() - start_time > self.__timeout:
                raise AsyncBlufiReadException(f"Get response timeout Timeout = {self.__timeout} s")
        return self.__response

    def _set_response(self, value: str) -> None:
        self.__response = bytearray(bytes.fromhex(value))

    @property
    def timeout(self) -> float:
        """"""
        return self.__timeout
