    j    L_6
       
L_0:
    sw    $ra, 0($sp)

L_1:
    lw    $t1, -12($sp)
    li    $t2, 1
   add    $t1, $t1, $t2
    sw    $t1, -20($sp)

L_2:
    lw    $t1, -20($sp)
    lw    $t0, -16($sp)
    sw    $t1, 0($t0)

L_3:
    li    $t1, 4
    sw    $t1, -20($s0)

L_4:
    lw    $t0, -16($sp)
    lw    $t1, 0($t0)
    lw    $t0, -8($sp)
    sw    $t1, 0($t0)

L_5:
    lw    $ra, 0($sp)
    jr    $ra

L_6:
    sw    $ra, 0($sp)
    addi  $sp, $sp, 28
    move  $s0, $sp

L_7:
    li    $t1, 1
    sw    $t1, -12($s0)

L_8:
    addi    $fp, $sp, 28
    lw    $t0, -12($s0)
    sw    $t0, -12($fp)

L_9:
    addi    $t0, $sp, -16
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
    sw    $t1, -20($s0)

L_13:
    lw    $t9, -20($s0)
    li    $v0, 1
    move  $a0, $t9
    syscall
    addi    $a0, $0, 0xA
    addi    $v0, $0, 0xB
    syscall

L_14:
    lw    $t9, -16($s0)
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
