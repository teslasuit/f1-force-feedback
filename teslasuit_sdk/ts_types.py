import uuid
from ctypes import (Structure, c_uint8,
                    c_uint32, c_float)


class TsDeviceHandle(Structure):
    pass


class TsDevice(Structure):
    _pack_ = 1
    _fields_ = [('uuid', c_uint8 * 16)]

    def __str__(self):
        return str(uuid.UUID(hex=''.join(format(b, '02x') for b in self.uuid)))


class TsVersion(Structure):
    _pack_ = 1
    _fields_ = [('major', c_uint32),
                ('minor', c_uint32),
                ('patch', c_uint32),
                ('build', c_uint32)]

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}'

    def __repr__(self):
        return f'TsVersion({self.major}.{self.minor}.{self.patch}.{self.build})'

