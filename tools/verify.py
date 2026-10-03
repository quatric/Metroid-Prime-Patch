#!/usr/bin/env python3
"""Check that every patch applies cleanly to retail main.dols and round-trips.

    MP_DOL=/path/to/main.dol python3 tools/verify.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dol import Dol
import features
import patcher
from regions import REGIONS


def main():
    path = os.environ.get('MP_DOL') or os.path.join(HERE, '..', 'work', 'fst_jp', 'sys', 'main.dol')
    if not os.path.isfile(path):
        sys.exit('Retail DOL not found at %s. Set MP_DOL=/path/to/main.dol' % path)

    dol = Dol(path)
    region = patcher.detect_region(dol)
    print('Detected region: %s' % region)
    assert region == 'R3IJ01', 'Expected R3IJ01, got %s' % region
    st = patcher.status(dol, region)
    print('Initial status: %s' % st)
    for feat, s in st.items():
        assert s == 'clean', '%s is not clean: %s' % (feat, s)

    # Test patching
    patched_dol = Dol(path)
    done = patcher.patch(patched_dol, region, ['cc', 'gc'])
    print('Applied: %s' % done)
    st_patched = patcher.status(patched_dol, region)
    print('Patched status: %s' % st_patched)
    for feat, s in st_patched.items():
        assert s == 'patched', '%s is not patched: %s' % (feat, s)

    print('Verification SUCCESS!')


if __name__ == '__main__':
    main()
