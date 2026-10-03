"""The retail releases of Metroid Prime (Wii).

Discs carry their own main.dol per region/release:
  R3IJ01: New Play Control! Metroid Prime (Japan)
  R32J01: New Play Control! Metroid Prime 2: Dark Echoes (Japan)
"""
REGIONS = {
    'R3IJ01': dict(label='Metroid Prime (Japan)', short='Japan', disc_id='R3IJ01', version=0, dol_size=5725664),
    'R32J01': dict(label='Metroid Prime 2: Dark Echoes (Japan)', short='MP2-Japan', disc_id='R32J01', version=0, dol_size=5725152),
}
