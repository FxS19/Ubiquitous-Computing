"""
Replacement for using print.
Serial communication needs time, which the processor doesn't have.
This provides a simple switch for enabling or disabling DEBUG
"""
DEBUG = False

def print_d(*values: object) -> None:
    """same as print(), but can be disabled to speed things up"""
    if DEBUG:
        print(values=values)

def set_debug_mode(value: bool) -> None:
    """set debug on or off"""
    DEBUG = value