import serial
import time
import random

# Set up the serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change '/dev/ttyACM0' to the correct port for your Arduino
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
 	# Generate Perlin noise value
        delay = int(noise.pnoise1(time.time()) * 102.0 + 153.0)
        # Ensure value is within the range of 50-255
        delay = max(50, min(value, 255))        


	# Generate two random numbers from 0 to 255
        delay = random.randint(0, 255)
        max_pwm = random.randint(0, 255)

        # Send the values to Arduino
        ser.write(str(delay).encode())
        ser.write(b',')
        ser.write(str(max_pwm).encode())
        ser.write(b'\n')

        # Wait for Arduino confirmation
        if arduino_ready():
            print("Arduino confirmed:", delay, max_pwm)
        else:
            print("Arduino failed to confirm")

    except KeyboardInterrupt:
        break

# Close the serial connection
ser.close()

