"""
Replacement for using print.
Serial communication needs time, which the processor doesn't have.
This provides a simple switch for enabling or disabling DEBUG
"""
from settingStorage import SettingStorage


def print_d(*values: object) -> None:
    """same as print(), but can be disabled to speed things up"""
    if get_debug_mode():
        print(*values)


def set_debug_mode(value: bool) -> None:
    """set debug on or off"""
    SettingStorage.set_value("debug", str(value))


def get_debug_mode() -> bool:
    """get debug mode"""
    return SettingStorage.get_value("debug") == "True"
