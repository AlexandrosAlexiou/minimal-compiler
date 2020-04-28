#include <stdio.h>

int main(void)
{
	int k, a, T_1, T_2, T_3, T_4, T_5, T_6, T_7, T_8, T_9, T_10, T_11, T_12, T_13, T_14, T_15, T_16;
	L_1: if(1> 2) goto L_3;
	L_2: goto L_6;
	L_3: T_1=a + 3;
	L_4: a=T_1;
	L_5: goto L_1;
	L_6: T_2=a + 4;
	L_7: a=T_2;
	L_8: T_3=a + 5;
	L_9: a=T_3;
	L_10: if(6> 7) goto L_12;
	L_11: goto L_15;
	L_12: T_4=a + 8;
	L_13: a=T_4;
	L_14: goto L_10;
	L_15: T_5=a + 9;
	L_16: a=T_5;
	L_17: T_6=0 - 3;
	L_18: T_7=T_6 + 4;
	L_19: T_8=0 - 3;
	L_20: T_9=T_8 + 10;
	L_21: T_10=T_7 * T_9;
	L_22: T_11=0 - 3;
	L_23: T_12=T_11 + 4;
	L_24: T_13=0 - 3;
	L_25: T_14=T_13 + 10;
	L_26: T_15=T_12 * T_14;
	L_27: T_16=T_10 + T_15;
	L_28: printf("%d\n", T_16);
	L_29: printf("%d\n", 1000);
	L_30: return 0;
	L_31:{}
}
