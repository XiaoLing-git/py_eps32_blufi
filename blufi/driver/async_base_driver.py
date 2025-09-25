""""""

import asyncio
import logging
import time

from ..commands import AckCommand, Commands_Type, ControlCommandWithData
from ..errors import AsyncBlufiConnectionError
from ..models import ControlAddress, Sector_Data
from ..responses import BlufiResponse
from .async_write_read import AsyncBlufiWriteRead

logger = logging.getLogger(__name__)


class AsyncBlufiBaseDriver(AsyncBlufiWriteRead):
    """Async Blufi Base Driver"""

    __slots__ = ("response_parser",)

    def __init__(self, device_address: str, timeout: float = 10) -> None:
        """init"""
        super().__init__(device_address, timeout)
        self.response_parser: BlufiResponse | None = None

    async def async_connect(self) -> None:
        """async_connect."""
        await super().async_connect()
        ack_cmd = AckCommand()
        response = await self.async_read_after_write(str(ack_cmd))
        blufi_response = BlufiResponse(response.hex())
        if blufi_response.pocket_type.func_code is not ControlAddress.ACK:
            raise AsyncBlufiConnectionError("device init fail")

    async def async_disconnect(self) -> None:
        """async_disconnect"""
        await super().async_disconnect()

    async def async_send_command(self, cmd: Commands_Type) -> None:
        """async_send_command"""
        await self.write(str(cmd), clear_response=False)

    def get_response(self) -> BlufiResponse:
        """get_response"""
        response = BlufiResponse(self.response)
        self.response_parser = response.parser()
        return response
