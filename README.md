# F1 Force Feedback
Application for force feedback with Teslasuit for F1 game. Haptic Feedback generation based on UDP Telemetry of the game.

## Requirements
Software:
- F1 2021 official game with UDP streaming enabled
- Teslasuit SDK installed
- Teslasuit Python API compatible with installed Teslasuit SDK

Hardware:
- Gaming steering wheel and pedals
- Teslasuit device

## Setup Environment
1. Install Teslasuit Studio build #18791 or higher - https://gitlab.vrweartek.com/software/teslasuit-studio/-/pipelines.
2. Install Python 3 from https://www.python.org/downloads/.
3. Install Steam and F1 2021 game from it - https://store.steampowered.com/.
4. Install Drivers for racing wheel. For thrustmaster - https://support.thrustmaster.com/en/product/t300rs-en/.

## Configuration
1. Turn on UDP streaming in F1 2021 settings. Ensure that port number is 20777 (or setup another port in f1_client.py).
2. Configure racing wheel for F1 - lock rotation to max 270-360 degrees. Configuration by default should be at "C:\Program Files\Thrustmaster\FFB Racing wheel\drivers\tmJoycpl.exe".

## Running
Run main.py - it will auto detect connected device, listen game telemetry and generate haptic feedback.
It can be run from terminal to check for any printed errors.

## Development

### Project structure
Project contains two main components - F1 game client and Teslasuit client.
F1 game client (f1_client.py) listen UDP socket for packages from the game and generated unified force feedback events (ff_event.py).
Teslasuit client (ts_client.py) detects attached suit, process feedback events into playback for haptic presets. TS client includes playlist object (playlist.py) to parse assets from disk and control their playback.

### F1 2021 UDP Spec
https://forums.codemasters.com/topic/80231-f1-2021-udp-specification/
