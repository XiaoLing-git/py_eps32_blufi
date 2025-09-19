"""Main function entry, mainly used for debugging."""
import asyncio
import logging

from blufi.driver.async_write_read import AsyncBlufiWriteRead
from blufi.models.base_models import TypeField, ControlAddress, Encryption, CrcCheck, Direction, Ack, Sector_Data
from blufi.models.commands import ControlCommandWithData, ControlCommand, PocketType, FrameControl
from blufi.serial_number import SerialNumber

logging.basicConfig(
    level=logging.INFO,  # 核心：设置最低日志级别为DEBUG
    format='%(asctime)s %(name)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

async def fun():
    ble = AsyncBlufiWriteRead(device_address="8CBFEA852D7E")

    await ble.async_connect()

    bc = ControlCommand(
        pocket_type=PocketType(
            type_field=TypeField.Control,
            func_code=ControlAddress.GET_VERSION),

        frame_control=FrameControl(
            encryption=Encryption.disable,
            crc_check=CrcCheck.enable,
            direction=Direction.device_to_esp,
            ack=Ack.enable,
            sector_Data=Sector_Data.disable,
        ),
        data_length=3
    )
    print(bc)
    await ble.async_read_after_write(str(bc))


    await ble.async_disconnect()
    # await ble.async_disconnect()

if __name__ == "__main__":
    asyncio.run(fun())