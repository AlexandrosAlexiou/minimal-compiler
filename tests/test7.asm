    j    L_7
       
L_0:
    sw    $ra, 0($sp)

L_1:
    lw    $t0, -12($sp)
    lw    $t1, 0($t0)
    lw    $t0, -16($sp)
    lw    $t2, 0($t0)
   bgt    $t1, $t2, L_3

L_2:
    j    L_5

L_3:
    li    $t1, 50
    lw    $t0, -12($sp)
    sw    $t1, 0($t0)

L_4:
    j    L_6

L_5:
    li    $t1, 51
    lw    $t0, -12($sp)
    sw    $t1, 0($t0)

L_6:
    lw    $ra, 0($sp)
    jr    $ra

L_7:
    sw    $ra, 0($sp)
    addi  $sp, $sp, 32
    move  $s0, $sp

L_8:
    li    $t1, 1
    sw    $t1, -12($s0)

L_9:
    li    $t1, 2
    sw    $t1, -16($s0)

L_10:
    addi    $fp, $sp, 32
    addi    $t0, $sp, -12
    sw    $t0, -12($fp)

L_11:
    addi    $t0, $sp, -16
    sw    $t0, -16($fp)

L_12:
    lw    $t0, -4($sp)
    sw    $t0, -4($fp)
    addi    $sp, $sp, 32
    jal     L_0
    addi    $sp, $sp, -32

L_13:
    lw    $t9, -12($s0)
    li    $v0, 1
    move  $a0, $t9
    syscall
    addi    $a0, $0, 0xA
    addi    $v0, $0, 0xB
    syscall

L_14:
    li    $v0, 10
    syscall

L_15:
    j    L_14