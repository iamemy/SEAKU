from rpi_ws281x import Adafruit_NeoPixel, Color
import time

class WS2812B(Adafruit_NeoPixel):
    """WS2812B class gathering methods to interface a ws2812b LED strip."""
    def __init__(self, idle_brightness: int = 16, emergency_brightness: int = 255) -> None:
        """Initializer method."""
        
        # Call the super() class initializer.
        super().__init__(60, 21, 800000, 10, False, idle_brightness, 0)
        
        # Set the straight-forward attributes.
        self.__idle_brightness: int = idle_brightness
        self.__emergency_brightness: int = emergency_brightness
        self.__state: bool = False # False is IDLE, True is EMERGENCY.
        
        # Initialize the LED strip.
        self.begin()
        
        # Set the ws2812b LED strip into idle mode.
        self.idle()
    
    def idle(self) -> None:
        """Show the LED strip in IDLE mode."""
        
        # Update the LED strip state.
        self.__state = False
        
        # Set the brightness to IDLE brightness.
        self.setBrightness(self.__idle_brightness)
        
        # For each LED out of two, give it the IDLE color.
        for i in range(int(self.numPixels()/2)):
            self.setPixelColor(2*i, Color(161, 222, 255))

        # Update the LED strip.
        self.show()
    
    def emergency(self) -> None:
        """Show the LED strip in EMERGENCY mode."""
        
        # Update the LED strip state.
        self.__state = True
        
        # Set the brightness to EMERGENCY brightness.
        self.setBrightness(self.__emergency_brightness)
        
        # Loop for 10 seconds.
        for _ in range(10):
            # For each LED, give it the EMERGENCY color.
            for i in range(self.numPixels()):
                self.setPixelColor(i, Color(255, 0, 0))
            
            # Update the LED strip.
            self.show()
            
            # Sleep 500 ms.
            time.sleep(0.5)
            
            # For each LED, give it the WHITE color.
            for i in range(self.numPixels()):
                self.setPixelColor(i, Color(255, 255, 255))
            
            # Update the LED strip.
            self.show()
            
            # Sleep 500 ms.
            time.sleep(0.5)
        
        # Set the LED strip in IDLE mode.
        self.idle()
    
    def end(self) -> None:
        """Turn off every LED from the LED strip."""
        
        # Turn off each LED.
        for i in range(self.numPixels()):
            self.setPixelColor(i, Color(0, 0, 0))
            
        # Update the LED strip.
        self.show()
    
    @property
    def is_emergency(self) -> bool:
        """Getter method for the state attribute."""
        return self.__state
