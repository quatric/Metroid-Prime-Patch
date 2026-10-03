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
    dol_map = {
        'R3IJ01': os.path.join(HERE, '..', 'work', 'fst_jp', 'sys', 'main.dol'),
        'R32J01': os.path.join(HERE, '..', 'work', 'fst_mp2_jp', 'sys', 'main.dol'),
        'RM3E01': os.path.join(HERE, '..', 'work', 'fst_mp3_usa', 'sys', 'main.dol'),
    }

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
