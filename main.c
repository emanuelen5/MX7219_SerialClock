/*
 * MAX7219SerialClock.c
 *
 * Created: 2015-11-08 23:02:15
 * Author : Emaus
 */ 

#define F_CPU 1000000UL
#include <avr/io.h>
#include "USART.h"
#include "bitops.h"
#include "7segFont.h"
#include <util/delay.h>

#define DDR_SPI  DDRB
#define PORT_SPI PORTB
#define DD_SCK   PB5   // Slave clock
#define DD_MISO  PB4   // Master in, slave out
#define DD_MOSI  PB3   // Master out, slave in
#define DD_SS    PB2   // Slave select

#define MX_LOAD1 PORT_SPI |= BV(DD_SS)
#define MX_LOAD0 PORT_SPI &= ~BV(DD_SS)

#define MX_ON    0x01
#define MX_OFF   0x00

#define PDBG   PB0
#define DBG    PORTB ^= BV(PDBG); \
			   _delay_ms(500);

/************************************************************************/
/* MAX7219-MAX7221 addresses                                            */
/************************************************************************/
enum MX_ADDR{
	MX_NOOP         = 0x00,
	MX_DIGIT0       = 0x01,
	MX_DIGIT1       = 0x02,
	MX_DIGIT2       = 0x03,
	MX_DIGIT3       = 0x04,
	MX_DIGIT4       = 0x05,
	MX_DIGIT5       = 0x06,
	MX_DIGIT6       = 0x07,
	MX_DIGIT7       = 0x08,
	MX_DECODE       = 0x09,
	MX_INTENSITY    = 0x0A,
	MX_SCAN_LIMIT   = 0x0B,
	MX_POWER        = 0x0C,
	MX_DISPLAY_TEST = 0x0F
};

/************************************************************************/
/* Initializes SPI in master mode with clock/64                         */
/************************************************************************/
void initSPI(void) {
	DDR_SPI |= BV(DD_MOSI) | BV(DD_SCK) | BV(DD_SS); // Enable output on MISO, SCK and SS pins
	SPCR |= BV(SPE) | BV(MSTR); // Enable SPI | Master device (Clock/4)
	SPSR |= BV(SPI2X); // Double clock speed => Clock/2
	SPDR = 0x00; // <-- Only way to clear the SPDR interrupt vector without an interrupt routine?
	MX_LOAD1;
}

/************************************************************************/
/* Sends data with SPI. BLocking until last data transfer is complete.  */
/************************************************************************/
void SPI_send(const uint8_t DATA) {
	while (!bit_is_set(SPSR, SPIF));
	SPDR = DATA;
}

/************************************************************************/
/*                                                                      */
/************************************************************************/
void MX(const enum MX_ADDR ADDR, const uint8_t DATA) {
	MX_LOAD0;
	SPI_send(ADDR);
	SPI_send(DATA);
	while (!bit_is_set(SPSR, SPIF));
	MX_LOAD1;
}

int main(void)
{
	DDRB |= BV(PDBG); // Set debug port to output
	initUSART();
	initSPI();

	MX(MX_POWER, MX_ON);
	MX(MX_SCAN_LIMIT, 0x07);
	MX(MX_DISPLAY_TEST, MX_OFF);
	
	 // Show a message
	 MX(MX_DECODE, 0);
	 MX(MX_DIGIT7, ASCII_2_7Seg(' '));
	 MX(MX_DIGIT6, ASCII_2_7Seg(' '));
	 MX(MX_DIGIT5, ASCII_2_7Seg(' '));
	 MX(MX_DIGIT4, ASCII_2_7Seg('R'));
	 MX(MX_DIGIT3, ASCII_2_7Seg('E'));
	 MX(MX_DIGIT2, ASCII_2_7Seg('A'));
	 MX(MX_DIGIT1, ASCII_2_7Seg('D'));
	 MX(MX_DIGIT0, ASCII_2_7Seg('Y'));
	 MX(MX_DISPLAY_TEST, MX_OFF);
	 _delay_ms(1500);
	
	 // Clear display
	 MX(MX_DIGIT0, 0);
	 MX(MX_DIGIT1, 0);
	 MX(MX_DIGIT2, 0);
	 MX(MX_DIGIT3, 0);
	 MX(MX_DIGIT4, 0);
	 MX(MX_DIGIT5, 0);
	 MX(MX_DIGIT6, 0);
	 MX(MX_DIGIT7, 0);

	char address, data;
	while (1)
	{
		address = receiveByte();
		printString("Address acknowledged\r\n");
		
		data = receiveByte();
		printString("Data acknowledged\r\n");
		
		if (receiveByte() == '\r') {
			printString("CR Acknowledged\r\n");
			MX(address, data);
		} else {
			printString("Error: Expected CR - waiting until next CR to synchronize\r\n");
			while (receiveByte() != '\r')
				printString("Waiting for \\r to resynchronize\r\n");
		}
	}
}


