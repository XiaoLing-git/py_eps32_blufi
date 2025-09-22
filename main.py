"""Main function entry, mainly used for debugging."""
import asyncio
import logging

from blufi.commands import GetVersionCommand, SetSecurityModeCommand, SetWifiOpModeCommand, CustomDataCommand
from blufi.driver.async_write_read import AsyncBlufiWriteRead
from blufi.models.base_models import TypeField, ControlAddress, Encryption, CrcCheck, Direction, Ack, Sector_Data, \
    DataAddress, SecurityMode
from blufi.models.commands_models import ControlCommand, PocketType, FrameControl, ControlCommandWithData
from blufi.responses.ack_parser import AckParser
from blufi.responses.response import BlufiResponse, ResponseParser
from blufi.serial_number import SerialNumber

# logging.basicConfig(
#     level=logging.INFO,  # 核心：设置最低日志级别为DEBUG
#     format='%(asctime)s %(name)s - %(levelname)s - %(message)s',  # 日志格式
#     datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
# )

async def fun():
    try:
        ble = AsyncBlufiWriteRead(device_address="8CBFEA852D7E")

        await ble.async_connect()


        # for n in range(20):
        #     ack =  CustomDataCommand("gss_test")
        #     print(ack)
        #     print(f"Command: {ack}, sn ={ack.sn} length ={ack.data_length}")
        #     res = await ble.async_read_after_write(str(ack))
        #     br = ResponseParser(res.hex())
        #     # if isinstance(br, AckParser):
        #     br.parser()
        #     print(br)
        #     print("*"*100)
        #     await asyncio.sleep(0.2)

        ack = CustomDataCommand("gss_test")
        print(ack)
        print(f"Command: {ack}, sn ={ack.sn} length ={ack.data_length}")
        res = await ble.async_read_after_write(str(ack))
        br = ResponseParser(res.hex())
        # if isinstance(br, AckParser):
        br.parser()
        print(br)

        for i in range(10):
            res = await ble.read(clear=True)
            br = ResponseParser(res.hex())
            # if isinstance(br, AckParser):
            br.parser()
            print(br)


    except Exception as e:
        raise e
    finally:
        await ble.async_disconnect()
    # await ble.async_disconnect()

if __name__ == "__main__":
    asyncio.run(fun())

    "410401020103"