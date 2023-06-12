import serial
import time
import noise

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

# Send Perlin noise values to Arduino
while True:
    try:
        # Generate Perlin noise value
        value = int(noise.pnoise1(time.time()) * 102.0 + 153.0)
        # Ensure value is within the range of 50-255
        value = max(50, min(value, 255))

        # Send the value to Arduino
        ser.write(str(value).encode())
        ser.write(b'\n')

        # Wait for Arduino confirmation
        if arduino_ready():
            print("Arduino confirmed:", value)
        else:
            print("Arduino failed to confirm")

    except KeyboardInterrupt:
        break

# Close the serial connection
ser.close()
