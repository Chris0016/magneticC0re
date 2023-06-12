import serial
import time
import random

# Set up the serial connection
ser = serial.Serial('/dev/tty0', 9600)  # Change '/dev/ttyACM0' to the correct port for your Arduino
ser.flushInput()

# Handshake signal from Arduino
def arduino_ready():
    while True:
        if ser.in_waiting:
            response = ser.readline().decode().strip()
            if response == "Ready":
                return True

# Send two random values to Arduino
while True:
    try:
        # Generate two random numbers from 0 to 255
        value1 = random.randint(0, 255)
        value2 = random.randint(0, 255)

        # Send the values to Arduino
        ser.write(str(value1).encode())
        ser.write(b',')
        ser.write(str(value2).encode())
        ser.write(b'\n')

        # Wait for Arduino confirmation
        if arduino_ready():
            print("Arduino confirmed:", value1, value2)
        else:
            print("Arduino failed to confirm")

    except KeyboardInterrupt:
        break

# Close the serial connection
ser.close()

