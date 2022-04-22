import socket
from struct import *
from ctypes import *
from collections import namedtuple

from teslasuit_sdk import ts_api
from teslasuit_sdk.subsystems.ts_haptic import TsHapticParam, TsHapticParamType, DEFAULT_LAYOUT_INDEX
from teslasuit_sdk.ts_mapper import Bone2dIndex

PORT = 20777
MAX_PACKET_SIZE = 65535

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



class F1TeslatuitForceFeedback:
    def start(self):
        self.setup_ts()
        self.setup_f1()
        while True:
            self.process_packet()

    def setup_f1(self):
        print("Connecting to F1 game...")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(("", PORT))
        print("Game connected.")    

    def setup_ts(self):
        print("Connecting teslasuit device...")
        api = ts_api.TsApi()
        device_manager = api.get_device_manager()
        device = device_manager.get_or_wait_last_device_attached()
        self.player = device.haptic
        mapper = api.mapper
        mapping_handle = device.get_mapping()
        layouts = mapper.get_layouts(mapping_handle)
        self.bones = mapper.get_layout_bones(layouts[DEFAULT_LAYOUT_INDEX])
        print("Device connected.")
        self.play_test_touch(mapper.get_bone_contents(self.bones[Bone2dIndex.RightUpperArm.value])) # todo: remove

    def play_test_touch(self, channels):
        params = [TsHapticParam() for i in range(0, 3)]
        params[0].type = TsHapticParamType.Period.value
        params[0].value = 100
        params[1].type = TsHapticParamType.Amplitude.value
        params[1].value = 40
        params[2].type = TsHapticParamType.PulseWidth.value
        params[2].value = 150
        playable_id = self.player.create_touch(params, channels, 1000)
        self.player.play_playable(playable_id)

    def process_packet(self):
        self.packet, addr = self.client.recvfrom(MAX_PACKET_SIZE)
        #packetFormat, gameMajorVersion, gameMinorVersion, packetVersion, packetId, sessionUID, sessionTime, frameIdentifier, playerCarIndex, secondaryPlayerCarIndex = unpack('<HBBBBQfLBB', self.packet[0:24])
        header = PacketHeader();
        header_size = 24
        memmove(addressof(header), self.packet[0:header_size], header_size)

        #print("Message received [id, frame, timestamp]:", str(packetId), ",", str(frameIdentifier), ",", str(sessionTime), ".")
        print("Message received [id, frame, timestamp]:", str(header.packetId), ",", str(header.frameIdentifier), ",", str(header.sessionTime), ".")
        print("-------------------------")


ff = F1TeslatuitForceFeedback()
ff.start()
