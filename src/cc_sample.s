# hook: KPAD sampling callback, the `stb r3,0x36(SMP_REG)` that stores the sample's
# data format (CHAN_REG = channel, SMP_REG = the sample in KPAD's ring buffer, a WPADStatus).
#
# A Classic Controller plugged into the Wii Remote is rewritten, in place, into
# the Wii Remote + Nunchuk sample the game was written for, so the rest of KPAD
# and the game run their ordinary Nunchuk code:
#
#   left stick      -> Nunchuk stick
#   right stick     -> pointer (carried to `pointer.s` in sample bytes 0x2a/0x2c)
#   buttons         -> Wii Remote / Nunchuk bits (table below)
#
# sample + 0x37 is the marker byte (bit 0 = "Classic Controller pointer"); it is
# the last byte of the 0x38-byte ring slot and nothing else uses it.
#
#   Classic Controller            Wii Remote / Nunchuk (Metroid Prime)
#   A                             A (Fire / Confirm)
#   B                             B (Jump / Cancel)
#   Y                             Missile (D-pad Down)
#   X                             Morph Ball (D-pad Up)
#   ZL                            Lock-on / Free Look (Z)
#   L                             Visor change (Minus)
#   R                             Fire Beam (A)
#   ZR                            Beam change (Plus)
#   -                             Map / Options (Minus / 1)
#   +                             Pause (Plus)
#   D-pad                         D-pad (Beams / Visors / Menus)
    stb     3, 0x36(SMP_REG)            # displaced instruction
    li      0, 0
    stb     0, 0x37(SMP_REG)            # marker: nothing synthetic yet
    lbz     4, 0x29(SMP_REG)
    cmplwi  4, 0
    bne     9f                          # only a good sample
    lbz     4, 0x28(SMP_REG)
    cmplwi  4, 2
    bne     9f                          # only a Classic Controller
    lhz     5, 0x2a(SMP_REG)            # Classic Controller buttons
    lhz     6, 0x00(SMP_REG)            # Wii Remote buttons
    lha     8, 0x2c(SMP_REG)            # left stick X
    lha     9, 0x2e(SMP_REG)            # left stick Y
    lha     10, 0x30(SMP_REG)           # right stick X
    lha     11, 0x32(SMP_REG)           # right stick Y
    li      7, 0
    mapbit  CC_A,      WM_A
    mapbit  CC_B,      WM_B
    mapbit  CC_Y,      WM_DOWN
    mapbit  CC_X,      WM_UP
    mapbit  CC_ZL,     WM_Z
    mapbit  CC_L,      WM_MINUS
    mapbit  CC_R,      WM_A
    mapbit  CC_ZR,     WM_PLUS
    mapbit  CC_MINUS,  WM_1
    mapbit  CC_PLUS,   WM_PLUS
    mapbit  CC_HOME,   WM_HOME
    mapbit  CC_UP,     WM_UP
    mapbit  CC_DOWN,   WM_DOWN
    mapbit  CC_LEFT,   WM_LEFT
    mapbit  CC_RIGHT,  WM_RIGHT
    or      6, 6, 7
    sth     6, 0x00(SMP_REG)
    # left stick (+-308) -> Nunchuk stick (+-71 is full deflection)
    mulli   8, 8, 59
    srawi   8, 8, 8
    clamp   8, 127
    mulli   9, 9, 59
    srawi   9, 9, 8
    clamp   9, 127
    # right stick (+-308) -> pointer in 1/1000ths
    dead    10, 40
    mulli   10, 10, 13
    srawi   10, 10, 2
    clamp   10, 1000
    dead    11, 40
    mulli   11, 11, 13
    srawi   11, 11, 2
    clamp   11, 1000
    li      0, 1
    stb     0, 0x28(SMP_REG)            # device: Nunchuk
    li      0, 4
    stb     0, 0x36(SMP_REG)            # data format: Nunchuk buttons + accelerometer
    stb     8, 0x30(SMP_REG)
    stb     9, 0x31(SMP_REG)
    sth     10, 0x2a(SMP_REG)
    sth     11, 0x2c(SMP_REG)
    li      0, 1
    stb     0, 0x37(SMP_REG)
9:
