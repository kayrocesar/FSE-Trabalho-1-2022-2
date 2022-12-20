import time
import os
import logging
import csv



def commandsLog(content):

    if content == 'REQUEST_STATE':
        content= "Listar Dispositivos"
    elif content == 'A1':
        content= "Ligar Lampada 1"
    elif content == 'D1':
        content= "Desligar Lampada 1"
    elif content == 'A2':
        content= "Ligar Lampada 2"
    elif content == 'D2':
        content= "Desligar Lampada 2"
    elif content == 'A3':
        content= "Ligar Ar Condicionado"
    elif content == 'D3':
        content= "Desligar Ar Condicionado"
    elif content == 'A4':
        content= "Ligar Projetor"
    elif content == 'D4':
        content= "Desligar Projetor"
    elif content == 'A5':
        content= "Ligar Alarme"
    elif content == 'D5':
        content= "Desligar Alarme"
    elif content == 'ONALL':
        content= "Ligar todos os dispositivos"
    elif content == 'OFFALL':
        content= "Desligar todos os dispositivos"

    row = [time.ctime() , content]    
    with open('../log/log.csv', 'a') as file:
                w = csv.writer(file)
                w.writerow(row)


