# Program which sends the current time to a serially connected MAX7219 8-segment display

import time
import serial
import threading

h_last = ""
m_last = ""
sec_last = ""

def MX_updateTime():
    threading.Timer(1.0, MX_updateTime).start()
    global h_last
    global m_last
    global sec_last
    h,m,sec = time.localtime()[3:6]
    print("Time is: {0}:{1}:{2}".format(digitString(h),digitString(m),digitString(sec)))
    if (h_last != h):
        MX_write(s, MX_5, h/10)
        MX_write(s, MX_4, h%10)
    if (m_last != m):
        MX_write(s, MX_3, m/10)
        MX_write(s, MX_2, m%10)
    if (sec_last != sec):
        MX_write(s, MX_1, sec/10)
        MX_write(s, MX_0, sec%10)
    h_last = h
    m_last = m
    sec_last = sec

# Turn a digit into a String of at least two characters
def digitString(number):
    if number < 10:
        return "0" + str(number)
    else:
        return str(number)

# Get the current Hour, Minute and Second in separate Strings
def getTimeString():
    h,m,s = time.localtime()[3:6]
    h = digitString(h)
    m = digitString(m)
    s = digitString(s)
    return h,m,s

# Turn a decimal number into binary
def dec2bin(dec):
    return [int(x) for x in bin(dec)[2:]]

# Turn a hexadecimal number into decimal
def hex2dec(dec):
    return int(dec, 16)

# Print a string to console without a newline
def print_no_newline(string):
    print(string, end="") 

# Write to serial port and accept data in return
def serialWrite(serialPort, data):
    serialPort.write([data])
    print("Sent: " + str(data))
    print_no_newline("Response: \"")
    resp = ""
    while (not resp.endswith("\n")):
        resp += serialPort.read().decode('UTF-8') # Must convert to string without escape characters
        print_no_newline(resp[-1:]) # Print last character
    print_no_newline("\"")

# Write data to a specific address on the MAX7219 via serial port
def MX_write(serialPort, address, data):
    serialWrite(serialPort, hex2dec(address));
    serialWrite(serialPort, int(data));
    serialWrite(serialPort, ord('\r')); # Convert character to integer

# Main method
if __name__ == "__main__":
    global s

    # Write addresses
    MX_0            = "0x01" # Digit 0
    MX_1            = "0x02" # Digit 1
    MX_2            = "0x03" # Digit 2
    MX_3            = "0x04" # Digit 3
    MX_4            = "0x05" # Digit 4
    MX_5            = "0x06" # Digit 5
    MX_6            = "0x07" # Digit 6
    MX_7            = "0x08" # Digit 7
    MX_DECODE_MODE  = "0x09" # Set decode mode for each digit
    MX_INTENSITY    = "0x0A" # Set intensity
    MX_SCAN_LIMIT   = "0x0B" # Set number of digits to display (affects the intensity as well)
    MX_POWER        = "0x0C" # On/off
    MX_DISPLAY_TEST = "0x0F" # Turn on all LEDs

    COM_N = input("COM port number: ")
    s = serial.Serial("COM"+COM_N, 9600, timeout=1)
    s.flushOutput()
    MX_write(s, MX_POWER, 1)
    MX_write(s, MX_SCAN_LIMIT, 5) # Only display 6 digits
    MX_write(s, MX_DECODE_MODE, hex2dec("0xFF")) # Decode all

    # Update the time on the display
    MX_updateTime()
