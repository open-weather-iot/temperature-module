# Connections:
#   Connect the screen up as shown below using the
#   physical pins indicated (physical pin on pico)

#   Vin                              Pico VIN (36)     
#   GND :                            Pico GND (28)     
#   3V3 :    
#   CLK : SPI Clock:                 Pico GP10 (14)
#   SDO : Serial Output(MISO-tx)     Pico GP11 (15)
#   SDI : Serial Input (MOSI-rx)     Pico GP12 (16)
#   CS  :                            Pico GP13 (17)
#   RDY :                             

from machine import Pin, SPI
import math

    # PT100 Temperature Project 
    # https://forum.micropython.org/viewtopic.php?t=5181
    # https://forum.micropython.org/viewtopic.php?f=21&t=12779
    # https://htlb-atk.github.io/schilf-iot-MAX31865/#spi-bus-interface

    # SPI com Raspberry Pico
    # https://www.youtube.com/watch?time_continue=232&v=s7Lud1Gqrqw&feature=emb_logo&ab_channel=LearnEmbeddedSystems

class MAX31865:

    ### Register constants, see data sheet for info.
    # Read Addresses
    MAX31865_REG_READ_CONFIG  = 0x00
    MAX31865_REG_READ_RTD_MSB = 0x01
    MAX31865_REG_READ_RTD_LSB = 0x02
    MAX31865_REG_READ_HFT_MSB = 0x03
    MAX31865_REG_READ_HFT_LSB = 0x04
    MAX31865_REG_READ_LFT_MSB = 0x05
    MAX31865_REG_READ_LFT_LSB = 0x06
    MAX31865_REG_READ_FAULT   = 0x07

    # Write Addresses
    MAX31865_REG_WRITE_CONFIG  = 0x80
    MAX31865_REG_WRITE_HFT_MSB = 0x83
    MAX31865_REG_WRITE_HFT_LSB = 0x84
    MAX31865_REG_WRITE_LFT_MSB = 0x85
    MAX31865_REG_WRITE_LFT_LSB = 0x86

    # Configuration Register
    MAX31865_CONFIG_50HZ_FILTER = 0x01
    MAX31865_CONFIG_CLEAR_FAULT = 0x02
    MAX31865_CONFIG_3WIRE       = 0x10
    MAX31865_CONFIG_ONE_SHOT    = 0x20
    MAX31865_CONFIG_AUTO        = 0x40
    MAX31865_CONFIG_BIAS_ON     = 0x80

    # *Use GPIO Number as port pin number
    # Pelo datasheet o MAX31865 só funciona nos modos 1 e 3 da comunicação SPI
    
    def __init__(self, wires=4, clk_pin=10, sdi_tx_pin = 11, sdo_rx_pin=12,  cs_pin=13, spi_id=1):

        self.CS = Pin(cs_pin, mode=Pin.OUT)
        self.CS.value(True)  # init chip select
        self.spi = SPI(spi_id, 
                        baudrate=115200, polarity=0, phase=1, firstbit=SPI.MSB, 
                        mosi=Pin(sdi_tx_pin, Pin.OUT), 
                        sck=Pin(clk_pin, Pin.OUT), 
                        miso=Pin(sdo_rx_pin, Pin.OUT)
                        )

        # set configuration register
        config = self.MAX31865_CONFIG_BIAS_ON + self.MAX31865_CONFIG_AUTO + self.MAX31865_CONFIG_CLEAR_FAULT + self.MAX31865_CONFIG_50HZ_FILTER
        if (wires == 3):
            config = config + self.MAX31865_CONFIG_3WIRE

        buf = bytearray(2)
        buf[0] = self.MAX31865_REG_WRITE_CONFIG  # config write address
        buf[1] = config
        self.CS.value(False)                      # Select chip
        nw=self.spi.write(buf)              # write config
        self.CS.value(True)

        self.RefR = 424.0
        self.R0  = 100.0

    def read(self):
        raw = self._get_raw()
        temperature, resistance = self._RawToTemp(raw)
        
        temperature = str(round(temperature, 2))
        
        return { 'raw': {'adc': raw,'resistance': resistance}, 'value': temperature,'unit': 'Celsius' }

    def _get_raw(self):
        self.CS.value(False)
        nw=self.spi.write(bytes([0x01])) # first read address
        MSB = self.spi.read(1)           # multi-byte transfer
        LSB = self.spi.read(1)
        self.CS.value(True)

        raw = (MSB[0] << 8) + LSB[0]
        raw = raw >> 1
        return raw

    def _RawToTemp(self, raw):
        RTD = (raw * self.RefR) / (32768)
        A = 3.908e-3
        B = -5.775e-7

        temperature = ((-A + math.sqrt(A*A - 4*B*(1-RTD/self.R0))) / (2*B))
        return temperature, RTD