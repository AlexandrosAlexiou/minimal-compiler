    j    L_38
      
L_0:
    sw    $ra, 0($sp)

L_1:
    li    $t1, 0
    li    $t2, 3
   sub    $t1, $t1, $t2
    sw    $t1, -28($sp)

L_2:
    lw    $t1, -28($sp)
    li    $t2, 5
   blt    $t1, $t2, L_6

L_3:
    j    L_4

L_4:
    li    $t1, 5
    li    $t2, 4
   bgt    $t1, $t2, L_6

L_5:
    j    L_8

L_6:
    li    $t1, 3
    sw    $t1, -20($sp)

L_7:
    j    L_9

L_8:
    li    $t1, 4
    sw    $t1, -20($sp)

L_9:
    li    $t1, 1000
    li    $t2, 300
   bgt    $t1, $t2, L_11

L_10:
    j    L_15

L_11:
    li    $t1, 10
    li    $t2, 100
   blt    $t1, $t2, L_13

L_12:
    j    L_15

L_13:
    li    $t1, 3
    sw    $t1, -20($sp)

L_14:
    j    L_16

L_15:
    li    $t1, 555
    sw    $t1, -20($sp)

L_16:
    li    $t1, 5
    li    $t2, 3
   bgt    $t1, $t2, L_18

L_17:
    j    L_21

L_18:
    lw    $t1, -20($sp)
    li    $t2, 3
   sub    $t1, $t1, $t2
    sw    $t1, -32($sp)

L_19:
    lw    $t1, -32($sp)
    sw    $t1, -20($sp)

L_20:
    j    L_16

L_21:
    lw    $t0, -4($sp)
    addi    $t0, $t0, -28
    lw    $t1, 0($t0)
    li    $t2, 30
   bgt    $t1, $t2, L_23

L_22:
    j    L_26

L_23:
    lw    $t1, -20($sp)
    li    $t2, 100
   sub    $t1, $t1, $t2
    sw    $t1, -36($sp)

L_24:
    lw    $t1, -36($sp)
    sw    $t1, -20($sp)

L_25:
    j    L_21

L_26:
    lw    $t1, -16($sp)
    lw    $t0, -8($sp)
    sw    $t1, 0($t0)
    lw    $ra, 0($sp)
    jr    $ra

L_27:
    lw    $ra, 0($sp)
    jr    $ra

L_28:
    sw    $ra, 0($sp)

L_29:
    addi    $fp, $sp, -44
    lw    $t0, -32($sp)
    sw    $t0, -12($fp)

L_30:
    addi    $t0, $sp, -36
    sw    $t0, -8($fp)

L_31:
    sw    $sp, -4($fp)
    addi    $sp, $sp, 44
    jal     L_0
    addi    $sp, $sp, -44

L_32:
    addi    $fp, $sp, -44
    lw    $t0, -36($sp)
    sw    $t0, -12($fp)

L_33:
    addi    $t0, $sp, -40
    sw    $t0, -8($fp)

L_34:
    sw    $sp, -4($fp)
    addi    $sp, $sp, 44
    jal     L_0
    addi    $sp, $sp, -44

L_35:
    lw    $t1, -40($sp)
    sw    $t1, -20($sp)

L_36:
    lw    $t1, -20($sp)
    lw    $t0, -8($sp)
    sw    $t1, 0($t0)
    lw    $ra, 0($sp)
    jr    $ra

L_37:
    lw    $ra, 0($sp)
    jr    $ra

L_38:
    sw    $ra, 0($sp)
    addi  $sp, $sp, 36
    move  $s0, $sp

L_39:
    addi    $fp, $sp, -36
    lw    $t0, -12($s0)
    sw    $t0, -12($fp)

L_40:
    lw    $t0, -16($s0)
    sw    $t0, -16($fp)

L_41:
    addi    $t0, $sp, -32
    sw    $t0, -8($fp)

L_42:
    lw    $t0, -4($sp)
    sw    $t0, -4($fp)
    addi    $sp, $sp, 36
    jal     L_28
    addi    $sp, $sp, -36

L_43:
    lw    $t1, -32($sp)
    sw    $t1, -28($s0)

L_44:
    li    $v0, 10
    syscall

L_45:
    j    L_44
