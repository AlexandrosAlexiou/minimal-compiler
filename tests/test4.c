#include <stdio.h>

int main(void)
{
	int a, c, b, T_1, T_2, T_3, T_4;
	L_1: a=50;
	L_2: b=6;
	L_3: c=69;
	L_4: if(c< 70) goto L_6;
	L_5: goto L_13;
	L_6: T_1=0 - 300;
	L_7: if(c> T_1) goto L_9;
	L_8: goto L_13;
	L_9: T_2=c - 10;
	L_10: c=T_2;
	L_11: printf("%d\n", c);
	L_12: goto L_4;
	L_13: if(b> 4) goto L_15;
	L_14: goto L_18;
	L_15: T_3=b - 1;
	L_16: b=T_3;
	L_17: goto L_4;
	L_18: if(a> 30) goto L_20;
	L_19: goto L_23;
	L_20: T_4=a - 5;
	L_21: a=T_4;
	L_22: goto L_4;
	L_23: printf("%d\n", a);
	L_24: printf("%d\n", b);
	L_25: printf("%d\n", c);
	L_26: return 0;
	L_27:{}
}
