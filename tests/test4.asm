    j    L_0
       
L_0:
    sw    $ra, 0($sp)
    addi  $sp, $sp, 32
    move  $s0, $sp

L_1:
    li    $t1, 50
    sw    $t1, -12($s0)

L_2:
    li    $t1, 6
    sw    $t1, -20($s0)

L_3:
    li    $t1, 70
    sw    $t1, -16($s0)

L_4:
    lw    $t1, -16($s0)
    li    $t2, 70
   bgt    $t1, $t2, L_6

L_5:
    j    L_9

L_6:
    lw    $t1, -16($s0)
    li    $t2, 40
   sub    $t1, $t1, $t2
    sw    $t1, -24($sp)

L_7:
    lw    $t1, -24($sp)
    sw    $t1, -16($s0)

L_8:
    j    L_4

L_9:
    lw    $t1, -12($s0)
    li    $t2, 100
   bgt    $t1, $t2, L_11

L_10:
    j    L_13

L_11:
    li    $t1, 2
    sw    $t1, -20($s0)

L_12:
    j    L_4

L_13:
    lw    $t1, -12($s0)
    li    $t2, 200
   bgt    $t1, $t2, L_15

L_14:
    j    L_17

L_15:
    li    $t1, 3
    sw    $t1, -12($s0)

L_16:
    j    L_4

L_17:
    lw    $t1, -12($s0)
    li    $t2, 30
   bgt    $t1, $t2, L_19

L_18:
    j    L_22

L_19:
    lw    $t1, -12($s0)
    li    $t2, 5
   sub    $t1, $t1, $t2
    sw    $t1, -28($sp)

L_20:
    lw    $t1, -28($sp)
    sw    $t1, -12($s0)

L_21:
    j    L_4

L_22:
    lw    $t9, -12($s0)
    li    $v0, 1
    move  $a0, $t9
    syscall
    addi    $a0, $0, 0xA
    addi    $v0, $0, 0xB
    syscall

L_23:
    li    $v0, 10
    syscall

L_24:
    j    L_23