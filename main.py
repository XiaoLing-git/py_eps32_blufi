"""Main function entry, mainly used for debugging."""
import asyncio
import logging

import time

from blufi.commands import CustomDataCommand, AckCommand

from blufi.driver.async_base_driver import AsyncBlufiBaseDriver
from blufi.responses import CustomDataParser

logging.basicConfig(
    level=logging.INFO,  # 核心：设置最低日志级别为DEBUG
    format='%(asctime)s %(name)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

async def fun():
    try:
        ble = AsyncBlufiBaseDriver(device_address="8CBFEA852D7E", timeout=20,debug=True)

        await ble.async_connect()

        start_time = time.time()
        while True:
            if time.time() - start_time > 3:
                break
            # print(ble.response_parser)
            ack = AckCommand()
            # print(ack)
            await ble.async_send_command(ack)
            ble.get_response()
            time.sleep(0.1)
            res = ble.get_response()

        print("-" * 100)
        cmd = CustomDataCommand(content="wifitest")
        await ble.async_send_command(cmd)
        start_time = time.time()
        while True:
            if time.time() - start_time > 20:
                break
            await asyncio.sleep(0.1)
            p = ble.get_response().parser()
            if isinstance(p, CustomDataParser):
                print(p.format)



    except Exception as e:
        raise e
    finally:
        await ble.async_disconnect()
    # await ble.async_disconnect()


if __name__ == "__main__":
    asyncio.run(fun())
    #
    # "410401020103"
    # content = b'\x02\x0bXiaomi_2ACD\x03\rrunucleverboy'
    # print(content.decode())
