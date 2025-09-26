"""Main function entry, mainly used for debugging."""
import asyncio
import logging

import time

from blufi.commands import CustomDataCommand, AckCommand
from blufi.driver import BlufiBaseDriver

from blufi.driver.async_base_driver import AsyncBlufiBaseDriver
from blufi.responses import CustomDataParser

logging.basicConfig(
    level=logging.INFO,  # 核心：设置最低日志级别为DEBUG
    format='%(asctime)s %(name)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

async def fun():
    ble = None
    try:
        ble = AsyncBlufiBaseDriver(device_address="8CBFEA852D7E", timeout=20,debug=True)

        await ble.async_connect()


        command = AckCommand()
        await ble.async_send_command(command)
        response = await ble.async_get_response()
        print(response)

        cmd = CustomDataCommand(content="wifitest")
        await ble.async_send_command(cmd)
        response = await ble.async_get_response()
        print(response)
    except Exception as e:
        raise e
    finally:
        await ble.async_disconnect()


if __name__ == "__main__":
    # asyncio.run(fun())

    ble = BlufiBaseDriver(device_address="8CBFEA852D7E", timeout=20, debug=True)

    ble.connect()

    command = AckCommand()
    ble.send_command(command)
    response = ble.get_response()
    print(response)
    print("-" * 100)
    command = CustomDataCommand(content="wifitest")
    ble.send_command(command)
    response = ble.get_response()
    print(response)
