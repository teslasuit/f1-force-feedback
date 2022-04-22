import time

from teslasuit_sdk import ts_types
from ctypes import (pointer, c_uint32)
from teslasuit_sdk.ts_device import TsDevice


class TsDeviceManager:
    def __init__(self, lib):
        self.__lib = lib

        self.devices = []

    def wait_for_device_to_connect(self):
        devices = (ts_types.TsDevice * 1)()

        while True:
            print('Waiting for a device connect...')

            number_of_devices_connected = c_uint32(1)
            self.__lib.ts_get_device_list(pointer(devices), pointer(number_of_devices_connected))
            if number_of_devices_connected.value == 1:
                break
            time.sleep(1)

        for device in list(devices):
            self.devices.append(TsDevice(self.__lib, device))

    def get_or_wait_last_device_attached(self):
        if len(self.devices) == 0:
            self.wait_for_device_to_connect()

        return self.devices[len(self.devices) - 1]
