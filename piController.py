import serial
import time
import random
import math
import statistics

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, AggOperations

'''
CYTON BOARD:

num eeg(emg,…) channels: 8

num acceleration channels: 3

sampling rate: 250

communication: serial port

signal gain: 24


'''

##Change these values depending on channel, some channels only go up to 100
BCI_UPPER_LIMIT = 55_000
BCI_LOWER_LIMIT = 45_000 #big negative numbers are considered no activity
SELECTED_CHANNEL = 8

DATA_ROWS = 80

#TO BE DELETED?
DELAY_LOWER_LIMIT = 150
DELAY_UPPER_LIMIT = 100
DELAY_STEP = 10
#TO BE DELETED? variable delay creates a 'lag' between input and pwm shown. 

PWM_LOWER_LIMIT = 20.0
PWM_UPPER_LIMIT = 40.0
PWM_STEP = 10 # TO BE DELETED?


#MIN_SLEEP = 2
#MAX_SLEEP = 4
#SLEEP_TIMER = max(MIN_SLEEP,  (DATA_ROWS % MAX_SLEEP)) #compute ideal sleep timer based on number of rows

SLEEP_TIMER = 3

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



def send_data(pwmTarget):
       
    #delay = randomMultiple(DELAY_LOWER_LIMIT, DELAY_UPPER_LIMIT, DELAY_STEP)
    delay = 0 # having a constant delay value makes the transitions between pwms more controllable
    ##pwmTarget = randomMultiple(PWM_LOWER_LIMIT, PWM_UPPER_LIMIT, PWM_STEP)
    ##pwmTarget = pwmTarget
    
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

#openBCI board setup
BoardShim.enable_dev_board_logger()

# use synthetic board for demo
# params = BrainFlowInputParams()
# board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)

#REAL BOARD
params = BrainFlowInputParams()
params.serial_port = "/dev/ttyUSB0"
board = BoardShim(BoardIds.CYTON_BOARD, params)

def get_board_data():

    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(SLEEP_TIMER)
    data = board.get_board_data(DATA_ROWS)
    board.stop_stream()
    board.release_session()
    

    
    eeg_channels = BoardShim.get_eeg_channels(BoardIds.CYTON_BOARD.value)
    
    downsampled_data = []

    # downsample data, it just aggregates data
    for count, channel in enumerate(eeg_channels):
        print('Original data for channel %d:' % channel)
        print(data[channel])
        # if count == 0:
        #     downsampled_channel = DataFilter.perform_downsampling(data[channel], 3, AggOperations.MEDIAN.value)
        # elif count == 1:
        #     downsampled_channel = DataFilter.perform_downsampling(data[channel], 2, AggOperations.MEAN.value)
        # else:
        #     downsampled_channel = DataFilter.perform_downsampling(data[channel], 2, AggOperations.EACH.value)
        
        #print('Downsampled data for channel %d:' % channel)
        #print(downsampled_data)

        # downsampled_data.append(downsampled_channel)

    return data[SELECTED_CHANNEL]



#Takes a channel with a number of eeg values and converts it to a 
#corresponding value in the range of PWM_LOWER_LIMIT(set to ~20) to PWM_UPPER_LIMIT(set to ~40)

def process_bci_data(channel):
    
    abs_channel = [abs(ele) for ele in channel]
    abs_channel.sort()
    max_val = abs_channel[len(abs_channel) - 1]
    mean =  statistics.mean(channel)  #always a value between 0 and 1

    if (mean < 0 ):
        return PWM_LOWER_LIMIT


    diff = (BCI_UPPER_LIMIT - BCI_LOWER_LIMIT)
    x = mean - BCI_LOWER_LIMIT

    x_normalized = (x/diff)

    print("\n channel: \n", channel, "\n")
    print("\n abs channel: \n", abs_channel, "\n")
    print("\n max value: ", max_val, "\n")
    print("\n mean: ", mean, "\n")
    print("\n x_nomalized:", x_normalized, "\n")

    
    return (x_normalized *  (PWM_UPPER_LIMIT - PWM_LOWER_LIMIT) ) + PWM_LOWER_LIMIT 

def get_pwm_value():
    #Collect data from bci headset

    downsampled_data = get_board_data()
    return process_bci_data(downsampled_data)

#print(get_pwm_value())

### openBCI Connection ###


# Set up the serial connection
# ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Change '/dev/ttyACM0' to the correct port for your Arduino
# ser.reset_input_buffer()
# ser.close()
# ser.open()
# time.sleep(5)

def main():
   
    # while True:
    #     try:
    #         # Wait for Arduino confirmation
    #         if arduino_ready():
    #             print("Arduino Ready")
    #             send_data(get_pwm_value())
    #         else:
    #             print("Waiting")

    #     except KeyboardInterrupt:
    #         break

    # Close the serial connection
    #ser.close()

    iteration = 1

    while True: 
        try:
            print("\n\n--------------- Iternation : ", iteration,"---------------\n\n")
            pwm = get_pwm_value()
            print("pwm: ", pwm)
            print("\n\nsleeping...\n\n")
            time.sleep(2)
            iteration = iteration + 1
        except KeyboardInterrupt:
            break


main()
