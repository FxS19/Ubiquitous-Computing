"""
Replacement for using print.
Serial communication needs time, which the processor doesn't have.
This provides a simple switch for enabling or disabling DEBUG
"""
DEBUG = False

def print_d(*values: object, sep: str) -> None:
    """same as print(), but can be disabled to speed things up"""
    if DEBUG:
        print(values=values, sep=sep)

def set_debug_mode(value: bool) -> None:
    """set debug on or off"""
    DEBUG = value