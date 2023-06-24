from machine import Pin, SPI # SPI is a class associated with the machine library.

# The below specified libraries have to be included. Also, ssd1306.py must be saved on the Pico. 
from components.ssd1306 import SSD1306_SPI # this is the driver library and the corresponding class
import framebuf # this is another library for the display. 

class Display:
    # Define columns and rows of the oled display. These numbers are the standard values. 
    SCREEN_WIDTH = 128 #number of columns
    SCREEN_HEIGHT = 64 #number of rows
    
    #
    # SPI Device ID can be 0 or 1. It must match the wiring. 
    #
    SPI_DEVICE = 0 # Because the peripheral is connected to SPI 0 hardware lines of the Pico


    # Initialize I/O pins associated with the oled display SPI interface
    # 18, 19, 21, 20, 17
    def __init__(self, sck, sda, res, dc, cs) -> None:
        self.spi_sck = Pin(sck) # sck stands for serial clock; always be connected to SPI SCK pin of the Pico
        self.spi_sda = Pin(sda) # sda stands for serial data;  always be connected to SPI TX pin of the Pico; this is the MOSI
        self.spi_res = Pin(res) # res stands for reset; to be connected to a free GPIO pin
        self.spi_dc  = Pin(dc) # dc stands for data/command; to be connected to a free GPIO pin
        self.spi_cs  = Pin(cs) # chip select; to be connected to the SPI chip select of the Pico 

        # SPI interface for the OLED display
        self.oled_spi = SPI( self.SPI_DEVICE, baudrate= 100000, sck= self.spi_sck, mosi= self.spi_sda )

        # Initialize the display
        self.oled = SSD1306_SPI( self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.oled_spi, self.spi_dc, self.spi_res, self.spi_cs, True )

    def text(self, text, col, row):
        self.oled.text(text, col, row)

    def box(self, x, y, width, height, draw):
        self.oled.rect( x, y, width, height, draw )

    def clear_buffer(self):
        self.oled.fill(0)

    def update_buffer(self):
        self.oled.show()

