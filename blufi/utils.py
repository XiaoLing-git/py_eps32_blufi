"""utils"""

from .errors import AsyncBlufiAddressFormatError, HexStrException


def assert_hex_str(target: str) -> None:
    """
    assert hex str
    :param target:
    :return: None
    """
    if not isinstance(target, str):
        raise HexStrException(f"{target} can't be hex_str")

    target_str = "0123456789ABCDEF"
    for i in target:
        if i.upper() not in target_str:
            raise HexStrException(f"{i} can't be hex_str")
    if len(target) % 2 != 0:
        raise HexStrException(f"{target} can't be hex_str,length of target is odd")


def assert_address_format(address: str) -> None:
    """
    assert address format
    :param address:
    :return: None
    """
    target_str = "0123456789ABCDEF:"
    for i in address:
        if i.upper() not in target_str:
            raise AsyncBlufiAddressFormatError(
                f"Device address must be in |0123456789ABCDEF:|, current address: {address} now get {i} "
            )

    if not (len(address) == 12 or len(address) == 17):
        raise AsyncBlufiAddressFormatError(f"Abnormal address length: {address} {len(address)}")

    format_address = address.replace(":", "")
    if len(format_address) != 12:
        raise AsyncBlufiAddressFormatError(f"Abnormal address: {address} maybe too much |:|")


def format_mac_address(mac: str, split: str = ":", lower: bool = True) -> str:
    """
    format mac address
    :param mac:
    :param split:
    :param lower:
    :return: formatted mac address[aa:bb:cc:dd:ee:ee]
    """
    assert_address_format(mac)
    response = split.join([mac[i : i + 2] for i in range(0, len(mac), 2)])
    if lower:
        return response.lower()
    else:
        return response.upper()
