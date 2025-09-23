""""""

import asyncio
import logging
import threading
import time

from ..commands import AckCommand, Commands_Type
from ..commands.commands_models import ControlCommandWithData
from ..errors import AsyncBlufiConnectionError
from ..models.base_models import ControlAddress, Sector_Data
from ..responses.response import BlufiResponse
from .async_write_read import AsyncBlufiWriteRead

logger = logging.getLogger(__name__)


class AsyncBlufiBaseDriver(AsyncBlufiWriteRead):
    """Async Blufi Base Driver"""

    def __init__(self, device_address: str, timeout: float = 10) -> None:
        """init"""
        super().__init__(device_address, timeout)
        self.response_parser: BlufiResponse | None = None
        self.__read_server_flag: bool = False

    async def async_connect(self) -> None:
        """async_connect."""
        await super().async_connect()
        ack_cmd = AckCommand()
        response = await self.async_read_after_write(str(ack_cmd))
        blufi_response = BlufiResponse(response.hex())
        if blufi_response.pocket_type.func_code is not ControlAddress.ACK:
            raise AsyncBlufiConnectionError("device init fail")
        self.start_read_server()

    async def async_disconnect(self) -> None:
        """async_disconnect"""
        await super().async_disconnect()
        self.__read_server_flag = False

    def start_read_server(self) -> None:
        """start_read_server"""
        self.__read_server_flag = True
        threading.Thread(target=self.__read_server).start()

    def stop_read_server(self) -> None:
        """stop_read_server"""
        self.__read_server_flag = False

    def __read_server(self) -> None:
        """__read_server"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__async_read_server())

    async def __async_read_server(self) -> None:
        """__async_read_server"""
        try:
            while self.__read_server_flag:
                await self.read(clear_response=False)
                temp_response = BlufiResponse(self.response)
                if temp_response.frame_control.sector_Data is Sector_Data.disable:
                    self.response_parser = temp_response
                else:
                    await self.read_sector_data(temp_response)
        except Exception as e:
            print(e)
            self.__read_server_flag = False
            raise e

    async def read_sector_data(self, first_sector: BlufiResponse) -> None:
        """read_sector_data"""
        sector = first_sector
        content = ""
        start_time = time.time()
        # while sector.frame_control.sector_Data is Sector_Data.enable:
        while True:
            print(sector)
            if time.time() - start_time > self.timeout:
                raise TimeoutError("Read SectorData timeout")

            if sector.frame_control.sector_Data is Sector_Data.disable:
                content = content + sector.data
                break
            else:
                content = content + sector.data[4:]
            response = await self.read()
            sector = BlufiResponse(response.hex())
        value = ControlCommandWithData(
            pocket_type=sector.pocket_type, frame_control=sector.frame_control, sn=sector.sn, data=content
        ).hex()
        print(bytes.fromhex(content).decode())
        self._set_response(value)

    async def async_send_command(self, cmd: Commands_Type) -> None:
        """async_send_command"""
        await self.write(str(cmd), clear_response=False)

    def get_response(self) -> None:
        """get_response"""
        pass
