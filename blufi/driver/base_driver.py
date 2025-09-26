"""base driver"""

import asyncio
from asyncio import AbstractEventLoop

from ..commands import Commands_Type
from ..responses import BlufiResponse
from .async_base_driver import AsyncBlufiBaseDriver


class BlufiBaseDriver:
    """Blufi Base Driver"""

    def __init__(self, device_address: str, timeout: float = 10, debug: bool = False) -> None:
        """
        init
        """
        self.__device_address = device_address
        self.__timeout = timeout
        self.__debug = debug
        self.__device = AsyncBlufiBaseDriver(device_address=device_address, timeout=timeout, debug=debug)
        self.__loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.__loop)

    @property
    def timeout(self) -> float:
        """timeout"""
        return self.__timeout

    @property
    def debug(self) -> bool:
        """debug"""
        return self.__debug

    @property
    def device(self) -> AsyncBlufiBaseDriver:
        """device"""
        return self.__device

    @property
    def loop(self) -> AbstractEventLoop:
        """loop"""
        return self.__loop

    def set_debug_mode(self, mode: bool) -> None:
        """connect"""
        self.device.set_debug_mode(mode)

    def connect(self) -> None:
        """connect"""
        self.loop.run_until_complete(self.device.async_connect())

    def disconnect(self) -> None:
        """disconnect"""
        self.loop.run_until_complete(self.device.async_disconnect())

    def send_command(self, cmd: Commands_Type) -> None:
        """send_command"""
        self.loop.run_until_complete(self.device.async_send_command(cmd))

    def get_response(self) -> BlufiResponse:
        """get_response"""
        return self.loop.run_until_complete(self.device.async_get_response())

    def is_connected(self) -> bool:
        """is_connected"""
        return self.device.is_connected
