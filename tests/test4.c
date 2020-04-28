#include <stdio.h>

int main(void)
{
	int a, c, b, T_1, T_2;
	L_1: a=50;
	L_2: b=6;
	L_3: c=70;
	L_4: if(c> 70) goto L_6;
	L_5: goto L_9;
	L_6: T_1=c - 40;
	L_7: c=T_1;
	L_8: goto L_4;
	L_9: if(a> 100) goto L_11;
	L_10: goto L_13;
	L_11: b=2;
	L_12: goto L_4;
	L_13: if(a> 200) goto L_15;
	L_14: goto L_17;
	L_15: a=3;
	L_16: goto L_4;
	L_17: if(a> 30) goto L_19;
	L_18: goto L_22;
	L_19: T_2=a - 5;
	L_20: a=T_2;
	L_21: goto L_4;
	L_22: printf("%d\n", a);
	L_23: return 0;
	L_24:{}
}
