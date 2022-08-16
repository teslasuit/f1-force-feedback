# F1 Force Feedback
Application for real time generation of Teslasuit haptic feedback on Teslasuit for F1 game.
Feedback generation is based on UDP Telemetry from the game.
Feedback is implemented for next game events:
- G-Forces with haptic impact based on force (Any movements, such as acceleration, braking, turning, collisions)
- Engine Vibration with haptic frequency based on engine RPM.
- Suspension shaking with haptic impact based on suspension acceleration.
- Wheel slippage for each of 4 wheels. Occurs on acceleration or braking without ABS.

## Requirements
Software:
- Teslasuit Control Center
- F1 2021 or newer official game

Hardware:
- Teslasuit device
- Gaming steering wheel and pedals

## Environment Setup
1. Install Teslasuit Control Center - https://teslasuit.io/.
2. Install Python 3 x64 from https://www.python.org/downloads/.
3. Install Steam and F1 2021 or newer game from it - https://store.steampowered.com/.
4. Install Drivers for racing wheel. For Thrustmaster - https://support.thrustmaster.com/en/product/t300rs-en/.

## Configuration
1. Turn on UDP streaming in F1 game settings at Game Options → Settings → Telemetry Settings → UDP Telemetry → On. Ensure that port number is 20777 (or setup another port in f1_client.py). If your game is newer than F1 2021 - select 2021 UDP format for compatibility.
2. Configure racing wheel for F1. For Thrustmaster: turn on wheel in PS3 mode (physical toogle), in configure tool lock rotation to max 270-360 degrees. Configuration tool by default should be at "C:\Program Files\Thrustmaster\FFB Racing wheel\drivers\tmJoycpl.exe".
3. Connect Teslasuit device to PC and calibrate it in Control Center.

## Running
1. Connect calibrated Teslasuit device to PC and launch F1 game.
2. Run main.py - it will auto detect connected device, listen game telemetry and generate haptic feedback.
3. Close main.py terminal to stop feedback.
4. It can be run from terminal to check for errors in terminal window.

## Development

### Project structure
1. Project contains two main components - F1 game client and Teslasuit client.
2. F1 game client (f1_client.py) listen UDP socket for packages from the game and generates unified force feedback events (ff_event.py).
3. Teslasuit client (ts_client.py) detects attached suit, process feedback events into playback for haptic presets. TS client includes playlist object (playlist.py) to parse assets from disk, preload assets, control assets playback and modifiers.
4. Directory ts_assets contains haptic assets for different feedback events, Teslasuit Studio project that can be used to view or modify haptic assets, template haptic calibration file that can be used to start calibration with it.

### F1 2021 UDP Spec
https://forums.codemasters.com/topic/80231-f1-2021-udp-specification/
