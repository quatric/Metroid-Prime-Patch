#!/usr/bin/env python3
"""Regenerate tools/prebuilt/*.json from src/ (needs devkitPPC and a retail main.dol).

    MP_DOL=/path/to/main.dol python3 tools/gen_prebuilt.py
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
            if os.path.isfile(p):
                dol_map['R3IJ01'] = p
    default_jp = os.path.join(HERE, '..', 'work', 'fst_jp', 'sys', 'main.dol')
    if 'R3IJ01' not in dol_map and os.path.isfile(default_jp):
        dol_map['R3IJ01'] = default_jp

    for region in REGIONS:
        if region not in dol_map:
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
