#!/usr/bin/env python3
import socket
import RPi.GPIO as GPIO
import board
import time
import adafruit_dht
import json
import threading
import sensorTempHum
import contPeopleRoom


def pinsConfig(conf):
 
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(conf['L_01'], GPIO.OUT)
  GPIO.setup(conf['L_02'], GPIO.OUT)
  GPIO.setup(conf['PR'], GPIO.OUT)
  GPIO.setup(conf['AC'], GPIO.OUT)
  GPIO.setup(conf['AL_BZ'], GPIO.OUT)
  GPIO.setup(conf['SPres'], GPIO.IN)
  GPIO.setup(conf['SFum'], GPIO.IN)
  GPIO.setup(conf['SJan'], GPIO.IN)
  GPIO.setup(conf['SPor'], GPIO.IN)
  GPIO.setup(conf['SC_IN'], GPIO.IN)
  GPIO.setup(conf['SC_OUT'], GPIO.IN)


def statesAll(conf):
  try:
    pinsConfig(conf)

    obj = {
      'L_01': 'OFF',
      'L_02': 'OFF',
      'AC': 'OFF',
      'PR': 'OFF',
      'AL_BZ': 'OFF',
      'SPres': 'OFF',
      'SFum': 'OFF',
      'SJan': 'OFF',
      'SPor': 'OFF',
      'Temperatura': '0',
      'Humidade': '0',
      'Pessoas': 0
    }
    GPIO.add_event_detect(conf['SC_IN'], GPIO.RISING)
    GPIO.add_event_detect(conf['SC_OUT'], GPIO.RISING)
    dhtThread = threading.Thread(target=sensorTempHum.tempHumidity, args=(conf,obj))
    dhtThread.start()
    peopleInRoomThread = threading.Thread(target=contPeopleRoom.peopleInRoom, args=(conf,obj))
    peopleInRoomThread.start()


    while True:
      time.sleep(0.05)
      if GPIO.input(conf['L_01']):
        obj['L_01'] = 'ON'
      else:
        obj['L_01'] = 'OFF'

      if GPIO.input(conf['L_02']):
         obj['L_02'] = 'ON'
      else:
        obj['L_02'] = 'OFF'

      if GPIO.input(conf['AC']):
        obj['AC'] = 'ON'
      else:
        obj['AC'] = 'OFF'

      if GPIO.input(conf['PR']):
        obj['PR'] = 'ON'
      else:
        obj['PR'] = 'OFF'

      if GPIO.input(conf['AL_BZ']):
        obj['AL_BZ'] = 'ON'
      else:
        obj['AL_BZ'] = 'OFF'

      if GPIO.input(conf['SPres']):
        obj['SPres'] = 'ON'
      else:
        obj['SPres'] = 'OFF'

      if GPIO.input(conf['SFum']):
        obj['SFum'] = 'ON'
      else:
        obj['SFum'] = 'OFF'
      
      if GPIO.input(conf['SJan']):
        obj['SJan'] = 'ON'
      else:
        obj['SJan'] = 'OFF'
      
      if GPIO.input(conf['SPor']):
        obj['SPor'] = 'ON'
      else:
        obj['SPor'] = 'OFF'
      
      with open('../jsons/statesSituation.json', 'w') as file:
                 json.dump(obj,file) 

  except KeyboardInterrupt: 
    pass