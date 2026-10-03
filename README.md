# Metroid Prime Series (Wii) — GameCube Controller & Classic Controller Patch

Play all Wii releases of the **Metroid Prime series** with a **GameCube controller** or a **Classic Controller** — no Wii Remote or sensor bar needed for the GameCube pad.

### Supported Games
- **Metroid Prime** (*New Play Control! Metroid Prime*, `R3IJ01`)
- **Metroid Prime 2: Dark Echoes** (*New Play Control! Metroid Prime 2: Dark Echoes*, `R32J01`)
- **Metroid Prime 3: Corruption** (`RM3E01` USA, `RM3P01` Europe)
- **Metroid Prime Trilogy** (`R3ME01` USA, `R3MP01` Europe)
  - FrontEnd / Loader (`main.dol` / `rs5fe_p.dol`)
  - Metroid Prime 1 (`rs5mp1_p.dol`)
  - Metroid Prime 2: Dark Echoes (`rs5mp2_p.dol`)
  - Metroid Prime 3: Corruption (`rs5mp3_p.dol`)

### Controls

#### GameCube Controller (Port 1 - No Wii Remote needed)
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

#### Classic Controller (Plugged into Wii Remote)
- **Left Stick**: Movement / strafe
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
python3 tools/patch_disc.py "Metroid Prime 3 - Corruption (USA).wbfs" --cc --gc
```
The patcher extracts the image, applies the hooks directly to `sys/main.dol`, backs up the original as `<image>.bak`, and rebuilds the disc image.

### 2. Dolphin / Gecko Codes
Copy `codes/<ID>.ini` (`R3IJ01.ini`, `R32J01.ini`, `RM3E01.ini`) to your Dolphin `GameSettings/` directory and enable the Gecko codes.

### 3. Riivolution
Place `riivolution/<ID>.xml` on your SD card along with Riivolution.

### Modded images

Disc patchers match the first four characters of the game ID (ID4), so mods can change the last two characters. The original disc ID and filename are preserved. Revision and executable patch-site checks still apply; mods that change required code may be incompatible.
