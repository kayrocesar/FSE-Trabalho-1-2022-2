import RPi.GPIO as GPIO
import board
import time
import adafruit_dht

def peopleInRoom(conf,obj):
  try:
    count = 0
    while True:
      obj['Pessoas'] = str(count)
      time.sleep(0.0001)
      if GPIO.event_detected(conf['SC_IN']):
          count +=1
      if GPIO.event_detected(conf['SC_OUT']):
          count -=1
          if count < 0:
            count = 0
  except:
    print('Erro ao contar pessoas')


