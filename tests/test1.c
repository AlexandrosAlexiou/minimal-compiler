#include <stdio.h>

int main(void)
{
	int a, k, T_1, T_2, T_3, T_4;
	L_1: a=100;
	L_2: T_1=a + 10;
	L_3: k=T_1;
	L_4: T_2=0 - 3;
	L_5: if(T_2< 5) goto L_17;
	L_6: goto L_7;
	L_7: if(5> 4) goto L_9;
	L_8: goto L_17;
	L_9: if(a< k) goto L_15;
	L_10: goto L_11;
	L_11: if(a> k) goto L_13;
	L_12: goto L_15;
	L_13: a=1;
	L_14: goto L_16;
	L_15: a=2;
	L_16: goto L_17;
	L_17: if(a> 1) goto L_19;
	L_18: goto L_23;
	L_19: if(a< 2) goto L_21;
	L_20: goto L_23;
	L_21: a=3;
	L_22: goto L_24;
	L_23: a=4;
	L_24: k=1000;
	L_25: if(a> 3) goto L_27;
	L_26: goto L_30;
	L_27: T_3=a - 3;
	L_28: a=T_3;
	L_29: goto L_25;
	L_30: scanf("%d", &a);
	L_31: printf("%d\n", a);
	L_32: if(k> 0) goto L_34;
	L_33: goto L_38;
	L_34: printf("%d\n", 10);
	L_35: T_4=k - 100;
	L_36: k=T_4;
	L_37: goto L_32;
	L_38: return 0;
	L_39:{}
}
