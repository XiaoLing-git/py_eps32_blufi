"""Main function entry, mainly used for debugging."""
import asyncio
import logging

from blufi.driver.async_write_read import AsyncBlufiWriteRead
from blufi.serial_number import SerialNumber

logging.basicConfig(
    level=logging.INFO,  # 核心：设置最低日志级别为DEBUG
    format='%(asctime)s %(name)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

async def fun():
    ble = AsyncBlufiWriteRead(device_address="8CBFEA8355DE")
    # await ble.async_connect()
    await ble.async_connect()
    # await ble.write("123456")
    # await ble.read()
    await ble.async_read_after_write("123456")

    await ble.async_read_after_write("456789")

    await ble.async_disconnect()
    # await ble.async_disconnect()

if __name__ == "__main__":
    # asyncio.run(fun())
    for i in range(100):
        print(SerialNumber().obj)