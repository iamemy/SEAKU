from __future__  import annotations
from button      import wait_for_button_pressed
from max30102    import MAX30102, calc_hr_and_spo2
from sd18b20     import get_sd18b20_temperature
from bmp280      import BMP280
from ws2812b     import WS2812B
from ssd1306     import SSD1306
from gui         import Dashboard, MESSAGE_SENT_TIMER
import typing
import _rpi_ws281x   as ws
import threading
import time


# Initialize the DATA global variable.
DATA: typing.Dict[str, typing.Optional[int]] = {
    "heart_rate"  : None,
    "O2_rate"     : None,
    "temperature" : None,
    "pressure"    : None,
    "altitude"    : None
}

# Initialize the APP global variable.
APP: typing.Optional[Dashboard] = None


def print_retry(device: str, s: int=3) -> None:
    """Print the Retry message."""
    print(f"Failed to initialize the {device}.")
    print("Retry in 3 seconds", end="")
    for _ in range(s):
        time.sleep(1)
        print('.', end="")
    print()


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


def run_max30102() -> None:
    """Run the max30102 sensor routine, retrieving the sensor's data and writing them to the screen."""
    
    # Make the DATA global variable writable.
    global DATA

    # Run the loop until the main thread stops.
    while True:
        # Add a try/except mechanism to handle measurement fails.
        try:
            # Initialize a MAX30102 sensor instance.
            max30102: MAX30102 = MAX30102()
            
            # Declare the variables used while iterating.
            heart_rate: int
            heart_rate_measured: bool
            o2_rate: float
            o2_rate_measured: bool

            # Run the loop until the main thread stops.
            while True:
                # Read the data using the read_sequential and hrcalc.calc_hr_and_spo2 methods.
                heart_rate, heart_rate_measured, o2_rate, o2_rate_measured = calc_hr_and_spo2(*max30102.read_sequential())
                
                # If both data have been red correctly, update the DATA global variable.
                if heart_rate_measured and o2_rate_measured and heart_rate != -999 and o2_rate != -999:
                    DATA["heart_rate"] = heart_rate
                    DATA["O2_rate"]    = int(o2_rate)
                
                # Sleep the process for a second.
                time.sleep(1)
        except OSError:
            # print("Court-circuit pour le capteur MAX30102")
            time.sleep(5)


def run_sd18b20() -> None:
    """Run the sd18b20 sensor routine, retrieving the sensor's data and writing them to the screen."""
    
    # Run the loop until the main thread stops.
    while True:
        # Update the DATA global variable using the get_sd18b20_temperature function.
        DATA["temperature"] = round(get_sd18b20_temperature(), 2)
        
        # Sleep the process for a second.
        time.sleep(1) 


def run_bmp280() -> None:
    """Run the bmp280 sensor routine, retrieving the sensor's data and writing them to the screen."""
    
    # Run the loop until the main thread stops.
    while True:
        # Add a try/except mechanism to handle measurement fails.
        try:
            # Initialize a bmp280 sensor instance.
            bmp280: BMP280 = BMP280()

            # Run the loop until the main thread stops.
            while True:
                try:
                    # Update the DATA global variable using the bmp280's attributes.
                    #DATA["temperature"] = bmp280.temperature
                    DATA["pressure"] = round(bmp280.pressure/1000, 2)
                    DATA["altitude"] = round(bmp280.altitude, 2)
                    
                    # Sleep the process for a second.
                    time.sleep(1)
                except OSError:
                    # print("Court-circuit pour le capteur BMP280")
                    time.sleep(1)
        except ValueError:
            # print("Court-circuit pour le capteur BMP280")
            time.sleep(5)


def run_button(ws2812b: WS2812B) -> None:
    """
    Run the Button routine, waiting for it to be pressed
    in order to turn the given ws2812b into emergency mode.
    
    :param WS2812B ws2812b: The LED strip to turn into emergency when the button get pressed.
    """
    
    # Run the loop until the main thread stops.
    while True:
        # Wait until the button get pressed.
        wait_for_button_pressed()
        
        # Set the LED strip into emergency mode.
        ws2812b.emergency()
        
        # Wait for 10 second.
        time.sleep(10)


def run_ssd1306(ssd1306: SSD1306) -> None:
    """
    Run the ssd1306 device routine, writing periodically the
    content of the DATA global variable on the SSD1306 screen.
    
    :param SSD1306 ssd1306: The instance of the ssd1306 device to write.
    """
    
    # Run the loop until the main thread stops.
    while True:
        try:
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
            heart_rate_string: str = f"""{DATA["heart_rate"]}"""
            o2_rate_string: str = f"""{DATA["O2_rate"]} 02%"""
            temperature_string: str = f"""{DATA["temperature"]} °C"""
            pressure_string: str = f"""{DATA["pressure"]} bar"""
            altitude_string: str = f"""{DATA["altitude"]} m"""
            ssd1306.write(heart_rate_string + (len(f"""{DATA["temperature"]}""")-len(f"""{DATA["heart_rate"]}""")+1)*' ' + "BPM" + (20-(len(temperature_string)+len(o2_rate_string))-1)*' ' + o2_rate_string, 0, 0)
            ssd1306.write(temperature_string + (20-(len(temperature_string)+len(pressure_string)))*' ' + pressure_string, 0, 15)
            ssd1306.write((20-len(altitude_string)-2)*' ' + altitude_string, 0, 30)
            
            # Set the ssd1306 as not busy anymore.
            ssd1306.is_busy = False
            
            # Sleep the loop for 5 seconds.
            time.sleep(5)
        except OSError:
            # print("Court-circuit pour l'écran SSD1306")
            time.sleep(5)


def refresher() -> None:
    """Refresh function for updating the GUI by calling update_data method."""
    
    # Call the gui's update_plot method.
    APP.update_plots()
    
    # Call the gui's update_data method.
    APP.update_data()
    
    # Calling this function again in 1 seconds.
    APP.after(1000, refresher)
    
    
def main() -> None:
    """Main function."""
    
    # Set the global variable MESSAGE_SENT_TIMER writable.
    global MESSAGE_SENT_TIMER
    
    # Set the global variable APP writable.
    global APP
    
    # Try to initialize the screen infinitely until it works.
    while True:
        try:
            # Initialize the ssd1306 device.
            ssd1306: SSD1306 = SSD1306()
            
            # Break the infinite loop.
            break
        except Exception as e:
            # Print the raised exception.
            print(e)
        
            # Retry in 3 seconds.
            print_retry("ssd1306 screen")
            
    # Try to initialize the LED strip infinitely until it works.
    while True:
        try:
            # Initialize the ws2812b device.
            ws2812b: WS2812B = WS2812B()
            
            # Break the infinite loop.
            break
        except Exception as e:
            # Print the raised exception.
            print(e)
        
            # Retry in 3 seconds.
            print_retry("ws2812b LED strip")
            
    try:
        # Run the different threads.
        message_sent_timer_thread: threading.Thread = threading.Thread(target = run_message_sent_timer, daemon=True,)
        message_sent_timer_thread.start()
        max30102_thread: threading.Thread           = threading.Thread(target = run_max30102, daemon=True)
        max30102_thread.start()
        sd18b20_thread: threading.Thread            = threading.Thread(target = run_sd18b20, daemon=True)
        sd18b20_thread.start()
        bmp280_thread: threading.Thread             = threading.Thread(target = run_bmp280, daemon=True)
        bmp280_thread.start()
        button_thread: threading.Thread             = threading.Thread(target = run_button, daemon=True, args=(ws2812b,))
        button_thread.start()
        ssd30102_thread: threading.Thread           = threading.Thread(target = run_ssd1306, daemon=True, args=(ssd1306,))
        ssd30102_thread.start()

        # Initialize the GUI.
        APP = Dashboard(ssd1306, ws2812b, DATA)

        # Call the refresher function.
        refresher()

        # Running the app mainloop.
        APP.mainloop()
    except KeyboardInterrupt:
        print("Program aborted")


if __name__ == "__main__":
    main()
