from machine import Pin
import time
import utime
from src.display_nokia import DisplayNokia
from src.max31865 import MAX31865

# ---------------------------------------
# ------------- SETUP    ----------------
# ---------------------------------------

# PORTS CONFIGURATION
led_internal = Pin(25,Pin.OUT) #INTERNAL LED

# READ_INTERVAL (ms) 
interval = 1000

# DISPLAY CLASS
display = DisplayNokia()
# ---------------------------------------
# -------------   LOOP   ----------------
# ---------------------------------------

def main():
  # INITIAL TIMESTAMP
  timestamp_initial = utime.ticks_us()
  # TURN ON INTERNAL RASPBERRY PICO LED
  led_internal.value(1)
  
  #LOOP: READ SENSORS
  while True:

    # SENSORS MAPPING
    # INSIDE LOOP TO RESET THE MODULE IN CASE OF PIN READING ERRORS
    sensors = {
      "t1": MAX31865(clk_pin=10, sdi_tx_pin = 11, sdo_rx_pin=12,  cs_pin=13, spi_id=1),
      #"t2": MAX31865(clk_pin=10, sdi_tx_pin = 11, sdo_rx_pin=12,  cs_pin=13, spi_id=1)
    }

    print('-----------------------')
    #Read Time
    timestamp_actual = utime.ticks_us()
    timepassed = (timestamp_actual - timestamp_initial ) /1000000
    print('{:0.2f}s'.format(timepassed)) 

    #Read
    read_map = {nome: sensor.read() for (nome, sensor) in sensors.items()}
    print(read_map)

    #Display
    temp = str(read_map['t1']['value'])
    resistance = str(round(read_map['t1']['raw']['resistance'],2))
    scale = read_map['t1']['unit']
    #adc = str(read_map['t1']['raw']['adc'])
    display.display_temp(temp = temp, scale=scale, resistance=resistance, showAll=True)
    display.lcd.fill(0)

    led_internal.toggle() #internal led toggle
    time.sleep_ms(interval)

#RUN
main()
