# py_eps32_blufi
 Python Support for [**ESP-32-Blufi**](https://docs.espressif.com/projects/esp-idf/zh_CN/stable/esp32/api-guides/ble/blufi.html)

## Notes:

1. This project is still in progress, if you have any questions, please feel free to contact us.

2. Before you start it, please make sure you have installed the following tools
   - make == GNU Make 4.4.1
   - poetry == 1.8.0
   - python ==  >=3.10, <=3.14

3. After cloning this project, please execute the command
   ```bash
   make project_init
   ```

## Install
   ```bash
   pip install https://github.com/XiaoLing-git/py_eps32_blufi/releases/download/release_1.1.1/py_esp32_blufi-1.1.1-py3-none-any.whl
   ```


## Development

### Build Wheel

```bash
make build
```

### Install Local

```bash
make install
```

### Enter Venv 

```bash
make shell
```

### Update pip 

```bash
make update
```

### Clean

```bash
make clean
```

### Commit To Github

```bash
make commit msg="comments"
make push msg="comments"
```

### Local check code

```bash
make check 
```

### Example
```python
import asyncio
from blufi.commands import CustomDataCommand, AckCommand
from blufi.driver.async_base_driver import AsyncBlufiBaseDriver
from blufi.driver import BlufiBaseDriver


async def async_fun():
    ble = None
    try:
        ble = AsyncBlufiBaseDriver(device_address="8CBFEA852D7E", timeout=20, debug=True)
        await ble.async_connect()
        command = AckCommand()
        await ble.async_send_command(command)
        response = await ble.async_get_response()
        print(response)
        print("-" * 100)
        cmd = CustomDataCommand(content="demo")
        await ble.async_send_command(cmd)
        response = await ble.async_get_response()
        print(response)
    except Exception as e:
        raise e
    finally:
        await ble.async_disconnect()
        
def fun():
   ble = None
   try:
      ble = BlufiBaseDriver(device_address="8CBFEA852D7E", timeout=20, debug=True)
      ble.connect()
      command = AckCommand()
      ble.send_command(command)
      response = ble.get_response()
      print(response)
      print("-" * 100)
      command = CustomDataCommand(content="demo")
      ble.send_command(command)
      response = ble.get_response()
      print(response)
   except Exception as e:
     raise e
   finally:
     ble.disconnect()


if __name__ == "__main__":
    fun()
    
    asyncio.run(async_fun())

```


