# hook: KPAD sampling callback, the `addi r0,INDEX_REG,1` that follows the store
# of the sample's data format (CHAN_REG = channel, SMP_REG = sample).
#
# A GameCube pad plugged into port 0/1/2/3 is converted into a Wii Remote +
# Nunchuk sample, overwriting whatever was there (nothing, if there is no Wii
# Remote).  The displaced instruction is executed at the end.
    .set    CHAN, CHAN_REG
    .set    SMP, SMP_REG
#include gc_convert.s
    addi    0, INDEX_REG, 1             # displaced instruction
