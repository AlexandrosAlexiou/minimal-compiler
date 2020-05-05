
L_1:   #1: -, 0, 3, T_1


L_2:   #2: <, T_1, 5, 6


L_3:   #3: jump, _, _, 4

    j    L_4

L_4:   #4: >, 5, 4, 6


L_5:   #5: jump, _, _, 8

    j    L_8

L_6:   #6: :=, 3, _, a


L_7:   #7: jump, _, _, 9

    j    L_9

L_8:   #8: :=, 4, _, a


L_9:   #9: >, 1000, 300, 11


L_10:   #10: jump, _, _, 15

    j    L_15

L_11:   #11: <, 10, 100, 13


L_12:   #12: jump, _, _, 15

    j    L_15

L_13:   #13: :=, 3, _, a


L_14:   #14: jump, _, _, 16

    j    L_16

L_15:   #15: :=, 555, _, a


L_16:   #16: >, 5, 3, 18


L_17:   #17: jump, _, _, 21

    j    L_21

L_18:   #18: -, a, 3, T_2


L_19:   #19: :=, T_2, _, a


L_20:   #20: jump, _, _, 16

    j    L_16

L_21:   #21: >, k, 30, 23


L_22:   #22: jump, _, _, 26

    j    L_26

L_23:   #23: -, a, 100, T_3


L_24:   #24: :=, T_3, _, a


L_25:   #25: jump, _, _, 21

    j    L_21

L_26:   #26: retv, m, _, _


L_27:   #27: end_block, randomfunc, _, _


L_29:   #29: par, u5, CV, _


L_30:   #30: par, T_4, RET, _


L_31:   #31: call, randomfunc, _, _


L_32:   #32: par, T_4, CV, _


L_33:   #33: par, T_5, RET, _


L_34:   #34: call, randomfunc, _, _


L_35:   #35: :=, T_5, _, kkk


L_36:   #36: retv, kkk, _, _


L_37:   #37: end_block, myfunc, _, _


L_39:   #39: out, u5, _, _


L_40:   #40: par, u5, CV, _


L_41:   #41: par, u5, CV, _


L_42:   #42: par, T_6, RET, _


L_43:   #43: call, myfunc, _, _


L_44:   #44: par, T_6, CV, _


L_45:   #45: par, u5, CV, _


L_46:   #46: par, u5, CV, _


L_47:   #47: par, T_7, RET, _


L_48:   #48: call, myfunc, _, _


L_49:   #49: par, T_7, CV, _


L_50:   #50: par, T_8, RET, _


L_51:   #51: call, myfunc, _, _


L_52:   #52: :=, T_8, _, u5


L_53:   #53: halt, _, _, _


L_54:   #54: end_block, test3, _, _

