# MX7219_SerialClock
MAX7219 controller written to via UART

The AVR microcontroller accepts commands via UART which it then writes to the MAX7219 (MX) controller.
The AVR waits for three bytes via UART, sends an acknowledge for each one and then sends the read bytes (address and data) over SPI to the MX controller.

The order of the bytes which are sent to the AVR via UART:

1. Address (see MX datasheet for figuring out what each address stands for)
2. Data (see MX datasheet...)
3. The ASCII character '\r' (carriage return) ends the command and starts the write to the MX

The AVR will ignore the command if the third byte is not an '\r'. It will keep blocking until it reads a '\r' - which means it is hopefully synchronized with the sender again.
Desynchronization can happen if you manually send commands over UART via a serial program.
