from __future__        import annotations
from ssd1306           import SSD1306
from max30102          import MAX30102, calc_hr_and_spo2
import typing
import threading
import time


# Initialize the DATA global variable.
DATA: typing.Dict[str, typing.Optional[int]] = {
    "heart_rate" : None,
    "O2_rate"    : None
}

# Initialize the MESSAGE_SENT_TIMER global variable.
MESSAGE_SENT_TIMER: int = 0


def run_message_sent_timer() -> None:
    """Run the message sent time routine, decrementing the global variable MESSAGE_SENT_TIMER by 1 every seconds."""
    
    # Set the global variable MESSAGE_SENT_TIMER writable.
    global MESSAGE_SENT_TIMER
    
    # Run the loop until the main thread stops.
    while True:
        # If the global variable MESSAGE_SENT_TIMER is not null,
        # decrement it by 1 and block the loop for 1 seconds.
        if MESSAGE_SENT_TIMER:
            MESSAGE_SENT_TIMER -= 1
            time.sleep(1)


def run_ssd1306(ssd1306: SSD1306) -> None:
    """
    Run the ssd1306 device routine, writing periodically the
    content of the DATA global variable on the SSD1306 screen.
    
    :param SSD1306 ssd1306: The instance of the ssd1306 device to write.
    """
    
    # Run the loop until the main thread stops.
    while True:
        # While MESSAGE_SENT_TIMER is not null, block the loop for 1 seconds.
        while MESSAGE_SENT_TIMER:
            time.sleep(1)
        
        # If the ssd1306 device is busy, block the loop for 1 seconds and continue.
        if ssd1306.is_busy:
            time.sleep(1)
            continue
        
        # Set the ssd1306 as busy.
        ssd1306.is_busy = True

        # Clear the content of the ssd1306 device.
        ssd1306.clear()
        
        # Retrieve from DATA and write the different metrics to the ssd1306 device.
        ssd1306.write(f"""{DATA["heart_rate"]} BPM""", 0, 0)
        ssd1306.write(f"""{DATA["O2_rate"]} 02%""", 0, 15)
        
        # Set the ssd1306 as not busy anymore.
        ssd1306.is_busy = False
        
        # Sleep the loop for 5 seconds.
        time.sleep(5)


def run_max30102() -> None:
    """Run the max30102 sensor routine, retrieving the sensor's data and writing them to the screen."""
    
    # Make the DATA global variable writable.
    global DATA

    # Run the loop until the main thread stops.
    while True:
        # Add a try/except mechanism to handle measurement fails.
        try:
            # Initialize a MAX30102 sensor instance.
            sensor: MAX30102 = MAX30102()
            
            # Declare the variables used while iterating.
            heart_rate: int
            heart_rate_measured: bool
            o2_rate: float
            o2_rate_measured: bool

            # Run the loop until the main thread stops.
            while True:
                # Read the data using the read_sequential and hrcalc.calc_hr_and_spo2 methods.
                heart_rate, heart_rate_measured, o2_rate, o2_rate_measured = calc_hr_and_spo2(*sensor.read_sequential())
                
                # If both data have been red correctly, update the DATA global variable.
                if heart_rate_measured and o2_rate_measured and heart_rate != -999 and o2_rate != -999:
                    DATA["heart_rate"] = heart_rate
                    DATA["O2_rate"]    = int(o2_rate)
        except OSError:
            print("Court-circuit pour le capteur MAX30102")
            time.sleep(5)


def main() -> None:
    """Main function."""
    
    # Set the global variable MESSAGE_SENT_TIMER writable.
    global MESSAGE_SENT_TIMER
    
    # Try to initialize the screen infinitely until it works.
    while True:
        try:
            # Initialize the ssd1306 device.
            ssd1306: SSD1306 = SSD1306()
            
            # Break the infinite loop.
            break
        except Exception as e:
            # Print the obtained exception.
            print(e)
        
            # Retry in 3 seconds.
            print("Retry in 3 seconds...")
            time.sleep(3)

    # Run the different threads.
    message_sent_timer_thread = threading.Thread(target = run_message_sent_timer, daemon=True,)
    message_sent_timer_thread.start()
    max30102_thread = threading.Thread(target = run_max30102, daemon=True)
    max30102_thread.start()
    ssd30102_thread = threading.Thread(target = run_ssd1306, daemon=True, args=(ssd1306,))
    ssd30102_thread.start()
    
    # Loop infinitely waiting for text to write to the display.
    while True:
        # Retrieve the text input from the suer.
        text: str = input("Write the text to write on the display: ")
        
        # Format the text to fit within the right number of lines.
        texts: typing.List[str] = []
        tmp: str
        while True:
            if len(text) <= 20:
                texts.append(text.strip())
                break
            tmp = text[:20]
            if not tmp.endswith(' '):
                if ' ' not in tmp:
                    text = text[20:]
                    texts.append(tmp.strip())
                    continue
                tmp = ' '.join(tmp.split(' ')[:-1])
                text = text[len(tmp):]
                texts.append(tmp.strip())
            else:
                text = text[len(tmp):]
                texts.append(tmp.strip().strip())
        
        # Initialize a lineno variable.
        lineno: int = 0
        
        # If the ssd1306 device is busy, wait for it to be not busy anymore.
        while ssd1306.is_busy:
            pass
        
        # Set the ssd1306 as busy.
        ssd1306.is_busy = True
        
        # Clear the screen.
        ssd1306.clear()
        
        # Write the obtained texts.
        for text_ in texts:
            if lineno == 4:
                # Wait 5 seconds for the display's content to be read.
                time.sleep(5)

                # Clear the display.
                ssd1306.clear()
                lineno = 0
            # Write the text_ content and increment the lineno variable.
            ssd1306.write(text_.strip(), 0, 15*lineno)
            lineno += 1
        
        # Set the global variable MESSAGE_SENT_TIMER to 5.
        MESSAGE_SENT_TIMER = 5
        
        # Set the ssd1306 as not busy anymore.
        ssd1306.is_busy = False


if __name__ == "__main__":
    main()
