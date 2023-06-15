import serial
import time
import random
import math

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, AggOperations



# Handshake signal from Arduino
def arduino_ready():
    while True:
        #print("waiting")
        if ser.in_waiting:
            response = ser.readline().decode('utf-8').rstrip()
            if response == "Ready":
                return True
            else:
                print("\n Recived->>", response)


DELAY_LOWER_LIMIT = 120
DELAY_UPPER_LIMIT = 300
DELAY_STEP = 10

PWM_LOWER_LIMIT = 50
PWM_UPPER_LIMIT = 170
PWM_STEP = 10




def send_data(isAtHigh):
       
    #delay = randomMultiple(DELAY_LOWER_LIMIT, DELAY_UPPER_LIMIT, DELAY_STEP)
    delay = 0 # having a constant delay value makes the transitions between pwms more controllable
    pwmTarget = randomMultiple(PWM_LOWER_LIMIT, PWM_UPPER_LIMIT, PWM_STEP)

    
    ##TESTING
    
    # low = 15
    # high = 50

    # if(isAtHigh):
    #     pwmTarget = low
    # else:
    #     pwmTarget = high
    
    ##TESTING

    #delay = 150
    #pwm_max = 255

    # Send the values to Arduino
    ser.write(str(delay).encode('utf-8'))
    ser.write(b',')
    ser.write(str(pwmTarget).encode('utf-8'))
    ser.write(b'\n')

def randomMultiple(minimum, maximum, step):
    return random.randint(math.ceil(minimum / step ), math.floor(maximum / step)) * step



### openBCI Connection ###

DATA_ROWS = 15 
MIN_SLEEP = 4
MAX_SLEEP = 8
SLEEP_TIMER = max(MIN_SLEEP,  (DATA_ROWS % MAX_SLEEP)) #compute ideal sleep timer based on number of rows

def get_board_data():

    #openBCI board setup
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
    
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(SLEEP_TIMER)
    data = board.get_board_data(DATA_ROWS)
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
    
    downsampled_data = []

    # downsample data, it just aggregates data
    for count, channel in enumerate(eeg_channels):
        #print('Original data for channel %d:' % channel)
        #print(data[channel])
        if count == 0:
            downsampled_channel = DataFilter.perform_downsampling(data[channel], 3, AggOperations.MEDIAN.value)
        elif count == 1:
            downsampled_channel = DataFilter.perform_downsampling(data[channel], 2, AggOperations.MEAN.value)
        else:
            downsampled_channel = DataFilter.perform_downsampling(data[channel], 2, AggOperations.EACH.value)
        
        #print('Downsampled data for channel %d:' % channel)
        #print(downsampled_data)

        downsampled_data.append(downsampled_channel)

    return downsampled_data


def linear_interpolation(lower_limit, upper_limit, a):
    return (upper_limit * (1 - a)) + (lower_limit * a)


BCI_UPPER_LIMIT = 500
SELECTED_CHANNEL = 1

def process_bci_data(data):
 
    channel_num = SELECTED_CHANNEL
    channel = data[channel_num]

    abs_channel = [abs(ele) for ele in channel]
    channel_max_value =  abs_channel[len(abs_channel) - 1]

    print("\n channel: \n", channel, "\n")
    print("\n abs channel: \n", abs_channel, "\n")
    print("\n max value: ", channel_max_value, "\n")
    
    return (channel_max_value / BCI_UPPER_LIMIT) * PWM_UPPER_LIMIT


def get_pwm_value():
    #Collect data from bci headset

    downsampled_data = get_board_data()
    return process_bci_data(downsampled_data)




#print(get_pwm_value())


### openBCI Connection ###




# Set up the serial connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Change '/dev/ttyACM0' to the correct port for your Arduino
ser.reset_input_buffer()
ser.close()
ser.open()
time.sleep(5)

def main():
    ##TESTING
    isAtHigh = True
    ##TESTING

    while True:
        try:
            # Wait for Arduino confirmation
            if arduino_ready():
                print("Arduino Ready")
                send_data(isAtHigh)
                isAtHigh = not(isAtHigh)
            else:
                print("Waiting")

        except KeyboardInterrupt:
            break

    # Close the serial connection
    ser.close()


main()
