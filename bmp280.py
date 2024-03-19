import board
import adafruit_bmp280

# Initialize a adafruit_bmp280 instance to be imported.
class BMP280(adafruit_bmp280.Adafruit_BMP280_I2C):
    """Simple wrapper class to Adafruit_BMP280_I2C."""

    def __init__(self) -> None:
        """Initializer method"""
        
        # Calling the super() class constructor.
        super().__init__(board.I2C(), address=0x76)
        
# bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(board.I2C(), address=0x76)
