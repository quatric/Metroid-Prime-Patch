"""Patch a whole disc image: extract with wit, patch sys/main.dol, rebuild.

The rebuilt image replaces the original in place, keeping its filename and
folder (USB loaders key off the `/wbfs/<Title> [ID6]/` layout); the untouched
original is kept next to it as `<name>.bak`.
"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import features
import patcher
from dol import Dol
from disc_ids import match_disc_id
from regions import REGIONS


def find_wit():
    name = 'wit.exe' if os.name == 'nt' else 'wit'
    if getattr(sys, 'frozen', False):
        for base in (getattr(sys, '_MEIPASS', None), os.path.dirname(sys.executable)):
            if base:
                bundled = os.path.join(base, name)
                if os.path.isfile(bundled):
                    return bundled
    return shutil.which('wit')


def find_file(root, name):
    for r, _, files in os.walk(root):
        if name in files:
            return os.path.join(r, name)
    return None


def read_disc_id(fst):
    boot = find_file(fst, 'boot.bin')
    if not boot:
        return None
    with open(boot, 'rb') as f:
        header = f.read(8)
    return header[0:6].decode('ascii', 'replace'), header[7]


def run_patch(image_path, log, done, which=('cc', 'gc')):
    """Patch `image_path` in place.  `which` names the features."""
    try:
        wit = find_wit()
        if wit is None:
            raise RuntimeError('wit (Wiimms ISO Tool) not found: not bundled with this '
                               'build and not on PATH')
        which = [w for w in patcher.ORDER if w in which]
        if not which:
            raise RuntimeError('nothing selected: tick at least one patch')
        fmt = '--iso' if image_path.lower().endswith('.iso') else '--wbfs'

        with tempfile.TemporaryDirectory(prefix='mp_patch_') as tmp:
            fst = os.path.join(tmp, 'fst')
            log('extracting %s...' % os.path.basename(image_path))
            r = subprocess.run([wit, 'extract', image_path, '--dest', fst, '--psel', 'data',
                                '--overwrite', '-q'], capture_output=True, text=True)
            if r.returncode:
                raise RuntimeError('extract failed:\n' + (r.stderr or r.stdout))

            got = read_disc_id(fst)
            if not got:
                raise RuntimeError('could not read sys/boot.bin from the extracted disc')
            disc_id, disc_ver = got
            region = match_disc_id(disc_id, REGIONS)
            if region is None or disc_ver != REGIONS[region]['version']:
                raise RuntimeError('%s v%d is not a Metroid Prime release this patcher knows.\n\n'
                                   'Supported: %s' % (disc_id, disc_ver, ', '.join(
                                       '%s (%s)' % (k, v['short']) for k, v in REGIONS.items())))
            log('disc: %s (%s)' % (region, REGIONS[region]['label']))

            # Collect all DOLs to patch on this disc
            # For standalone releases: sys/main.dol
            # For Metroid Prime Trilogy: sys/main.dol, files/rs5mp1_p.dol, files/rs5mp2_p.dol, files/rs5mp3_p.dol
            targets = []
            sys_main = find_file(fst, 'main.dol')
            if not sys_main or os.path.basename(os.path.dirname(sys_main)) != 'sys':
                raise RuntimeError('could not find sys/main.dol in the extracted disc')
            targets.append((sys_main, region))

            # Check for Trilogy sub-DOLs in files/
            sub_map = {
                'rs5mp1_p.dol': f'{region}_mp1',
                'rs5mp2_p.dol': f'{region}_mp2',
                'rs5mp3_p.dol': f'{region}_mp3',
            }
            files_dir = os.path.join(fst, 'files')
            if os.path.isdir(files_dir):
                for sub_fname, sub_reg in sub_map.items():
                    sub_path = os.path.join(files_dir, sub_fname)
                    if os.path.isfile(sub_path) and sub_reg in REGIONS:
                        targets.append((sub_path, sub_reg))

            total_patched = 0
            for d_path, d_reg in targets:
                d_name = os.path.basename(d_path)
                dol = Dol(d_path)
                have = patcher.status(dol, d_reg)
                todo = []
                for name in which:
                    st = have.get(name)
                    if st == 'patched':
                        log('%s: %s is already in this DOL, skipping' % (d_name, features.TITLES[name]))
                    elif st == 'clean':
                        todo.append(name)
                    else:
                        raise RuntimeError('%s: does not match retail %s (%s) -- already modified'
                                           % (d_name, REGIONS[d_reg]['label'], features.TITLES[name]))
                if todo:
                    for t in patcher.patch(dol, d_reg, todo):
                        log('  [%s] added %s' % (d_name, t))
                    dol.save(d_path)
                    log('  patched %s' % d_name)
                    total_patched += len(todo)

            if not total_patched:
                raise RuntimeError('nothing left to add: the selected patches are already in this disc.')

            staged = os.path.join(tmp, 'patched.img')
            log('rebuilding...')
            cmd = [wit, 'copy', fst, '--dest', staged, fmt, '--overwrite', '-q']
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode:
                raise RuntimeError('rebuild failed:\n' + (r.stderr or r.stdout))

            backup = image_path + '.bak'
            if os.path.exists(backup):
                log('  backup already exists, keeping it: %s' % os.path.basename(backup))
            else:
                shutil.copyfile(image_path, backup)
                log('  backed up original -> %s' % os.path.basename(backup))
            shutil.move(staged, image_path)
            log('done: patched in place, %s' % os.path.basename(image_path))
            done(True, image_path)
    except Exception as e:
        log('ERROR: %s' % e)
        done(False, str(e))
