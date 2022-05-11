import socket
from struct import *
from ctypes import *
from enum import IntEnum, unique
from collections import namedtuple

PORT = 20777
MAX_PACKET_SIZE = 65535

@unique
class FeedbackEventType(IntEnum):
    Undefined = 0
    Acceleration = 1
    Breaking = 2
    GForce = 3
    Vibration = 4
    Shaking = 5
    Slip = 6
    Lag = 7

@unique
class FeedbackEventDirection(IntEnum):
    Undefined = 0
    Front = 1
    Back = 2
    Left = 3
    Right = 4
    Up = 5
    Down = 6

@unique
class FeedbackEventLocation(IntEnum):
    Undefined = 0
    FrontLeftDown = 1
    FrontRightDown = 2
    RearLeftDown = 3
    RearRightDown = 4
    FrontLeftUp = 1
    FrontRightUp = 2
    RearLeftUp = 3
    RearRightUp = 4

class FeedbackEvent:
    def __init__(self):
        self.enable = True
        self.type = FeedbackEventType.Undefined
        self.direction = FeedbackEventDirection.Undefined
        self.location = FeedbackEventLocation.Undefined
        self.intensity_percent = float(0)
        self.frequency_percent = float(0)

class F1Client:
    def init(self):
        print("Connecting to F1 game...")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(("", PORT))
        print("Game connected.")

    def set_event_callback(self, callback):
        self.event_callback = callback

    def process(self):
        self.packet, addr = self.client.recvfrom(MAX_PACKET_SIZE)
        header = PacketHeader()
        memmove(addressof(header), self.packet[0:header.get_size()], header.get_size())
        self.events = list()
        #print("Game packet received [id, frame, timestamp]:", str(header.packetId), ",", str(header.frameIdentifier), ",", str(header.sessionTime), ".")
        #print("-------------------------")
        if header.packetId == PacketId.Motion:
            self.process_motion(self.packet, header.get_size(), header.playerCarIndex)
        if header.packetId == PacketId.CarTelemetry:
            self.process_telemetry(self.packet, header.get_size(), header.playerCarIndex)
        if self.event_callback != None:
            self.event_callback(self.events)


    def process_motion(self, packet, offset, player_car_index):
        motion_data = PacketMotionData()
        memmove(addressof(motion_data), packet[offset:motion_data.get_size()], motion_data.get_size())
        #print("Wheel speed:", motion_data.wheelSpeed[0])

    def process_telemetry(self, packet, offset, player_car_index):
        telemetry_data = PacketCarTelemetryData()
        memmove(addressof(telemetry_data), packet[offset:telemetry_data.get_size()], telemetry_data.get_size())
        print("Speed:", telemetry_data.carTelemetryData[player_car_index].speed)


#######################################################################################################################

class PacketHeader(Structure):
    _pack_ = 1
    _fields_ = [("packetFormat", c_uint16),           # 2021
                ("gameMajorVersion", c_uint8),        # Game major version - "X.00"
                ("gameMinorVersion", c_uint8),        # Game minor version - "1.XX"
                ("packetVersion", c_uint8),           # Version of this packet type, all start from 1
                ("packetId", c_uint8),                # Identifier for the packet type, see below
                ("sessionUID", c_uint64),             # Unique identifier for the session
                ("sessionTime", c_float),             # Session timestamp
                ("frameIdentifier", c_uint32),        # Identifier for the frame the data was retrieved on
                ("playerCarIndex", c_uint8),          # Index of player's car in the array
                ("secondaryPlayerCarIndex", c_uint8)] # Index of secondary player's car in the array (splitscreen)
    def get_size(self):
        return 24

@unique
class PacketId(IntEnum):
    Motion = 0              # Contains all motion data for player’s car – only sent while player is in control
    Session = 1             # Data about the session – track, time left
    LapData = 2             # Data about all the lap times of cars in the session
    Event = 3               # Various notable events that happen during a session
    Participants = 4        # List of participants in the session, mostly relevant for multiplayer
    CarSetups = 5           # Packet detailing car setups for cars in the race
    CarTelemetry = 6        # Telemetry data for all cars
    CarStatus = 7           # Status data for all cars
    FinalClassification = 8 # Final classification confirmation at the end of a race
    LobbyInfo = 9           # Information about players in a multiplayer lobby
    CarDamage = 10          # Damage status for all cars
    SessionHistory = 11     # Lap and tyre data for session

class CarMotionData(Structure):
    _pack_ = 1
    _fields_ = [("worldPositionX", c_float),     # World space X position
                ("worldPositionY", c_float),     # World space Y position
                ("worldPositionZ", c_float),     # World space Z position
                ("worldVelocityX", c_float),     # Velocity in world space X
                ("worldVelocityY", c_float),     # Velocity in world space Y
                ("worldVelocityZ", c_float),     # Velocity in world space Z
                ("worldForwardDirX", c_int16),   # World space forward X direction (normalised)
                ("worldForwardDirY", c_int16),   # World space forward Y direction (normalised)
                ("worldForwardDirZ", c_int16),   # World space forward Z direction (normalised)
                ("worldRightDirX", c_int16),     # World space right X direction (normalised)
                ("worldRightDirY", c_int16),     # World space right Y direction (normalised)
                ("worldRightDirZ", c_int16),     # World space right Z direction (normalised)
                ("gForceLateral", c_float),      # Lateral G-Force component
                ("gForceLongitudinal", c_float), # Longitudinal G-Force component
                ("gForceVertical", c_float),     # Vertical G-Force component
                ("yaw", c_float),                # Yaw angle in radians
                ("pitch", c_float),              # Pitch angle in radians
                ("roll", c_float)]               # Roll angle in radians

class PacketMotionData(Structure):
    _pack_ = 1
    _fields_ = [#("header", PacketHeader),               # Header
                ("carMotionData", CarMotionData * 22),   # Data for all cars on track
                # Extra player car ONLY data
                ("suspensionPosition", c_float * 4),     # Note: All wheel arrays have the following order:
                ("suspensionVelocity", c_float * 4),     # RL, RR, FL, FR
                ("suspensionAcceleration", c_float * 4), # RL, RR, FL, FR
                ("wheelSpeed", c_float * 4),             # Speed of each wheel
                ("wheelSlip", c_float * 4),              # Slip ratio for each wheel
                ("localVelocityX", c_float),             # Velocity in local space
                ("localVelocityY", c_float),             # Velocity in local space
                ("localVelocityZ", c_float),             # Velocity in local space
                ("angularVelocityX", c_float),           # Angular velocity x-component
                ("angularVelocityY", c_float),           # Angular velocity y-component
                ("angularVelocityZ", c_float),           # Angular velocity z-component
                ("angularAccelerationX", c_float),       # Angular velocity x-component
                ("angularAccelerationY", c_float),       # Angular velocity y-component
                ("angularAccelerationZ", c_float),       # Angular velocity z-component
                ("frontWheelsAngle", c_float)]           # Current front wheels angle in radians
    def get_size(self):
        return 1440

class CarTelemetryData(Structure):
    _pack_ = 1
    _fields_ = [("speed", c_uint16),                      # Speed of car in kilometres per hour
                ("throttle", c_float),                    # Amount of throttle applied (0.0 to 1.0)
                ("steer", c_float),                       # Steering (-1.0 (full lock left) to 1.0 (full lock right))
                ("brake", c_float),                       # Amount of brake applied (0.0 to 1.0)
                ("clutch", c_uint8),                      # Amount of clutch applied (0 to 100)
                ("gear", c_int8),                         # Gear selected (1-8, N=0, R=-1)
                ("engineRPM", c_uint16),                  # Engine RPM
                ("drs", c_uint8),                         # 0 = off, 1 = on
                ("revLightsPercent", c_uint8),            # Rev lights indicator (percentage)
                ("revLightsBitValue", c_uint16),          # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
                ("brakesTemperature", c_uint16 * 4),      # Brakes temperature (celsius)
                ("tyresSurfaceTemperature", c_uint8 * 4), # Tyres surface temperature (celsius)
                ("tyresInnerTemperature", c_uint8 * 4),   # Tyres inner temperature (celsius)
                ("engineTemperature", c_uint16),          # Engine temperature (celsius)
                ("tyresPressure", c_float * 4),           # Tyres pressure (PSI)
                ("surfaceType", c_uint8 * 4)]             # Driving surface, see appendices

class PacketCarTelemetryData(Structure):
    _pack_ = 1
    _fields_ = [#("header", PacketHeader),                   # Header
                ("carTelemetryData", CarTelemetryData * 22), # Data for all cars on track
                ("mfdPanelIndex", c_uint8),                  # Index of MFD panel open - 255 = MFD closed; Single player, race – 0 = Car setup, 1 = Pits, 2 = Damage, 3 =  Engine, 4 = Temperatures; May vary depending on game mode
                ("mfdPanelIndexSecondaryPlayer", c_uint8),   # See above
                ("suggestedGear", c_int8)]                   # Suggested gear for the player (1-8), 0 if no gear suggested
    def get_size(self):
        return 1323
