# py_eps32_blufi
 Python Support for [**ESP-32-Blufi**](https://docs.espressif.com/projects/esp-idf/zh_CN/stable/esp32/api-guides/ble/blufi.html)

## Notes:

1. Before you start it, please make sure you have installed the following tools
   - make == GNU Make 4.4.1
   - poetry == 1.8.0
   - python ==  >=3.10, <=3.14

2. This project is still in progress, if you have any questions, please feel free to contact us.



## Commands

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

### update pip 

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