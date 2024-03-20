from PIL               import Image
from PIL               import ImageDraw
from PIL               import ImageFont
import typing
import Adafruit_GPIO.SPI   as SPI
import Adafruit_SSD1306


class SSD1306:
    """SSD1306 class gathering methods to interface a 128x64 SSD1306 display."""
    def __init__(self) -> None:
        """Initializer method."""
        
        # Initialize the is_busy attribute.
        self.__is_busy: bool = False
        
        # Initialize the display attribute.
        self.__display: Adafruit_SSD1306.SSD1306_128_64 = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        
        # Initialize the width and height attributes.
        self.__width: int = self.__display.width
        self.__height: int = self.__display.height
        
        # Initialize the top attribute.
        self.__top: int = 2
        
        # Initialize the image attribute.
        self.__image: Image = Image.new('1', (self.__width, self.__height))
        
        # Initialize the font attribute.
        self.__font: ImageFont.Font = ImageFont.load_default()
        
        # Initialize the draw attribute.
        self.__draw: ImageDraw.Draw = ImageDraw.Draw(self.__image)

        # Draw a black filled box to clear the image.
        self.__draw.rectangle((0, 0, self.__width, self.__height), outline=0, fill=0)
        
        # Initialize the Adafruit library.
        self.__display.begin()

        # Clear the display.
        self.__display.clear()
        self.__display.display()
    
    def clear(self) -> None:
        """Clear the screen."""

        # Draw a black filled box to clear the image.
        self.__draw.rectangle((0, 0, self.__width, self.__height), outline=0, fill=0)
        
        # Display image.
        self.__display.image(self.__image)
        self.__display.display()

    def write(self, text: str, x: int, y: int, font: typing.Optional[ImageFont.ImageFont] = None) -> None:
        """
        Write a given text on the given coordonates.
        The (0;0) coordonate correspond ot the top-left screen corner.
        If no font is provided, the default one will be used.
        
        :param str text: The text to write on the 128x64 SSD1306 screen.
        :param int x: The x coordonates to write the text.
        :param int y: The y coordonate to write the text.
        :param font: The optional font to use. By default, None.
        :type font: ImageFont.Font
        """
        
        # Draw the text on the image attribute using the draw attribute.
        self.__draw.text((x, y), text, font=self.__font if font is None else font, fill=1)

        # Display image.
        self.__display.image(self.__image)
        self.__display.display()

    @property
    def is_busy(self) -> bool:
        """Getter method for the is_busy attribute."""
        return self.__is_busy

    @is_busy.setter
    def is_busy(self, is_busy: bool) -> None:
        """
        Setter method for the is_busy attribute.
        
        :param bool is_busy: The new is_busy attribute to set.
        """
        self.__is_busy = is_busy