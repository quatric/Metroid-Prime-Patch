"""Shared pieces of the Classic Controller and GameCube controller builders for Metroid Prime series."""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import asm
from ops import Hook

REGION_SITES = {
    'R3IJ01': dict(
        stb=0x804886CC,
        addi=0x804886D0,
        bl=0x804882F8,
        b=0x804882FC,
        probe=0x804A6F30,
        ring=0x80487D44,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFEF19,
        b_op=0x48000008,
    ),
    'R32J01': dict(
        stb=0x80488554,
        addi=0x80488558,
        bl=0x80488180,
        b=0x80488184,
        probe=0x804A6DB8,
        ring=0x80487BCC,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFEF19,
        b_op=0x48000008,
    ),
    'RM3E01': dict(
        stb=0x804D9C1C,
        addi=0x804D9C20,
        bl=0x804D97F0,
        b=0x804D97F4,
        probe=0x804F66B8,
        ring=0x804D923C,
        smp_reg=28,
        chan_reg=30,
        index_reg=29,
        stb_op=0x987C0036,
        addi_op=0x381D0001,
        bl_op=0x4BFFEF2D,
        b_op=0x48000008,
    ),
    'RM3P01': dict(
        stb=0x804DB928,
        addi=0x804DB92C,
        bl=0x804DB4FC,
        b=0x804DB500,
        probe=0x804F83C4,
        ring=0x804DAF48,
        smp_reg=28,
        chan_reg=30,
        index_reg=29,
        stb_op=0x987C0036,
        addi_op=0x381D0001,
        bl_op=0x4BFFEF2D,
        b_op=0x48000008,
    ),
    # Metroid Prime Trilogy (USA) - Main & Games
    'R3ME01': dict(
        stb=0x80487E60,
        addi=0x80487E64,
        bl=0x80487A54,
        b=0x80487A58,
        probe=0x804A6718,
        ring=0x804874A0,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFEF19,
        b_op=0x48000008,
    ),
    'R3ME01_mp1': dict(
        stb=0x803BD850,
        addi=0x803BD854,
        bl=0x803BD444,
        b=0x803BD448,
        probe=0x803D7E0C,
        ring=0x803BCE90,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFEF19,
        b_op=0x48000008,
    ),
    'R3ME01_mp2': dict(
        stb=0x803F0638,
        addi=0x803F063C,
        bl=0x803F022C,
        b=0x803F0230,
        probe=0x8040AB24,
        ring=0x803EFC78,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFEF19,
        b_op=0x48000008,
    ),
    'R3ME01_mp3': dict(
        stb=0x804D9EB4,
        addi=0x804D9EB8,
        bl=0x804D9AA8,
        b=0x804D9AAC,
        probe=0x804F8764,
        ring=0x804D94F4,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFEF19,
        b_op=0x48000008,
    ),
    # Metroid Prime Trilogy (Europe) - Main & Games
    'R3MP01': dict(
        stb=0x80488924,
        addi=0x80488928,
        bl=0x80487F2C,
        b=0x80487F30,
        probe=0x804A779C,
        ring=0x804879F0,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFE9B9,
        b_op=0x48000010,
        ring_op=0x881A013B,
        ring_src='gc_synth_pal_mpt.s',
    ),
    'R3MP01_mp1': dict(
        stb=0x803BE76C,
        addi=0x803BE770,
        bl=0x803BDD74,
        b=0x803BDD78,
        probe=0x803D92E8,
        ring=0x803BD838,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFE9B9,
        b_op=0x48000010,
        ring_op=0x881A013B,
        ring_src='gc_synth_pal_mpt.s',
    ),
    'R3MP01_mp2': dict(
        stb=0x803F411C,
        addi=0x803F4120,
        bl=0x803F3724,
        b=0x803F3728,
        probe=0x8040EBC8,
        ring=0x803F31E8,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFE9B9,
        b_op=0x48000010,
        ring_op=0x881A013B,
        ring_src='gc_synth_pal_mpt.s',
    ),
    'R3MP01_mp3': dict(
        stb=0x804DA448,
        addi=0x804DA44C,
        bl=0x804D9A50,
        b=0x804D9A54,
        probe=0x804F92B8,
        ring=0x804D9514,
        smp_reg=30,
        chan_reg=29,
        index_reg=28,
        stb_op=0x987E0036,
        addi_op=0x381C0001,
        bl_op=0x4BFFE9B9,
        b_op=0x48000010,
        ring_op=0x881A013B,
        ring_src='gc_synth_pal_mpt.s',
    ),
}

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
    cfg = REGION_SITES[region]
    out = {k: cfg[k] for k in ('stb', 'addi', 'bl', 'b')}
    w = {k: struct.unpack('>I', dol.read(a, 4))[0] for k, a in out.items()}
    if w['stb'] != cfg['stb_op'] or w['addi'] != cfg['addi_op']:
        raise SystemExit('%s: sample hook sites are 0x%08X 0x%08X (expected 0x%08X 0x%08X)' % (
            region, w['stb'], w['addi'], cfg['stb_op'], cfg['addi_op']))
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
    cfg = REGION_SITES[region]
    out = {k: cfg[k] for k in ('probe', 'ring')}
    w = {k: struct.unpack('>I', dol.read(a, 4))[0] for k, a in out.items()}
    exp_ring = cfg.get('ring_op', 0x881F010F)
    if w['probe'] != 0x9421FFF0 or w['ring'] != exp_ring:
        raise SystemExit('%s: probe / ring sites are 0x%08X 0x%08X (expected 0x%08X 0x%08X)' % (
            region, w['probe'], w['ring'], 0x9421FFF0, exp_ring))
    return out, w

