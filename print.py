"""
Replacement for using print.
Serial communication needs time, which the processor doesn't have.
This provides a simple switch for enabling or disabling DEBUG
"""

def print_d(*values: object) -> None:
    """same as print(), but can be disabled to speed things up"""
    if get_debug_mode():
        print(*values)

def set_debug_mode(value: bool) -> None:
    """set debug on or off"""
    f = open('debug', 'w')
    if value:
        f.write('Enabled')
    else:
        f.write('')
    f.close()

def get_debug_mode() -> bool:
    """get debug mode"""
    f = open('debug')
    v = f.read()
    f.close()
    if v:
        return True
    return False