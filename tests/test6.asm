# This file was automatically generated by: Minimal++ Compiler

    j    Lmain

L_0:
    sw    $ra, 0($sp)

L_1:
    lw    $t1, -12($sp)
    li    $t2, 1
   beq    $t1, $t2, L_3

L_2:
    j    L_5

L_3:
    lw    $t1, -12($sp)
    lw    $t0, -8($sp)
    sw    $t1, 0($t0)

L_4:
    j    L_13

L_5:
    lw    $t1, -12($sp)
    li    $t2, 1
   sub    $t1, $t1, $t2
    sw    $t1, -20($sp)

L_6:
    lw    $t1, -20($sp)
    sw    $t1, -12($sp)

L_7:
    lw    $t9, -12($sp)
    li    $v0, 1
    move  $a0, $t9
    syscall
    addi    $a0, $0, 0xA
    addi    $v0, $0, 0xB
    syscall

L_8:
    addi    $fp, $sp, 28
    lw    $t0, -12($sp)
    sw    $t0, -12($fp)

L_9:
    lw    $t0, -4($sp)
    addi    $t0, $t0, -16
    lw    $t0, 0($t0)
    sw    $t0, -16($fp)

L_10:
    addi    $t0, $sp, -24
    sw    $t0, -8($fp)

L_11:
    lw    $t0, -4($sp)
    sw    $t0, -4($fp)
    addi    $sp, $sp, 28
    jal     L_0
    addi    $sp, $sp, -28

L_12:
    lw    $t1, -24($sp)
    lw    $t0, -8($sp)
    sw    $t1, 0($t0)

L_13:
    lw    $ra, 0($sp)
    jr    $ra

Lmain:
    addi  $sp, $sp, 28
    move  $s0, $sp

L_15:
    li    $t1, 10
    sw    $t1, -16($s0)

L_16:
    li    $t1, 5
    sw    $t1, -12($s0)

L_17:
    addi    $fp, $sp, 28
    lw    $t0, -16($s0)
    sw    $t0, -12($fp)

L_18:
    addi    $t0, $sp, -12
    sw    $t0, -16($fp)

L_19:
    addi    $t0, $sp, -24
    sw    $t0, -8($fp)

L_20:
    lw    $t0, -4($sp)
    sw    $t0, -4($fp)
    addi    $sp, $sp, 28
    jal     L_0
    addi    $sp, $sp, -28

L_21:
    lw    $t1, -24($sp)
    sw    $t1, -20($s0)

L_22:
    li    $v0, 10
    syscall

L_23:
    j    L_22
