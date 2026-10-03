import sys
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import patcher
from regions import REGIONS

class RegionIdentityTests(unittest.TestCase):
    def test_id4_filter_keeps_executable_checks(self):
        key, info = next(iter(REGIONS.items()))
        dol = Mock(data=bytearray(info['dol_size']))
        with patch.object(patcher, 'status', return_value={'cc': 'clean'}):
            self.assertEqual(patcher.detect_region(dol, info['disc_id'][:4] + '99'), key)
            self.assertIsNone(patcher.detect_region(dol, 'ZZZZ99'))
        with patch.object(patcher, 'status', return_value={'cc': 'mismatch'}):
            self.assertIsNone(patcher.detect_region(dol, info['disc_id'][:4] + '99'))
