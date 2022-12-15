#include "Adc.h"
#include "Uart.h"
#include <stdio.h>

int main() {
	UART0_Init(115200);
	ADC0_Init();
	RGBLed_Init();
	
	for(;;) {
	}
	
}
