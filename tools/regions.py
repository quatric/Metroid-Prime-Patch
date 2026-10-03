"""The retail releases of Metroid Prime (Wii).

Discs carry their own main.dol per region/release:
  R3IJ01: New Play Control! Metroid Prime (Japan)
  R32J01: New Play Control! Metroid Prime 2: Dark Echoes (Japan)
  RM3E01: Metroid Prime 3: Corruption (USA)
"""
REGIONS = {
    'R3IJ01': dict(label='Metroid Prime (Japan)', short='Japan', disc_id='R3IJ01', version=0, dol_size=5725664),
    'R32J01': dict(label='Metroid Prime 2: Dark Echoes (Japan)', short='MP2-Japan', disc_id='R32J01', version=0, dol_size=5725152),
    'RM3E01': dict(label='Metroid Prime 3: Corruption (USA)', short='MP3-USA', disc_id='RM3E01', version=0, dol_size=6045952),
    'RM3P01': dict(label='Metroid Prime 3: Corruption (Europe)', short='MP3-PAL', disc_id='RM3P01', version=0, dol_size=6055776),
    # Metroid Prime Trilogy (USA)
    'R3ME01': dict(label='Metroid Prime Trilogy (USA)', short='MPT-USA', disc_id='R3ME01', version=0, dol_size=5722688),
    'R3ME01_mp1': dict(label='Metroid Prime 1 (Trilogy USA)', short='MPT-USA-MP1', disc_id='R3ME01', version=0, dol_size=4957376),
    'R3ME01_mp2': dict(label='Metroid Prime 2 (Trilogy USA)', short='MPT-USA-MP2', disc_id='R3ME01', version=0, dol_size=5125472),
    'R3ME01_mp3': dict(label='Metroid Prime 3 (Trilogy USA)', short='MPT-USA-MP3', disc_id='R3ME01', version=0, dol_size=6053344),
    # Metroid Prime Trilogy (Europe)
    'R3MP01': dict(label='Metroid Prime Trilogy (Europe)', short='MPT-PAL', disc_id='R3MP01', version=0, dol_size=5744512),
    'R3MP01_mp1': dict(label='Metroid Prime 1 (Trilogy PAL)', short='MPT-PAL-MP1', disc_id='R3MP01', version=0, dol_size=4973664),
    'R3MP01_mp2': dict(label='Metroid Prime 2 (Trilogy PAL)', short='MPT-PAL-MP2', disc_id='R3MP01', version=0, dol_size=5155040),
    'R3MP01_mp3': dict(label='Metroid Prime 3 (Trilogy PAL)', short='MPT-PAL-MP3', disc_id='R3MP01', version=0, dol_size=6066880),
}
