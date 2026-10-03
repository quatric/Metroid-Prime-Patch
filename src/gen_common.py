"""Shared pieces of the Classic Controller and GameCube controller builders for Metroid Prime."""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import asm
from ops import Hook
from sig import find_unique

# Site addresses in R3IJ01:
SAMPLE_STB = 0x804886CC          # stb r3,0x36(r30)   data format stored
SAMPLE_ADDI = 0x804886D0         # addi r0,r28,1      next instruction
POINTER_BL = 0x804882F8          # bl <per-sample IR/geometry>
POINTER_B = 0x804882FC           # b  <end of the sample's iteration>

PROBE_ENTRY = 0x804A6F30         # WPADProbe, first instruction (stwu r1,-0x10(r1))
RING_COUNT = 0x80487D44          # lbz r0,0x10f(r31)  KPAD read: samples waiting in the ring

# Wii Remote / Nunchuk button bits (WPAD)
WM = dict(WM_LEFT=0x0001, WM_RIGHT=0x0002, WM_DOWN=0x0004, WM_UP=0x0008, WM_PLUS=0x0010,
          WM_2=0x0100, WM_1=0x0200, WM_B=0x0400, WM_A=0x0800, WM_MINUS=0x1000,
          WM_Z=0x2000, WM_C=0x4000, WM_HOME=0x8000)
# Classic Controller button bits (WPAD)
CC = dict(CC_UP=0x0001, CC_LEFT=0x0002, CC_ZR=0x0004, CC_X=0x0008, CC_A=0x0010, CC_Y=0x0020,
          CC_B=0x0040, CC_ZL=0x0080, CC_R=0x0200, CC_PLUS=0x0400, CC_HOME=0x0800,
          CC_MINUS=0x1000, CC_L=0x2000, CC_DOWN=0x4000, CC_RIGHT=0x8000)
# GameCube pad button bits (PAD)
PAD = dict(PAD_LEFT=0x0001, PAD_RIGHT=0x0002, PAD_DOWN=0x0004, PAD_UP=0x0008, PAD_Z=0x0010,
           PAD_R=0x0020, PAD_L=0x0040, PAD_A=0x0100, PAD_B=0x0200, PAD_X=0x0400, PAD_Y=0x0800,
           PAD_START=0x1000)

# pointer scale: screen units per 1/1000th of stick travel
PTR_X = 0.00065
PTR_Y = -0.00070


def read(name):
    out = []
    for line in open(os.path.join(HERE, name)).read().split('\n'):
        out.append(read(line.split()[1]) if line.startswith('#include ') else line)
    return '\n'.join(out)


def decode_branch(word, at):
    li = word & 0x03FFFFFC
    if li & 0x02000000:
        li -= 0x04000000
    return (at + li) & 0xFFFFFFFF


def sites(region, dol):
    out = dict(stb=SAMPLE_STB, addi=SAMPLE_ADDI, bl=POINTER_BL, b=POINTER_B)
    w = {k: struct.unpack('>I', dol.read(a, 4))[0] for k, a in out.items()}
    if w['stb'] != 0x987E0036 or w['addi'] != 0x381C0001:
        raise SystemExit('%s: sample hook sites are 0x%08X 0x%08X' % (region, w['stb'], w['addi']))
    if (w['bl'] >> 26) != 18 or not (w['bl'] & 1) or (w['b'] >> 26) != 18 or (w['b'] & 1):
        raise SystemExit('%s: pointer hook sites are not bl / b' % region)
    return out, w


def pointer_source(marker, prologue='', epilogue=''):
    return (prologue + read('pointer.s').replace('MARKER', str(marker)).replace('PTR_X', repr(PTR_X)).replace(
        'PTR_Y', repr(PTR_Y)) + epilogue)


def hook(site, orig, base, source, syms, consts, note):
    words = asm.words(asm.assemble(read('macros.s') + source, base, syms, consts)) + [0]
    return Hook(site, orig, words, base, note=note), (len(words) * 4 + 15) & ~15


def gc_extra_sites(region, dol):
    out = dict(probe=PROBE_ENTRY, ring=RING_COUNT)
    w = {k: struct.unpack('>I', dol.read(a, 4))[0] for k, a in out.items()}
    if w['probe'] != 0x9421FFF0 or w['ring'] != 0x881F010F:
        raise SystemExit('%s: probe / ring sites are 0x%08X 0x%08X' % (region, w['probe'], w['ring']))
    return out, w
