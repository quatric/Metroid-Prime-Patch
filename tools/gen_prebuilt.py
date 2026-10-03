#!/usr/bin/env python3
"""Regenerate tools/prebuilt/*.json from src/ (needs devkitPPC and a retail main.dol).

    MP_DOLS=R3IJ01=/path/to/main.dol,R32J01=/path/to/mp2/main.dol,RM3E01=/path/to/mp3/main.dol python3 tools/gen_prebuilt.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'src')
sys.path.insert(0, HERE)
sys.path.insert(0, SRC)
from dol import Dol
from features import PREBUILT, dump
import gen_cc
import gen_gc
from regions import REGIONS


def main():
    os.makedirs(PREBUILT, exist_ok=True)
    dols = os.environ.get('MP_DOLS') or os.environ.get('MP_DOL')
    dol_map = {}
    if dols:
        for p in dols.split(','):
            p = p.strip()
            if '=' in p:
                reg, path = p.split('=', 1)
                dol_map[reg.strip()] = path.strip()
            elif os.path.isfile(p):
                dol_map['R3IJ01'] = p
    
    mp_dols = os.path.expanduser('~/mp_dols')
    for reg in REGIONS:
        cand = os.path.join(mp_dols, f'{reg}.dol')
        if reg not in dol_map and os.path.isfile(cand):
            dol_map[reg] = cand
    # MPT USA
    mpt_u = os.path.join(mp_dols, 'mpt_usa')
    dol_map.setdefault('R3ME01', os.path.join(mpt_u, 'main.dol'))
    dol_map.setdefault('R3ME01_mp1', os.path.join(mpt_u, 'rs5mp1_p.dol'))
    dol_map.setdefault('R3ME01_mp2', os.path.join(mpt_u, 'rs5mp2_p.dol'))
    dol_map.setdefault('R3ME01_mp3', os.path.join(mpt_u, 'rs5mp3_p.dol'))
    # MPT Europe
    mpt_p = os.path.join(mp_dols, 'mpt_pal')
    dol_map.setdefault('R3MP01', os.path.join(mpt_p, 'main.dol'))
    dol_map.setdefault('R3MP01_mp1', os.path.join(mpt_p, 'rs5mp1_p.dol'))
    dol_map.setdefault('R3MP01_mp2', os.path.join(mpt_p, 'rs5mp2_p.dol'))
    dol_map.setdefault('R3MP01_mp3', os.path.join(mpt_p, 'rs5mp3_p.dol'))

    for region in REGIONS:
        if region not in dol_map or not os.path.isfile(dol_map[region]):
            print("Skipping %s (DOL not found)" % region)
            continue
        print("Building prebuilt for %s from %s..." % (region, dol_map[region]))
        dol = Dol(dol_map[region])
        for name, mod in (('cc', gen_cc), ('gc', gen_gc)):
            feat = mod.build(region, dol)
            out = os.path.join(PREBUILT, '%s_%s.json' % (name, region))
            with open(out, 'w') as fh:
                json.dump(dump(feat), fh, indent=1)
                fh.write('\n')
            print("  %-3s %s: %d ops -> %s" % (name, region, len(feat.ops), os.path.relpath(out)))


if __name__ == '__main__':
    main()
