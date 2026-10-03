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
    
    default_jp = os.path.join(HERE, '..', 'work', 'fst_jp', 'sys', 'main.dol')
    default_mp2_jp = os.path.join(HERE, '..', 'work', 'fst_mp2_jp', 'sys', 'main.dol')
    default_mp3_usa = os.path.join(HERE, '..', 'work', 'fst_mp3_usa', 'sys', 'main.dol')
    if 'R3IJ01' not in dol_map and os.path.isfile(default_jp):
        dol_map['R3IJ01'] = default_jp
    if 'R32J01' not in dol_map and os.path.isfile(default_mp2_jp):
        dol_map['R32J01'] = default_mp2_jp
    if 'RM3E01' not in dol_map and os.path.isfile(default_mp3_usa):
        dol_map['RM3E01'] = default_mp3_usa

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
