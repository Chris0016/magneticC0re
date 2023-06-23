import openbci_stream as stream

def handle_sample(sample):
    # Process the received sample data
    print(sample.channels_data)

def print_data(num_rows):
    # Set up the OpenBCI board
    board = stream.OpenBCIBoard(port='/dev/ttyUSB0')  # Update the port with your Cyton board's serial port

    # Attach the sample handler
    board.attach(handle_sample)

    # Start streaming data
    board.start_streaming()

    # Keep track of the number of rows printed
    rows_printed = 0

    # Print data until the desired number of rows is reached
    while rows_printed < num_rows:
        pass

        # Increment the row count
        rows_printed += 1

    # Stop streaming data
    board.stop_streaming()

def main():
    # Print 100 rows of data
    print_data(100)

if __name__ == '__main__':
    main()
