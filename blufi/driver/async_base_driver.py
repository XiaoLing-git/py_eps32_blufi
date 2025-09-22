""""""

import asyncio
import logging
import time

from bleak import BleakGATTCharacteristic

from ..commands import AckCommand, Commands_Type, CustomDataCommand
from ..errors import (
    AsyncBlufiConnectionError,
    AsyncBlufiReadException,
    AsyncBlufiWriteException,
    AsyncBlufiWriteReadException,
)
from ..models.base_models import ControlAddress
from ..responses.ack_parser import AckParser
from ..responses.response import BlufiResponse
from .async_write_read import AsyncBlufiWriteRead

logger = logging.getLogger(__name__)


class AsyncBlufiBaseDriver(AsyncBlufiWriteRead):
    """Async Blufi Base Driver"""

    async def async_read_large_data_after_write(self, cmd: Commands_Type) -> BlufiResponse:
        """
        async read after write
        :param cmd:
        :return:
        """
        data = str(cmd)
        await self.write(data, start_notify=True)

        response = await self.read()
        parser = BlufiResponse(response.hex())
        print(parser.pocket_type.func_code)
        if parser.pocket_type.func_code is ControlAddress.ACK:
            response = await self.read(clear=True)
            parser = BlufiResponse(response.hex())

        start_time = time.time()
        results = parser.data
        while parser.is_vector():
            if time.time() - start_time > self.timeout:
                break
            response = await self.read(clear=True)
            parser = BlufiResponse(response.hex())
            results = results + parser.data
        print("results = ", bytes.fromhex(results).decode())
        if results == parser.data:
            print(1)
            return parser
        else:
            print(2)
            parser.insert_data(results)
            return parser
