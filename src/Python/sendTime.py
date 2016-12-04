# Program which sends the current time to a serially connected MAX7219 8-segment display

import time
import serial
import threading

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

h_last = ""
m_last = ""
sec_last = ""
displayBuffer = []

COM_N = input("COM port number: ")
# Timeout must be smaller than the thread interrupt value to avoid interrupt overflow
s = serial.Serial("COM"+COM_N, 9600, timeout=0.1)
s.flushOutput()

# Updates the display with a list of values
def MX_updateBuffer(digits):
    global displayBuffer
    if (len(digits) > 8):
        print("Only 8 digits are on the display!")
        print("Got " + len(digits))
        return
    dl = len(digits) - len(displayBuffer)
    # Only display as many digits as are in the buffer
    if (dl != 0):
        MX_write(s, MX_SCAN_LIMIT, len(digits)-1)
    if (dl > 0):
        displayBuffer.extend([""] * dl)
    elif (dl < 0):
        displayBuffer = displayBuffer[:dl]
    i = len(digits)-1;
    # Update each digit that has changed
    while (i >= 0):
        value = digits[len(digits) - 1 - i]
        if (displayBuffer[i] != value):
            digit = hex(int(MX_0, 16) + i)
            MX_write(s, digit, value)
            displayBuffer[i] = value
        i -= 1;
    displayBuffer = displayBuffer[:len(digits)] # Cut off extra entries (if buffer has shortened)

def MX_updateTime():
    threading.Timer(1.0, MX_updateTime).start()
    digits = [0]*6
    h,m,sec = time.localtime()[3:6]
    print("Time is: {0}:{1}:{2}".format(digitString(h),digitString(m),digitString(sec)))
    digits[0] = int(h/10)
    digits[1] = int(h%10)
    digits[2] = int(m/10)
    digits[3] = int(m%10)
    digits[4] = int(sec/10)
    digits[5] = int(sec%10)
    MX_updateBuffer(digits)

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
    tmp = "\0" # Used for dealing with if there is no response
    while (not resp.endswith("\n") and tmp != ""):
        tmp = serialPort.read().decode('UTF-8') # Convert to string without escape characters
        print_no_newline(tmp) # Print last character
        resp += tmp
    print("\"")
    if (tmp == ""):
        print("No response received within time limit - skipping parse of response!")

# Write data to a specific address on the MAX7219 via serial port
def MX_write(serialPort, address, data):
    serialWrite(serialPort, hex2dec(address));
    serialWrite(serialPort, int(data));
    serialWrite(serialPort, ord('\r')); # Convert character to integer

# Main method
if __name__ == "__main__":
    MX_write(s, MX_POWER, 1)
    MX_write(s, MX_SCAN_LIMIT, 5) # Only display 6 digits
    MX_write(s, MX_DECODE_MODE, hex2dec("0xFF")) # Decode all to numbers
    MX_write(s, MX_DISPLAY_TEST, 0)

    # Update the time on the display
    MX_updateTime()
