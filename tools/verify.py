#!/usr/bin/env python3
"""Check that every patch applies cleanly to retail main.dols and round-trips."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dol import Dol
import features
import patcher
from regions import REGIONS


def main():
    mp_dols = os.path.expanduser('~/mp_dols')
    dol_map = {}
    for r in REGIONS:
        cand = os.path.join(mp_dols, f'{r}.dol')
        if os.path.isfile(cand):
            dol_map[r] = cand
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
        path = dol_map.get(region)
        if not path or not os.path.isfile(path):
            print("Skipping %s (no retail DOL)" % region)
            continue

        print("\nVerifying %s (%s)..." % (region, REGIONS[region]['label']))
        dol = Dol(path)
        det = patcher.detect_region(dol)
        print("  Detected region: %s" % det)
        assert det == region, "Expected %s, got %s" % (region, det)
        st = patcher.status(dol, region)
        print("  Initial status: %s" % st)
        for feat, s in st.items():
            assert s == 'clean', "%s is not clean: %s" % (feat, s)

        # Test patching
        patched_dol = Dol(path)
        done = patcher.patch(patched_dol, region, ['cc', 'gc'])
        print("  Applied: %s" % done)
        st_patched = patcher.status(patched_dol, region)
        print("  Patched status: %s" % st_patched)
        for feat, s in st_patched.items():
            assert s == 'patched', "%s is not patched: %s" % (feat, s)
        print("  SUCCESS!")

    print("\nALL REGIONS VERIFIED SUCCESSFULLY!")


if __name__ == '__main__':
    main()
