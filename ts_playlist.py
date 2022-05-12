import os

from teslasuit_sdk import ts_api
from teslasuit_sdk.subsystems import ts_haptic
from teslasuit_sdk.ts_mapper import TsBone2dIndex

class TsPlaylist:
    def __init__(self, api, device, assets_path):
        self.api = api
        self.device = device
        self.player = self.device.haptic
        self.load_assets(assets_path)

    def load_assets(self, assets_path):
        for file in os.listdir(assets_path):
            if file.endswith(".ts_asset"):
                print(file)

    def unload_assets(self):
        print("unload assets")

