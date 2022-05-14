from teslasuit_sdk import ts_api
from teslasuit_sdk.subsystems import ts_haptic
from teslasuit_sdk.ts_mapper import TsBone2dIndex

import ts_playlist
from ff_event import FeedbackEvent, FeedbackEventType, FeedbackEventDirection, FeedbackEventLocation

class TsClient:
    def init(self, lib_path=None):
        print("Connecting teslasuit device...")
        api = ts_api.TsApi(lib_path)
        device = api.get_device_manager().get_or_wait_last_device_attached()
        self.player = device.haptic
        self.bones = api.mapper.get_layout_bones(api.mapper.get_haptic_electric_channel_layout(device.get_mapping()))
        print("Device connected.")
        print("Loading TS assets...")
        self.playlist = ts_playlist.TsPlaylist(api, device, "ts_assets")
        print("TS assets loaded.")

    def play_touch(self, params, channels, duration_ms):
        playable_id = player.create_touch(params, channels, duration_ms)
        self.player.play_playable(playable_id)

    def test_haptic(self):
        params = player.create_touch_parameters(100, 40, 150)
        bones = mapper.get_bone_contents(self.bones[TsBone2dIndex.RightUpperArm.value])
        duration_ms = 1000
        self.play_touch(params, bones, duration_ms)
        time.sleep(duration_ms / 1000)

    def process_ff_events(self, events):
        asset = None
        for event in events:
            asset_name = self.get_asset_name(event)
            if asset_name == None:
                continue
            if event.is_enable:
                self.playlist.play(asset_name, event.is_continue, event.intensity_percent, event.frequency_percent)
            else:
                self.playlist.stop(asset_name)

    def get_asset_name(self, event):
        if event.type == FeedbackEventType.Acceleration:
            return "acceleration.ts_asset"
        elif event.type == FeedbackEventType.Breaking:
            return "breaking.ts_asset"
        elif event.type == FeedbackEventType.Vibration:
            return "engine_rpm.ts_asset"
        else:
            return None
