"""Storage framework for saving simple values as key-storage type"""

import os


class SettingStorage:

    def set_value(key: str, value: str) -> None:
        """set value"""
        if value:
            with open('storage_' + key, 'wt+') as f:
                f.write(value)
                f.close()
        else:
            os.remove('storage_' + key)

    def get_value(key: str) -> str:
        """get value as string"""
        try:
            with open('storage_' + key, 'rt') as f:
                v = f.read()
                f.close()
                return v
        except OSError:
            return '0'
