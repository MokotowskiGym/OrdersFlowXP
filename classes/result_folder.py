from typing import Dict

import zzz_tools as t


class SingletonMeta(type):
    _instances: Dict["SingletonMeta", object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ResultFolder(metaclass=SingletonMeta):
    result_dir = None

    def get_result_dir(self):
        if self.result_dir is None:
            folder_name = r"result/" + t.get_now_str()
            root_dir = t.get_dir_safe("result")
            self.result_dir = t.get_dir_safe(folder_name)
        return self.result_dir

    def get_result_sub_dir(self, sub_folder_name):
        return t.get_dir_safe(self.get_result_dir() + "/" + sub_folder_name)
