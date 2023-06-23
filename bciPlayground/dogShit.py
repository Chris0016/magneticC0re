import time
import statistics

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, AggOperations

BoardShim.enable_dev_board_logger()

# use synthetic board for demo
# params = BrainFlowInputParams()
# board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
rows = 60

#REAL BOARD
params = BrainFlowInputParams()
params.serial_port = "/dev/ttyUSB0"
board = BoardShim(BoardIds.CYTON_BOARD, params)

def run():

    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(2)
    data = board.get_board_data(rows)
   
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(BoardIds.CYTON_BOARD.value)

   
   # demo for downsampling, it just aggregates data
    for count, channel in enumerate(eeg_channels):
        print('Original data for channel %d:' % channel)
        print('channel :', channel, "\n")
        print(data[channel])
        print('\nMax: ', max(data[channel]), "\n")
        print('\nMin: ', min(data[channel]), "\n")
        print('\nMean: ', statistics.mean(data[channel]) )
        

        # if count == 0:
        #     downsampled_data = DataFilter.perform_downsampling(data[channel], 3, AggOperations.MEDIAN.value)
        # elif count == 1:
        #     downsampled_data = DataFilter.perform_downsampling(data[channel], 2, AggOperations.MEAN.value)
        # else:
        #     downsampled_data = DataFilter.perform_downsampling(data[channel], 2, AggOperations.EACH.value)
        #print('Downsampled data for channel %d:' % channel)
        #print(downsampled_data)


  

# if __name__ == "__main__":
#     main()

iteration = 1
while True: 
        try:
            print("\n\n--------------- Iternation : ", iteration,"---------------\n\n")
            run()
            print("\n\nsleeping...\n\n")
            time.sleep(2)
            iteration = iteration + 1
        except KeyboardInterrupt:
            break