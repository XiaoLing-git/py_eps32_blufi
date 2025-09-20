"""Main function entry, mainly used for debugging."""
import asyncio
import logging

from blufi.driver.async_write_read import AsyncBlufiWriteRead
from blufi.models.base_models import TypeField, ControlAddress, Encryption, CrcCheck, Direction, Ack, Sector_Data, \
    DataAddress
from blufi.models.commands import ControlCommand, PocketType, FrameControl, ControlCommandWithData
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


        for n in range(10):
            ack = ControlCommandWithData(
                pocket_type=PocketType(
                    type_field=TypeField.Control,
                    func_code=ControlAddress.GET_WIFI_STATUS),
                frame_control=FrameControl(
                    encryption=Encryption.disable,
                    crc_check=CrcCheck.disable,
                    direction=Direction.device_to_esp,
                    ack=Ack.enable,
                    sector_Data=Sector_Data.disable,
                ),
                sn=SerialNumber().obj,
                data="00"
            )
            print(ack)
            print(f"Command: {ack.hex()}, sn ={ack.sn} length ={ack.data_length}")
            res = await ble.async_read_after_write(ack.hex())
            br = ResponseParser(res.hex())
            # if isinstance(br, AckParser):
            br.parser()
            print(br)
            print("*"*100)
            await asyncio.sleep(0.1)
            # for i in range(5):
            #     res = await ble.read(clear=True)
            #     br = ResponseParser(res.hex())
            #     br.parser()
            #     print(br)
            #     print("&" * 100)
            # print("-"*100)




        # bc = ControlCommand(
        #     pocket_type=PocketType(
        #         type_field=TypeField.Control,
        #         func_code=ControlAddress.GET_VERSION),
        #     frame_control=FrameControl(
        #         encryption=Encryption.disable,
        #         crc_check=CrcCheck.disable,
        #         direction=Direction.device_to_esp,
        #         ack=Ack.enable,
        #         sector_Data=Sector_Data.disable,
        #     ),
        #     sn=SerialNumber().obj,
        # )
        # print(bc)
        # print("*"*100)
        # res = await ble.async_read_after_write(str(bc))
        # br = ResponseParser(res.hex())
        # br.parser()
        # print(br)
        # print("#"*100)
        # if br.pocket_type.func_code is DataAddress.VERSION:
        #     pass
        # else:
        #     for i in range(10):
        #         res = await ble.read(clear=True)
        #         br = ResponseParser(res.hex())
        #         br.parser()
        #         print(br)
        #         print("*" * 100)
        #         if br.pocket_type.func_code is DataAddress.VERSION:
        #             break
        #
        # print("-"*100)
        # bc = ControlCommand(
        #     pocket_type=PocketType(
        #         type_field=TypeField.Control,
        #         func_code=ControlAddress.GET_VERSION),
        #
        #     frame_control=FrameControl(
        #         encryption=Encryption.disable,
        #         crc_check=CrcCheck.disable,
        #         direction=Direction.device_to_esp,
        #         ack=Ack.enable,
        #         sector_Data=Sector_Data.disable,
        #     ),
        #     sn=SerialNumber().obj,
        #
        # )
        # print(bc.pocket_type)
        # print(bc.frame_control)
        # print(bc.sn,"SN")
        # print(bc)
        # print("*" * 100)
        # res = await ble.async_read_after_write(str(bc))
        # br = ResponseParser(res.hex())
        # br.parser()
        # print("#" * 100)
        # if br.pocket_type.func_code is DataAddress.VERSION:
        #     pass
        # else:
        #     for i in range(10):
        #         res = await ble.read(clear=True)
        #         br = ResponseParser(res.hex())
        #         br.parser()
        #         print("*" * 100)
        #         if br.pocket_type.func_code is DataAddress.VERSION:
        #             break

    except Exception as e:
        raise e
    finally:
        await ble.async_disconnect()
    # await ble.async_disconnect()

if __name__ == "__main__":
    asyncio.run(fun())

    "410401020103"