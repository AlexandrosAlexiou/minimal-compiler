#include <stdio.h>

int main(void)
{
	int a, c, b, T_1;
	L_1: a=5;
	L_2: a=6;
	L_3: a=7;
	L_4: if(6> 6) goto L_6;
	L_5: goto L_8;
	L_6: a=8;
	L_7: goto L_4;
	L_8: if(a> 100) goto L_10;
	L_9: goto L_12;
	L_10: b=9;
	L_11: goto L_4;
	L_12: if(200> 200) goto L_14;
	L_13: goto L_16;
	L_14: a=10;
	L_15: goto L_4;
	L_16: if(300> 300) goto L_18;
	L_17: goto L_20;
	L_18: a=11;
	L_19: goto L_4;
	L_20: a=5000;
	L_21: a=1000;
	L_22: T_1=b + 5;
	L_23: a=T_1;
	L_24: return 0;
	L_25:{}
}
