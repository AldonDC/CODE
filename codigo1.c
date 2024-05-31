#include "stm32f1xx.h" // Asegúrate de incluir el archivo de cabecera correcto para STM32F103

void configure_PB0_PB4_output(void) {
    // Habilitar el reloj para el puerto B
    RCC->APB2ENR |= RCC_APB2ENR_IOPBEN;

    // Configurar PB0 como salida push-pull de 50 MHz
    GPIOB->CRL &= ~(GPIO_CRL_MODE0 | GPIO_CRL_CNF0); // Limpiar los bits de configuración para PB0
    GPIOB->CRL |= (GPIO_CRL_MODE0_1 | GPIO_CRL_MODE0_0); // Configurar como salida de 50 MHz

    // Configurar PB4 de la misma manera, se necesita acceder a CRH ya que es un pin de mayor número
    GPIOB->CRL &= ~(GPIO_CRH_MODE4 | GPIO_CRH_CNF4); // Limpiar los bits de configuración para PB4
    GPIOB->CRL |= (GPIO_CRH_MODE4_1 | GPIO_CRH_MODE4_0); // Configurar como salida de 50 MHz

    // Establecer PB0 y PB4 a alto nivel
    GPIOB->BSRR = GPIO_BSRR_BS0 | GPIO_BSRR_BS4;
}

int main(void) {
    configure_PB0_PB4_output();
    
    // El resto de tu código principal va aquí

    while(1) {
        // Bucle infinito
    }
}
