# PCD8544 (Nokia 5110) LCD sample for Raspberry Pi Pico
# Required library:
#  https://github.com/mcauser/micropython-pcd8544

# Connections:
#   Connect the screen up as shown below using the
#   physical pins indicated (physical pin on pico)

#   RST - Reset:                     Pico GP8 (11)     
#   CE - Chip Enable / Chip select : Pico GP5 ( 7)     
#   DC - Data/Command :              Pico GP4 ( 6)     
#   Din - Serial Input (Mosi):       Pico GP7 (10)
#   Clk - SPI Clock:                 Pico GP6 ( 9)
#   Vcc:                             Pico 3V3 (36)
#   BL :                             Pico GP9 (12)
#   Gnd:                             Pico GND (38)

# Reference
# https://www.youtube.com/watch?v=DehRWwvWFuo&ab_channel=NerdCave

import test.pcd8544_fb as pcd8544_fb
from machine import Pin, SPI

class DisplayNokia:

    # *Use GPIO Number as port pin number

    # set up pins
    spi = SPI(0)
    spi.init(baudrate=2000000, polarity=0, phase=0)
    dc = Pin(4)
    cs = Pin(5)
    rst = Pin(8)

    # set bl on/off
    back_light = Pin(9, Pin.OUT)

    #initialize lcd
    lcd = pcd8544_fb.PCD8544_FB(spi, cs, dc, rst)


    def display_temp(self,*,temp="",scale="",resistance="",showAll = True):
        self.lcd.text('-Leitura-', 0, 0, 1) #text, x, y, visible
        if showAll:
            self.lcd.text('Res:'+resistance,0,12, 1)
            self.lcd.text(scale,0,24, 1)
            self.lcd.text('Tem:'+temp+'C',0,36, 1)
        else:    
            self.lcd.text('Tem:'+temp+'C',0,12, 1)
        self.lcd.clear()
        self.lcd.show()
