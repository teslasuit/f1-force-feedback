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
        if event.type == FeedbackEventType.GForce:
            if event.direction == FeedbackEventDirection.Back:
                return "_g_force_back.ts_asset"
            elif event.direction == FeedbackEventDirection.Front:
                return "_g_force_front.ts_asset"
            elif event.direction == FeedbackEventDirection.Left:
                return "_g_force_left.ts_asset"
            elif event.direction == FeedbackEventDirection.Right:
                return "_g_force_right.ts_asset"
        elif event.type == FeedbackEventType.Vibration:
            return "_rpm_vibration.ts_asset"
        elif event.type == FeedbackEventType.Slip:
            if event.location == FeedbackEventLocation.FrontLeftDown:
                return "_slip_fl.ts_asset"
            elif event.location == FeedbackEventLocation.FrontRightDown:
                return "_slip_fr.ts_asset"
            elif event.location == FeedbackEventLocation.RearLeftDown:
                return "_slip_rl.ts_asset"
            elif event.location == FeedbackEventLocation.RearRightDown:
                return "_slip_rr.ts_asset"
        elif event.type == FeedbackEventType.Shaking:
            if event.location == FeedbackEventLocation.FrontLeftDown:
                return "_shaking_fl.ts_asset"
            elif event.location == FeedbackEventLocation.FrontRightDown:
                return "_shaking_fr.ts_asset"
            elif event.location == FeedbackEventLocation.RearLeftDown:
                return "_shaking_rl.ts_asset"
            elif event.location == FeedbackEventLocation.RearRightDown:
                return "_shaking_rr.ts_asset"
        return None
