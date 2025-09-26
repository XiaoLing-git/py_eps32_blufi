""""""

import logging

from ..commands import AckCommand, Commands_Type
from ..errors import AsyncBlufiConnectionError
from ..models import ControlAddress
from ..responses import BlufiResponse
from .async_write_read import AsyncBlufiWriteRead

logger = logging.getLogger(__name__)


class AsyncBlufiBaseDriver(AsyncBlufiWriteRead):
    """Async Blufi Base Driver"""

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
        logger.info(f"Send: {cmd}") if self.debug_mode else None
        await self.write(str(cmd), clear_response=False)

    def get_response(self) -> BlufiResponse:
        """get_response"""
        response = BlufiResponse(self.response)
        logger.info(f"read: {response}") if self.debug_mode else None
        return response

    def is_connected(self) -> bool:
        """is_connected"""
        return self._client.is_connected  # type: ignore[no-any-return]
