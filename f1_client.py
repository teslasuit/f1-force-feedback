import socket
from struct import *
from ctypes import *
from enum import IntEnum, unique
from collections import namedtuple

PORT = 20777
MAX_PACKET_SIZE = 65535

class F1Client:
    def init(self):
        print("Connecting to F1 game...")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(("", PORT))
        print("Game connected.")

    def process(self):
        self.packet, addr = self.client.recvfrom(MAX_PACKET_SIZE)
        header = PacketHeader();
        header_size = 24
        memmove(addressof(header), self.packet[0:header_size], header_size)
        #print("Game packet received [id, frame, timestamp]:", str(header.packetId), ",", str(header.frameIdentifier), ",", str(header.sessionTime), ".")
        #print("-------------------------")
        if header.packetId == PacketId.CarTelemetry:
            self.process_telemetry(self.packet, header_size)

    def process_telemetry(self, packet, offset=0):
        print("Telemetry packet received.")


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