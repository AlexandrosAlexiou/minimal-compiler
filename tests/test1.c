#include <stdio.h>

int main(void)
{
	int a, k, T_1, T_2, T_3;
	L_1: T_1=0 - 3;
	L_2: if(T_1< 5) goto L_6;
	L_3: goto L_4;
	L_4: if(5> 4) goto L_6;
	L_5: goto L_8;
	L_6: a=1;
	L_7: goto L_9;
	L_8: a=2;
	L_9: if(a> 1) goto L_11;
	L_10: goto L_15;
	L_11: if(a< 2) goto L_13;
	L_12: goto L_15;
	L_13: a=3;
	L_14: goto L_16;
	L_15: a=4;
	L_16: k=10000;
	L_17: if(a> 3) goto L_19;
	L_18: goto L_22;
	L_19: T_2=a - 3;
	L_20: a=T_2;
	L_21: goto L_17;
	L_22: if(k> 0) goto L_24;
	L_23: goto L_28;
	L_24: printf("%d\n", 10);
	L_25: T_3=k - 100;
	L_26: k=T_3;
	L_27: goto L_22;
	L_28: return 0;
	L_29:{}
}
