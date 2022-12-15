#include "MKL25Z4.h"

void ADC0_Init(void);
int ADC0_Calibrate(void);
uint16_t ADC0_Read(void);
void ADC0_IRQHandler(void);
void show_light_value(void);
void RGBLed_Init(void);
