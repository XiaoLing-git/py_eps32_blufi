"""Main function entry, mainly used for debugging."""
import asyncio
import logging
import time

from blufi.commands import CustomDataCommand, AckCommand, GetVersionCommand, SetSecurityModeCommand, GetWifiListCommand, \
    GetWifiStatusCommand, StaWifiSSIDCommand, StaWifiPasswordCommand, ConnectWifiCommand, DisconnectWifiCommand, \
    BleDisconnectCommand, CACertificationCommand
from blufi.driver.async_base_driver import AsyncBlufiBaseDriver
from blufi.driver.async_write_read import AsyncBlufiWriteRead
from blufi.errors import BlufiBaseException
from blufi.models import ControlAddress, TypeField, Encryption, CrcCheck, Direction, Ack, Sector_Data
from blufi.models.frame_models import PocketType, FrameControl, BaseDataModels, ControlCommandWithData
from blufi.serial_number import SerialNumber


#
# logging.basicConfig(
#     level=logging.INFO,  # 核心：设置最低日志级别为DEBUG
#     format='%(asctime)s %(name)s - %(levelname)s - %(message)s',  # 日志格式
#     datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
# )

async def fun():
    try:
        ble = AsyncBlufiBaseDriver(device_address="8CBFEA852D7E", timeout=20)

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
            if ble.response_parser:
                print(ble.response_parser)

        print("-" * 100)
        cmd = CustomDataCommand(content="wifitest")
        await ble.async_send_command(cmd)
        start_time = time.time()
        while True:
            if time.time() - start_time > 20:
                break
            await asyncio.sleep(0.1)
            ble.get_response()
            if ble.response_parser:
                print(ble.response_parser)

        # print("-" * 100)
        # cmd = StaWifiPasswordCommand(content="runucleverboy")
        # await ble.async_send_command(cmd)
        # start_time = time.time()
        # while True:
        #     if time.time() - start_time > 10:
        #         break
        #     await asyncio.sleep(0.1)
        #     if ble.response_parser:
        #         print(ble.get_response().pocket_type, ble.get_response().parser())
        #
        # print("-" * 100)
        # cmd = ConnectWifiCommand()
        # await ble.async_send_command(cmd)
        # start_time = time.time()
        # while True:
        #     if time.time() - start_time > 10:
        #         break
        #     await asyncio.sleep(0.1)
        #     if ble.response_parser:
        #         p = ble.get_response()
        #         print("@", p.pocket_type.func_code, p.parser())

        # print("-" * 100)
        # cmd = DisconnectWifiCommand()
        # await ble.async_send_command(cmd)
        # start_time = time.time()
        # while True:
        #     if time.time() - start_time > 10:
        #         break
        #     await asyncio.sleep(0.1)
        #     if ble.response_parser:
        #         p = ble.get_response()
        #         print("@", p.pocket_type.func_code, p.parser())

        # start_time = time.time()
        # while True:
        #     if time.time() - start_time > 5:
        #         break
        #     time.sleep(1)
        #     print("hold")

        # for i in range(10):
        # ack = CustomDataCommand("wifitest")
        # res = await ble.async_read_large_data_after_write(ack)
        # if isinstance(res, CustomDataParser):
        #     print(res.content)

        # for n in range(10):
        #     ack =  CustomDataCommand("wifitest")
        #     print(ack)
        #     # print(f"Command: {ack}, sn ={ack.sn} length ={ack.data_length}")
        #     res = await ble.async_read_after_write(str(ack))
        #     br = ResponseParser(res.hex())
        #     # if isinstance(br, AckParser):
        #     br.parser()
        #     print(br)
        #     print("*"*100)
        #     await asyncio.sleep(3)

        # ack = CustomDataCommand("gss_test")
        # print(ack)
        # print(f"Command: {ack}, sn ={ack.sn} length ={ack.data_length}")
        # res = await ble.async_read_after_write(str(ack))
        # br = ResponseParser(res.hex())
        # br.parser()
        # print(br)
        #
        # for i in range(10):
        #     res = await ble.read(clear=True)
        #     br = ResponseParser(res.hex())
        #     br.parser()
        #     print(br)




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
