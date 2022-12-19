import time
import os
import json
import threading
import controllerStates
import socket
import RPi.GPIO as GPIO


def readFileConfig(name):
  with open(name,'r') as file:
    conf = {}
    object = json.load(file)
    conf['ip_servidor_central'] = object['ip_servidor_central']
    conf['porta_servidor_central'] = object['porta_servidor_central']
    conf['ip_servidor_distribuido'] = object['ip_servidor_distribuido']
    conf['porta_servidor_distribuido'] = object['porta_servidor_distribuido']
    conf['nome'] = object['nome']
    conf['L_01'] = object['outputs'][0]['gpio']
    conf['L_02'] = object['outputs'][1]['gpio']
    conf['PR'] = object['outputs'][2]['gpio']
    conf['AC'] = object['outputs'][3]['gpio']
    conf['AL_BZ'] = object['outputs'][4]['gpio']
    conf['SPres'] = object['inputs'][0]['gpio']
    conf['SFum'] = object['inputs'][1]['gpio']
    conf['SJan'] = object['inputs'][2]['gpio']
    conf['SPor'] = object['inputs'][3]['gpio']
    conf['SC_IN'] = object['inputs'][4]['gpio']
    conf['SC_OUT'] = object['inputs'][5]['gpio']
    conf['DHT22'] = object['sensor_temperatura'][0]['gpio']
    return conf


def handle(server, conf):
  try:
    while True:
      received_msg = server.recv(2048).decode('ascii')
      print (received_msg)
      if received_msg == 'REQUEST_STATE':
        #func fazer tratamento
        with open('../jsons/statesSituation.json', 'r') as openfile:
          json_object = json.load(openfile)
          msg_to_send = json.dumps(json_object).encode('ascii')
          server.send(msg_to_send)

      if received_msg == 'A1':
          if not GPIO.input(conf['L_01']):
            GPIO.output(conf['L_01'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

      if received_msg == 'A2':
          if not GPIO.input(conf['L_02']):
            GPIO.output(conf['L_02'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

      if received_msg == 'A3':
          if not GPIO.input(conf['AC']):
            GPIO.output(conf['AC'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

      if received_msg == 'A4':
          if not GPIO.input(conf['PR']):
            GPIO.output(conf['PR'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

      if received_msg == 'A5':
          if not GPIO.input(conf['AL_BZ']):
            GPIO.output(conf['AL_BZ'], GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

       #OFF DISP
      if received_msg == 'D1': 
          if GPIO.input(conf['L_01']):
            GPIO.output(conf['L_01'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

      if received_msg == 'D2':
          if GPIO.input(conf['L_02']):
            GPIO.output(conf['L_02'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

      if received_msg == 'D3':
          if  GPIO.input(conf['AC']):
            GPIO.output(conf['AC'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

      if received_msg == 'D4':
          if  GPIO.input(conf['PR']):
            GPIO.output(conf['PR'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

      if received_msg == 'D5':
          if GPIO.input(conf['AL_BZ']):
            GPIO.output(conf['AL_BZ'], GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
            continue
          else: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))
            continue

      if received_msg == 'ONALL':
          try:
            GPIO.output(conf['L_01'] ,GPIO.HIGH)
            GPIO.output(conf['L_02'], GPIO.HIGH)
            GPIO.output(conf['AC'] ,GPIO.HIGH)
            GPIO.output(conf['PR'] ,GPIO.HIGH)
            GPIO.output(conf['AL_BZ'] ,GPIO.HIGH)
            server.send('SUCCESS'.encode('ascii'))
            continue
          except: 
            server.send('UNSUCCESSFULLY'.encode('ascii'))

      if received_msg == 'OFFALL':
          try:
            GPIO.output(conf['L_01'], GPIO.LOW)
            GPIO.output(conf['L_02'] ,GPIO.LOW)
            GPIO.output(conf['AC'] ,GPIO.LOW)
            GPIO.output(conf['PR'] ,GPIO.LOW)
            GPIO.output(conf['AL_BZ'] ,GPIO.LOW)
            server.send('SUCCESS'.encode('ascii'))
            continue
          except:
            server.send('UNSUCCESSFULLY'.encode('ascii'))

  except RuntimeError as error:
        return error.args[0]

def main():
    #Lendo dados de configuração da sala
    conf= readFileConfig('../jsons/config-s04.json')

    #Configurando endereço do servidor baseado no json
    ip = conf['ip_servidor_central']
    port = conf['porta_servidor_central']

    print(ip)
    print(port)

    server_add = (ip,port)

    sdist = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sdist.connect(server_add)

    
    cr = threading.Thread(target=controllerStates.statesAll, args=(conf,)) #thread pra atualização de dados da sala
    cr.start()  # inicia a thread
    handle(sdist,conf) ##conecta ao central


if __name__ == "__main__":
    main()


                    

