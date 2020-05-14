    j    L_0
       
L_0:
    sw    $ra, 0($sp)
    addi  $sp, $sp, 84
    move  $s0, $sp

L_1:
    li    $t1, 1
    li    $t2, 2
   bgt    $t1, $t2, L_3

L_2:
    j    L_6

L_3:
    lw    $t1, -16($s0)
    li    $t2, 3
   add    $t1, $t1, $t2
    sw    $t1, -20($sp)

L_4:
    lw    $t1, -20($sp)
    sw    $t1, -16($s0)

L_5:
    j    L_1

L_6:
    lw    $t1, -16($s0)
    li    $t2, 4
   add    $t1, $t1, $t2
    sw    $t1, -24($sp)

L_7:
    lw    $t1, -24($sp)
    sw    $t1, -16($s0)

L_8:
    lw    $t1, -16($s0)
    li    $t2, 5
   add    $t1, $t1, $t2
    sw    $t1, -28($sp)

L_9:
    lw    $t1, -28($sp)
    sw    $t1, -16($s0)

L_10:
    li    $t1, 6
    li    $t2, 7
   bgt    $t1, $t2, L_12

L_11:
    j    L_15

L_12:
    lw    $t1, -16($s0)
    li    $t2, 8
   add    $t1, $t1, $t2
    sw    $t1, -32($sp)

L_13:
    lw    $t1, -32($sp)
    sw    $t1, -16($s0)

L_14:
    j    L_10

L_15:
    lw    $t1, -16($s0)
    li    $t2, 9
   add    $t1, $t1, $t2
    sw    $t1, -36($sp)

L_16:
    lw    $t1, -36($sp)
    sw    $t1, -16($s0)

L_17:
    li    $t1, 0
    li    $t2, 3
   sub    $t1, $t1, $t2
    sw    $t1, -40($sp)

L_18:
    lw    $t1, -40($sp)
    li    $t2, 4
   add    $t1, $t1, $t2
    sw    $t1, -44($sp)

L_19:
    li    $t1, 0
    li    $t2, 3
   sub    $t1, $t1, $t2
    sw    $t1, -48($sp)

L_20:
    lw    $t1, -48($sp)
    li    $t2, 10
   add    $t1, $t1, $t2
    sw    $t1, -52($sp)

L_21:
    lw    $t1, -44($sp)
    lw    $t2, -52($sp)
   mul    $t1, $t1, $t2
    sw    $t1, -56($sp)

L_22:
    li    $t1, 0
    li    $t2, 3
   sub    $t1, $t1, $t2
    sw    $t1, -60($sp)

L_23:
    lw    $t1, -60($sp)
    li    $t2, 4
   add    $t1, $t1, $t2
    sw    $t1, -64($sp)

L_24:
    li    $t1, 0
    li    $t2, 3
   sub    $t1, $t1, $t2
    sw    $t1, -68($sp)

L_25:
    lw    $t1, -68($sp)
    li    $t2, 10
   add    $t1, $t1, $t2
    sw    $t1, -72($sp)

L_26:
    lw    $t1, -64($sp)
    lw    $t2, -72($sp)
   mul    $t1, $t1, $t2
    sw    $t1, -76($sp)

L_27:
    lw    $t1, -56($sp)
    lw    $t2, -76($sp)
   add    $t1, $t1, $t2
    sw    $t1, -80($sp)

L_28:
    lw    $t9, -80($sp)
    li    $v0, 1
    move  $a0, $t9
    syscall

L_29:
    li    $t9, 1000
    li    $v0, 1
    move  $a0, $t9
    syscall

L_30:
    li    $v0, 10
    syscall

L_31:
    j    L_30
