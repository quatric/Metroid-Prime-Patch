# Metroid Prime (Wii) — GameCube Controller & Classic Controller Patch

Play the Wii release of **Metroid Prime** (*New Play Control! Metroid Prime*, R3IJ01) with a **GameCube controller** or a **Classic Controller** — no Wii Remote or sensor bar needed for the GameCube pad.

Includes:
- **GameCube controller support** (Port 1): fully standalone, connects natively without a Wii Remote. Controls mapped to match the original GameCube game:
  - **Control Stick**: Movement / strafe
  - **C-Stick**: Aiming / Pointer control
  - **A**: Fire Beam / Confirm
  - **B**: Jump / Cancel
  - **Y**: Missile
  - **X**: Morph Ball
  - **L**: Lock-on / Free Look
  - **R**: Fire Beam
  - **Z**: Visor select
  - **Start**: Pause
- **Classic Controller support**: plug a Classic Controller into your Wii Remote:
  - **Left Stick**: Movement
  - **Right Stick**: Aiming / Pointer control
  - **A / R**: Fire Beam
  - **B**: Jump
  - **Y**: Missile
  - **X**: Morph Ball
  - **ZL**: Lock-on / Free Look
  - **L**: Visor select
  - **ZR**: Beam select
  - **+ / -**: Pause / Map

## Install Methods

### 1. Patch your disc image (WBFS / ISO)
Run the GUI patcher (drag-and-drop):
```bash
python3 tools/gui.py
```
Or command line:
```bash
python3 tools/patch_disc.py "Metroid Prime (Japan).wbfs" --cc --gc
```
The patcher extracts the image, applies the hooks directly to `sys/main.dol`, backs up the original as `<image>.bak`, and rebuilds the disc image.

### 2. Dolphin / Gecko Codes
Copy `codes/R3IJ01.ini` to your Dolphin `GameSettings/` directory and enable the Gecko codes.

### 3. Riivolution
Place `riivolution/R3IJ01.xml` on your SD card along with Riivolution.
