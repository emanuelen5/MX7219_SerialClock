# MX7219_SerialClock
MAX7219 controller written to via UART

The AVR microcontroller accepts commands via UART which it then writes to the MAX7219 (MX) controller.

Format of UART commands:
- 1B Address
- 1B Data
- The ASCII character '\r' ends the command and starts the write to the MX
