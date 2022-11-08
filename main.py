from machine import Pin
import time
import utime
from temperature import *
from display_nokia import *
from max31865 import MAX31865

# ---------------------------------------
# ------------- SETUP    ----------------
# ---------------------------------------

# Micro Python Setup in VS Code
# https://www.youtube.com/watch?v=XuYUaOdO07I&ab_channel=FabioSouza

# PORTS CONFIGURATION
led_internal = Pin(25,Pin.OUT) #INTERNAL LED
led_internal.value(1)

# average number of temperature values
n_average_values = 7

# READ_INTERVAL (ms) 
interval = 1000

#display = Display(sda=24,scl=25)
display = DisplayNokia()
# ---------------------------------------
# ------------- FUNCTIONS----------------
# ---------------------------------------
lista_temperaturas = [] 
def average_temperature(temperatura):
  #Append value to a list
  #Print average of last temperature values
  lista_temperaturas.append(temperatura)
  if(len(lista_temperaturas) > n_average_values):
    lista_temperaturas.pop(0)
    media = sum(lista_temperaturas) / len(lista_temperaturas)
    print('Media ultimos',n_average_values,'valores: {:0.2f}'.format(media))

 
# ---------------------------------------   
led = Pin(27,Pin.OUT)
def blink_led(led,led_internal, time_interval):
    led.high()
    led_internal.high()
    time.sleep_ms(time_interval)
    led.low()
    led_internal.low()
    time.sleep_ms(time_interval)

# ---------------------------------------
# -------------   LOOP   ----------------
# ---------------------------------------

def main():
  
  sensors = {
      "t1": MAX31865(clk_pin=10, sdi_tx_pin = 11, sdo_rx_pin=12,  cs_pin=13, spi_id=1)
      #"t2": MAX31865(clk_pin=10, sdi_tx_pin = 11, sdo_rx_pin=12,  cs_pin=13, spi_id=1)
  }

  # INITIAL TIMESTAMP TIME
  timestamp_initial = utime.ticks_us()
  while True:
    
    print('-----------------------')
    #Tempo
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

    #display.show_display_message(temperatura, timepassed)
    led_internal.toggle() #internal led toggle
    time.sleep_ms(interval)

#RUN
main()
# ---------------------------------------
# ---------------------------------------