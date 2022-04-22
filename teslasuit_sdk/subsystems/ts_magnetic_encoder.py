from ctypes import (c_void_p, c_uint8,
                    c_uint64, CFUNCTYPE,
                    POINTER, pointer,
                    Structure, cast,
                    c_uint)
from teslasuit_sdk.ts_types import TsDeviceHandle
from enum import Enum, unique, IntEnum


@unique
class TsMagneticEncoderId(Enum):
    FlexionThumb = 1
    FlexionIndex = 2
    FlexionMiddle = 3
    FlexionRing = 4
    FlexionPinky = 5

    AbductionThumb = 6
    AbductionIndex = 7
    AbductionMiddle = 8
    AbductionRing = 9
    AbductionPinky = 10


@unique
class TsForceFeedBackId(Enum):
    Thumb = 1
    Index = 2
    Middle = 3
    Ring = 4
    Pinky = 5


@unique
class TsMagneticEncoderCalibrationPose(IntEnum):
    FlexionUp = 1
    FlexionDown = 2
    AbductionLeft = 3
    AbductionRight = 4


class TsMagneticEncoderData(Structure):
    _pack_ = 1
    _fields_ = [('encoder_id', c_uint64),
                ('angle', c_uint64)]

    def __str__(self):
        return 'encoder_id = {0}, angle = {1}'.format(self.encoder_id, self.angle)


class TsMagneticEncoders(Structure):
    _pack_ = 1
    _fields_ = [('size', c_uint8),
                ('encoder_data', POINTER(TsMagneticEncoderData))]

    def __str__(self):
        data = ''
        for i in range(0, self.size):
            data += '{' + str(self.encoder_data[i]) + '}'

        return data


class TsForceFeedbackControl(Structure):
    _pack_ = 1
    _fields_ = [('servo_id', c_uint64),
                ('angle', c_uint64),
                ('reserved_1', c_uint64),
                ('reserved_2', c_uint64)]


MAGNETIC_ENCODER_LOWEST_ANGLE = 0
MAGNETIC_ENCODER_HIGHEST_ANGLE = 4095


class TsMagneticEncoder:
    def __init__(self, lib, device):
        self.__device = device
        self.__lib = lib

        self.__is_data_ready = False
        self.__is_started = False

        self.__data = TsMagneticEncoders()

        self.__data_callback = None

    def __str__(self):
        return str(self.__data)

    def __subscribe_on_data_update(self):
        def on_update_callback(device_ptr, data_ptr, size, user_data):
            data = (TsMagneticEncoderData * size)()

            for i in range(0, size):
                data[i].encoder_id = data_ptr[i].encoder_id
                data[i].angle = data_ptr[i].angle

            self.__data.size = size
            self.__data.encoder_data = cast(data, POINTER(TsMagneticEncoderData))

        glove_update_prototype = CFUNCTYPE(None, c_void_p, POINTER(TsMagneticEncoderData), c_uint64, c_void_p)
        self.__data_callback = glove_update_prototype(on_update_callback)
        self.__lib.ts_glove_me_set_update_callback(self.__device, self.__data_callback,
                                                   c_void_p())

    def get_glove_data(self):
        return self.__data

    def start_me_streaming(self):
        if self.__is_started:
            return

        self.__subscribe_on_data_update()

        self.__lib.ts_glove_me_start_streaming(self.__device)
        self.__is_started = True

    def stop_me_streaming(self):
        if not self.__is_started:
            return

        self.__lib.ts_glove_me_stop_streaming(self.__device)
        self.__is_started = False

    def calibrate_me_pose(self, calibration_pose):
        self.__lib.ts_glove_me_calibrate_by_pose(self.__device, c_uint(calibration_pose))

    def set_force_feedback_controls(self, feedback_controls):
        control_casted = (TsForceFeedbackControl * len(feedback_controls))(*feedback_controls)
        self.__lib.ts_glove_force_feedback_set_controls(self.__device,
                                                        cast(control_casted, POINTER(TsForceFeedbackControl)),
                                                        c_uint64(len(feedback_controls)))

    def release_force_feedback_controls(self, servo_ids, size):
        servo_ids_casted = (c_uint64 * size)(*servo_ids)
        self.__lib.ts_glove_force_feedback_release_controls(self.__device,
                                                            servo_ids_casted,
                                                            c_uint64(size))
