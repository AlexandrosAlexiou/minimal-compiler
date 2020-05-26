    j    Lmain
L_0:
    sw    $ra, 0($sp)

L_1:
    li    $t1, 1
    lw    $t0, -4($sp)
    addi    $t0, $t0, -12
    sw    $t1, 0($t0)

L_2:
    li    $t1, 1
    lw    $t0, -8($sp)
    sw    $t1, 0($t0)

L_3:
    lw    $ra, 0($sp)
    jr    $ra

L_4:
    sw    $ra, 0($sp)

L_5:
    addi    $fp, $sp, 20
    addi    $t0, $sp, -16
    sw    $t0, -8($fp)

L_6:
    sw    $sp, -4($fp)
    addi    $sp, $sp, 20
    jal     L_0
    addi    $sp, $sp, -20

L_7:
    lw    $t1, -16($sp)
    sw    $t1, -12($s0)

L_8:
    lw    $t1, -12($s0)
    lw    $t0, -8($sp)
    sw    $t1, 0($t0)

L_9:
    lw    $ra, 0($sp)
    jr    $ra

Lmain:    sw    $ra, 0($sp)
    addi  $sp, $sp, 20
    move  $s0, $sp

L_11:
    addi    $fp, $sp, 20
    addi    $t0, $sp, -16
    sw    $t0, -8($fp)

L_12:
    lw    $t0, -4($sp)
    sw    $t0, -4($fp)
    addi    $sp, $sp, 20
    jal     L_4
    addi    $sp, $sp, -20

L_13:
    lw    $t9, -16($sp)
    li    $v0, 1
    move  $a0, $t9
    syscall
    addi    $a0, $0, 0xA
    addi    $v0, $0, 0xB
    syscall

L_14:
    lw    $t9, -12($s0)
    li    $v0, 1
    move  $a0, $t9
    syscall
    addi    $a0, $0, 0xA
    addi    $v0, $0, 0xB
    syscall

L_15:
    li    $v0, 10
    syscall

L_16:
    j    L_15
