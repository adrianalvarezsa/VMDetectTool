#include<stdio.h>

int main(){
	int cpuid;
	__asm__("xor %eax, %eax\n\t");
	__asm__("mov $0x40000000, %eax\n\t");
	__asm__("cpuid\n\t");
	__asm__("cmp $0x4D566572, %ecx\n\t");
	__asm__("jne NopInstr\n\t");
	__asm__("cmp $0x65726177,%edx\n\t");
	__asm__("jne NopInstr\n\t");
	__asm__("mov $0x1, %0\n\t":"=r" (cpuid));
	__asm__("NopInstr:\n\t");
	__asm__("nop\n\t");
	
	if (cpuid == 1){
		printf("vmware\n");
	} else {
		printf("no\n");
	}
}
