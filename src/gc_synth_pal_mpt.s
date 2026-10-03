# hook: KPAD read in MPT PAL, `lbz r0, 0x13B(r26)`
# r26 = KPAD struct, r25 = channel (0..3)
# Ring layout:
#   write_idx: 0x13A(r26)
#   count:     0x13B(r26)
#   ring base: 0x13C(r26), element size 0x38
# Connect callback:
#   cb ptr:    0x50C(r26)
#   fired flag:0x55B(r26)
    lbz     0, 0x13B(26)
    cmpwi   0, 0
    bne     9f                          # samples waiting: remote producing them
    cmplwi  25, 3
    bgt     9f
    lbz     0, 0x13A(26)
    cmplwi  0, 16
    blt     slot
    li      0, 0
slot:
    mulli   3, 0, 0x38
    add     3, 3, 26
    addi    3, 3, 0x13C                 # the next ring slot
    li      0, 0
    stw     0, 0x00(3)
    stw     0, 0x04(3)
    stw     0, 0x08(3)
    stw     0, 0x0c(3)
    stw     0, 0x10(3)
    stw     0, 0x14(3)
    stw     0, 0x18(3)
    stw     0, 0x1c(3)
    stw     0, 0x20(3)
    stw     0, 0x24(3)
    stw     0, 0x28(3)
    stw     0, 0x2c(3)
    stw     0, 0x30(3)
    stw     0, 0x34(3)
    li      0, 0x68
    sth     0, 0x06(3)                  # accelerometer at rest
    .set    CHAN, 25
    .set    SMP, 3
#include gc_convert.s
    lbz     0, 0x37(3)
    andi.   0, 0, 2
    beq     9f                          # no pad answered
    lbz     5, 0x13A(26)
    cmplwi  5, 16
    blt     idx
    li      5, 0
idx:
    addi    5, 5, 1
    stb     5, 0x13A(26)
    lbz     5, 0x13B(26)
    cmplwi  5, 16
    bge     full
    addi    5, 5, 1
    stb     5, 0x13B(26)
full:
    # tell the game a controller has connected, once
    lwz     0, 0x50C(26)
    cmpwi   0, 0
    beq     9f
    lbz     0, 0x55B(26)
    cmpwi   0, 0
    bne     9f
    li      0, 1
    stb     0, 0x55B(26)
    mr      3, 25
    li      4, 1
    lwz     12, 0x50C(26)
    mtctr   12
    bctrl
9:
    lbz     0, 0x13B(26)                # displaced instruction
