    j    L_0
       
L_0:
    sw    $ra, 0($sp)
    addi  $sp, $sp, 36
    move  $s0, $sp

L_1:
    li    $t1, 100
    sw    $t1, -12($s0)

L_2:
    lw    $t1, -12($s0)
    li    $t2, 10
   add    $t1, $t1, $t2
    sw    $t1, -20($sp)

L_3:
    lw    $t1, -20($sp)
    sw    $t1, -16($s0)

L_4:
    li    $t1, 0
    li    $t2, 3
   sub    $t1, $t1, $t2
    sw    $t1, -24($sp)

L_5:
    lw    $t1, -24($sp)
    li    $t2, 5
   blt    $t1, $t2, L_17

L_6:
    j    L_7

L_7:
    li    $t1, 5
    li    $t2, 4
   bgt    $t1, $t2, L_9

L_8:
    j    L_17

L_9:
    lw    $t1, -12($s0)
    lw    $t2, -16($s0)
   blt    $t1, $t2, L_15

L_10:
    j    L_11

L_11:
    lw    $t1, -12($s0)
    lw    $t2, -16($s0)
   bgt    $t1, $t2, L_13

L_12:
    j    L_15

L_13:
    li    $t1, 1
    sw    $t1, -12($s0)

L_14:
    j    L_16

L_15:
    li    $t1, 2
    sw    $t1, -12($s0)

L_16:
    j    L_17

L_17:
    lw    $t1, -12($s0)
    li    $t2, 1
   bgt    $t1, $t2, L_19

L_18:
    j    L_23

L_19:
    lw    $t1, -12($s0)
    li    $t2, 2
   blt    $t1, $t2, L_21

L_20:
    j    L_23

L_21:
    li    $t1, 3
    sw    $t1, -12($s0)

L_22:
    j    L_24

L_23:
    li    $t1, 4
    sw    $t1, -12($s0)

L_24:
    li    $t1, 1000
    sw    $t1, -16($s0)

L_25:
    lw    $t1, -12($s0)
    li    $t2, 3
   bgt    $t1, $t2, L_27

L_26:
    j    L_30

L_27:
    lw    $t1, -12($s0)
    li    $t2, 3
   sub    $t1, $t1, $t2
    sw    $t1, -28($sp)

L_28:
    lw    $t1, -28($sp)
    sw    $t1, -12($s0)

L_29:
    j    L_25

L_30:
    li    $v0, 5
    syscall
    move $t0, $v0
    addi    $a0, $0, 0xA
    addi    $v0, $0, 0xB
    sw    $t0, -12($s0)

L_31:
    lw    $t9, -12($s0)
    li    $v0, 1
    move  $a0, $t9
    syscall
    addi    $a0, $0, 0xA
    addi    $v0, $0, 0xB
    syscall

L_32:
    lw    $t1, -16($s0)
    li    $t2, 0
   bgt    $t1, $t2, L_34

L_33:
    j    L_38

L_34:
    li    $t9, 10
    li    $v0, 1
    move  $a0, $t9
    syscall
    addi    $a0, $0, 0xA
    addi    $v0, $0, 0xB
    syscall

L_35:
    lw    $t1, -16($s0)
    li    $t2, 100
   sub    $t1, $t1, $t2
    sw    $t1, -32($sp)

L_36:
    lw    $t1, -32($sp)
    sw    $t1, -16($s0)

L_37:
    j    L_32

L_38:
    li    $v0, 10
    syscall

L_39:
    j    L_38
