import RPi.GPIO as GPIO
import board
import time
import adafruit_dht


def tempHumidity(conf,obj):
  try:
    while True:
      time.sleep(0.002)
      if conf['DHT22'] == 18:
         dht_device = adafruit_dht.DHT22(board.D18, False)
      elif conf['DHT22'] == 4:
         dht_device = adafruit_dht.DHT22(board.D4, False)
      
      temp = dht_device.temperature
      hum = dht_device.humidity
      obj['Temperatura'] = temp
      obj['Humidade'] = hum
  except:
    tempHumidity(conf,obj)

