import os

from teslasuit_sdk import ts_api
from teslasuit_sdk.subsystems import ts_haptic
from teslasuit_sdk.ts_mapper import TsBone2dIndex

class TsPlaylist:
    def __init__(self, api, device, assets_path):
        self.api = api
        self.asset_manager = api.asset_manager
        self.device = device
        self.player = self.device.haptic
        self.__load_assets(assets_path)

    def __del__(self):
        self.__unload_assets()

    def __load_assets(self, assets_path):
        self.assets = dict()
        for file in os.listdir(assets_path):
            if file.endswith(".ts_asset"):
                path = os.path.join(assets_path, file)
                print("Load asset: ", path)
                asset_handle = self.asset_manager.load_asset_from_path(path)
                print("Create playable")
                playable_id = self.player.create_playable(asset_handle, True)
                self.assets[file] = TsAssetInfo(file, asset_handle, playable_id)
                
    def __unload_assets(self):
        for asset_info in self.assets:
            self.player.remove_playable(asset_info.playable_id)
            self.asset_manager.unload_asset(asset_info.asset_handle)

    def play(self, name, is_continue=True, intensity_percent=1, frequency_percent=1):
        # find asset info
        asset_info = self.assets.get(name)
        # check if asset existing
        if asset_info == None:
            print("Asset not found: ", name)
            return
        # stop before restart if not continue
        if not is_continue:
            self.stop(name)
        # set multipliers
        multipliers = self.player.create_touch_multipliers(frequency_percent, intensity_percent, intensity_percent)
        self.player.set_playable_multipliers(asset_info.playable_id, multipliers)
        # start if not playing
        if not asset_info.is_playing:
            print("Play:", asset_info.name)
            asset_info.is_playing = True
            self.player.play_playable(asset_info.playable_id)

    def stop(self, name):
        asset_info = self.assets.get(name)
        if asset_info == None:
            print("Asset not found: ", name)
            return
        asset_info = self.assets[name]
        print("Stop:", asset_info.name)
        asset_info.is_playing = False
        self.player.stop_playable(asset_info.playable_id)


class TsAssetInfo:
    def __init__(self, name, asset_handle, playable_id):
        self.name = name
        self.asset_handle = asset_handle
        self.playable_id = playable_id
        self.is_playing = False
        