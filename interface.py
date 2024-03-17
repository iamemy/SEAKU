from __future__      import annotations
from PIL             import Image
from PIL             import ImageDraw
from PIL             import ImageFont
import typing
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import subprocess

DISPLAY: typing.Optional[Display] = None

class Display:
    """Display class gathering methods to interface a 128x64 SSD1306 display."""
    def __init__(self) -> None:
        """Initializer method."""
        
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

    def write(self, text: str, x: int, y: int, font: typing.Optional[ImageFont.Font] = None) -> None:
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


def init_display() -> None:
    """Initialize the 128x64 SSD1306 display."""
    
    # Make the DISPLAY global variable writable.
    global DISPLAY
    
    # Initialize the DISPLAY global variable.
    DISPLAY = Display()


def main() -> None:
    """Main function."""
    
    # Initialize the display.
    init_display()

    
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
            
            
        
        #[text[20*i:20*(i+1)] for i in range(int(len(text)/20)+1)]
        
        # Initialize a lineno variable.
        lineno: int = 0
        
        # Clear the screen.
        DISPLAY.clear()
        
        # Write the obtained texts.
        for text_ in texts:
            if lineno == 4:
                # Wait 5 seconds for the display's content to be read.
                time.sleep(5)

                # Clear the display.
                DISPLAY.clear()
                lineno = 0
            # Write the text_ content and increment the lineno variable.
            DISPLAY.write(text_.strip(), 0, 15*lineno)
            lineno += 1


if __name__ == "__main__":
    main()
