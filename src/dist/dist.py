import time
import os
import json
import threading
import controllerStates
import socket
import RPi.GPIO as GPIO
from parserJson.loadJson import loadJson
from readFileConfigDist import readFileConfigDist

def  onOneDisp(received_msg, conf, server):
  if received_msg[1] == '1':
          if not GPIO.input(conf['L_01']):
            GPIO.output(conf['L_01'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
  if received_msg[1] == '2':
          if not GPIO.input(conf['L_02']):
            GPIO.output(conf['L_02'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

  if received_msg[1] == '3':
          if not GPIO.input(conf['AC']):
            GPIO.output(conf['AC'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

  if received_msg[1] == '4':
          if not GPIO.input(conf['PR']):
            GPIO.output(conf['PR'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

  if received_msg[1] == '5':
          if not GPIO.input(conf['AL_BZ']):
            GPIO.output(conf['AL_BZ'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

def  offOneDisp(received_msg, conf, server):
      if received_msg[1] == '1': 
          if GPIO.input(conf['L_01']):
            GPIO.output(conf['L_01'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            

      if received_msg[1] == '2': 
          if GPIO.input(conf['L_02']):
            GPIO.output(conf['L_02'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

      if received_msg[1] == '3': 
          if  GPIO.input(conf['AC']):
            GPIO.output(conf['AC'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

      if received_msg[1] == '4': 
          if  GPIO.input(conf['PR']):
            GPIO.output(conf['PR'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

      if received_msg[1] == '5': 
          if GPIO.input(conf['AL_BZ']):
            GPIO.output(conf['AL_BZ'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

def  onAllDisp(conf, server):
    try:
            GPIO.output(conf['L_01'] ,GPIO.HIGH)
            GPIO.output(conf['L_02'], GPIO.HIGH)
            GPIO.output(conf['AC'] ,GPIO.HIGH)
            GPIO.output(conf['PR'] ,GPIO.HIGH)
            GPIO.output(conf['AL_BZ'] ,GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
    except: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

def  offAllDisp(conf, server):
    try:
            GPIO.output(conf['L_01'], GPIO.LOW)
            GPIO.output(conf['L_02'] ,GPIO.LOW)
            GPIO.output(conf['AC'] ,GPIO.LOW)
            GPIO.output(conf['PR'] ,GPIO.LOW)
            GPIO.output(conf['AL_BZ'] ,GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
    except:
            server.send('UNSUCCESSFULLY'.encode('ascii'))


def handle(server, conf):
  try:
    while True:
      received_msg = server.recv(2048).decode('ascii')
      print (received_msg)
      if received_msg == 'REQUEST_STATE':
        threadLoad = threading.Thread(target=loadJson, args=()) 
        threadLoad.start()
        msg_back=loadJson()
        server.send(msg_back)

      if received_msg[0] == 'A':
         onOneDisp(received_msg,conf, server )

      if received_msg[0] == 'D':
         offOneDisp(received_msg,conf, server )

      if received_msg == 'ONALL':
         onAllDisp(conf, server )

      if received_msg == 'OFFALL':
         offAllDisp(conf, server )
  except RuntimeError as error:
        return error.args[0]

def main():
    
    conf= readFileConfigDist('../jsons/config-s04.json')

    
    ip = conf['ip_servidor_central']
    port = conf['porta_servidor_central']
    server_add = (ip,port)
    
    sdist = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sdist.connect(server_add)

    
    cr = threading.Thread(target=controllerStates.statesAll, args=(conf,)) #thread pra atualização de dados da sala
    cr.start()  # inicia a thread
    handle(sdist,conf) ##conecta ao central


if __name__ == "__main__":
    main()


                    

