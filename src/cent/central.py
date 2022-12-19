import socket
import sys
import threading
import json
import RPi.GPIO as GPIO
import time
import os


conns = {}
addresses_list =[]

def readFileConfig(name):
  with open(name,'r') as file:
    object = json.load(file)
    conf = {}
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


def sendRequest(conn, content):
    conn.send(content.encode('ascii'))

def getServers(s):
    try:
        while True:
            conn, add = s.accept() 
            addresses_list.append(add[0]) ##adiciona ao fim da lista
            conns[add[0]] = conn 
            print(f'{str(add)} Conectado!\n')
    except:
        print('Error in Receive')

def getStatusDispAlter(conn):
    try:
        resp = conn.recv(2048).decode('ascii')
        if resp == 'SUCESS':
            print('Estado do dispositivo alternado com sucesso!')
        elif resp == 'UNSUCCESSFULLY':
            print('Problema para trocar o estado do dispositivo! Verifique se o estado desejado já não está em curso')
    except:
        print('Error getting status ')
    


def getStatusAll(conn):
  try:
    status = conn.recv(2048).decode('ascii')
    status = json.loads(status)
    print('--------Saidas--------: ')
    print('\n')
    print('Lâmpada 01 (L_01): '+status['L_01'])
    print('Lâmpada 02 (L_02): '+status['L_02'])
    print('Ar-Condicionado (AC): '+status['AC'])
    print('Projetor Multimídia (PR): '+status['PR'])
    print('Alarme (AL_BZ): '+status['AL_BZ'])
    print('\n')
    print('--------Sensores:--------')
    print('Sensor de Presença (SPres): '+status['SPres'])
    print('Sensor de Fumaça (SFum): '+status['SFum'])
    print('Sensor de Janela (SJan): '+status['SJan'])
    print('Sensor de Porta (SPor): '+status['SPor'])
    print("Temperatura={0:0.1f}*C  Umidade={1:0.1f}%".format(status['Temperatura'], status['Humidade']))
    print('Pessoas na sala: '+status['Pessoas'])
  except:
    print('Error ao obter o status dos dispositivos da sala')

def showStatusOutputs(conn):
  try:
    statusOutputs = conn.recv(2048).decode('ascii')
    statusOutputs = json.loads(statusOutputs)
    print('\n')
    print('1- Lâmpada 01 (L_01) : '+statusOutputs['L_01'])
    print('2- Lâmpada 02 (L_02): '+statusOutputs['L_02'])
    print('3- Ar-Condicionado (AC): '+statusOutputs['AC'])
    print('4- Projetor Multimídia (PR): '+statusOutputs['PR'])
    print('5- Alarme (AL_BZ): '+statusOutputs['AL_BZ'])
    print('\n')
  except:
    print('Erro ao obter o status das saidas!')


def menu():
    opc=-1
    while int (opc)!=0:
                os.system('clear')
                print(' Servidor Central ')
                print('\n')
                print('0- Sair ')
                print('1- Ligar um Dispositivo ')
                print('2- Desligar um Dispositivo ')
                print('3- Ligar todos os dispositivos')
                print('4- Desligar todos os dispositivos')
                print('5- Verificar Status dos sensores e dispositivos ')
                
                opc= input('Escolha uma opção: ')

                if  int (opc) == 0:
                        quit()

                elif int(opc) == 1: ## ON ONE DISP
                    os.system('clear')
                    t=len(addresses_list)
                    if t == 0:
                            print('Nenhuma sala conectada ao servidor central')
                            input('Aperte enter para prosseguir...')
                            continue
                    r = -1
                    tam= len(addresses_list)
                    while r < 0  or r > tam:
                            print('Salas conectadas ao servidor central: ')
                            for i in range(len(addresses_list)):
                                print(f'Sala {i} - IP:{addresses_list[i]}')
                            r = int(input('Digite o numero da sala: '))
                    
                    disp = 0
                    while disp < 1 or disp > 5:
                           
                            print('-------- Dispositivos--------')
                            sendRequest(conns[addresses_list[r]], f'REQUEST_STATE')
                            showStatusOutputs(conns[addresses_list[r]])
                            disp = int(input('Digite o numero do dispositivo que deseja ligar: '))
                            if disp == 1:
                                sendRequest(conns[addresses_list[r]], f'A1')
                                getStatusDispAlter(conns[addresses_list[r]])
                            elif disp == 2:
                                sendRequest(conns[addresses_list[r]], f'A2')
                                getStatusDispAlter(conns[addresses_list[r]])
                            elif disp == 3:
                                sendRequest(conns[addresses_list[r]], f'A3')
                                getStatusDispAlter(conns[addresses_list[r]])
                            elif disp == 4:
                                sendRequest(conns[addresses_list[r]], f'A4')
                                getStatusDispAlter(conns[addresses_list[r]])
                            elif disp == 5:
                                sendRequest(conns[addresses_list[r]], f'A5')
                                getStatusDispAlter(conns[addresses_list[r]])
                            print('Retornando ao menu...')
                            time.sleep(2)

                elif int(opc) == 2: ## OFF ONE DISP
                    os.system('clear')
                    t=len(addresses_list)
                    if t == 0:
                            print('Nenhuma sala conectada ao servidor central')
                            input('Aperte enter para prosseguir...')
                            continue
                    r = -1
                    tam= len(addresses_list)
                    while r < 0  or r > tam:
                            print('Salas conectadas ao servidor central: ')
                            for i in range(len(addresses_list)):
                                print(f'Sala {i} - IP:{addresses_list[i]}')
                            r = int(input('Digite o numero da sala: '))
                    
                    disp = 0
                    while disp < 1 or disp > 5:
                           
                            print('-------- Dispositivos--------')
                            sendRequest(conns[addresses_list[r]], f'REQUEST_STATE')
                            showStatusOutputs(conns[addresses_list[r]])
                            disp = int(input('Digite o numero do dispositivo que deseja desligar: '))
                            if disp == 1:
                                sendRequest(conns[addresses_list[r]], f'D1')
                            elif disp == 2:
                                sendRequest(conns[addresses_list[r]], f'D2')
                            elif disp == 3:
                                sendRequest(conns[addresses_list[r]], f'D3')
                            elif disp == 4:
                                sendRequest(conns[addresses_list[r]], f'D4')
                            elif disp == 5:
                                sendRequest(conns[addresses_list[r]], f'D5')
                            getStatusDispAlter(conns[addresses_list[r]])
                            print('Retornando ao menu...')
                            time.sleep(2)

                elif int(opc) == 3: ## ON ALL DISP
                    os.system('clear')
                    t=len(addresses_list)
                    if t == 0:
                            print('Nenhuma sala conectada ao servidor central')
                            input('Aperte enter para prosseguir...')
                            continue
                    r = -1
                    tam= len(addresses_list)
                    while r < 0  or r > tam:
                            print('Salas conectadas ao servidor central: ')
                            for i in range(len(addresses_list)):
                                print(f'Sala {i} - IP:{addresses_list[i]}')
                            r = int(input('Digite o numero da sala: '))
                    
                    disp = 0
                    while disp < 1 or disp > 2:
                           
                            print('-------- Dispositivos--------')
                            sendRequest(conns[addresses_list[r]], f'REQUEST_STATE')
                            showStatusOutputs(conns[addresses_list[r]])
                            disp = int(input('Tem certeza que deseja ligar todos os dispositivos? Digite 1 para confirmar ou 2 para cancelar '))
                            if disp == 1:
                                sendRequest(conns[addresses_list[r]], f'ONALL')
                                getStatusDispAlter(conns[addresses_list[r]])
                            elif disp == 2:
                                pass
                            print('Retornando ao menu...')
                            time.sleep(2)


                elif int(opc) == 4: ## OFF ALL DISP
                    os.system('clear')
                    t=len(addresses_list)
                    if t == 0:
                            print('Nenhuma sala conectada ao servidor central')
                            input('Aperte enter para prosseguir...')
                            continue
                    r = -1
                    tam= len(addresses_list)
                    while r < 0  or r > tam:
                            print('Salas conectadas ao servidor central: ')
                            for i in range(len(addresses_list)):
                                print(f'Sala {i} - IP:{addresses_list[i]}')
                            r = int(input('Digite o numero da sala: '))
                    
                    disp = 0
                    while disp < 1 or disp > 2:
                           
                            print('-------- Dispositivos--------')
                            sendRequest(conns[addresses_list[r]], f'REQUEST_STATE')
                            showStatusOutputs(conns[addresses_list[r]])
                            disp = int(input('Tem certeza que deseja desligar todos os dispositivos? Digite 1 para confirmar ou 2 para cancelar '))
                            if disp == 1:
                                sendRequest(conns[addresses_list[r]], f'OFFALL')
                                getStatusDispAlter(conns[addresses_list[r]])
                            elif disp == 2:
                                pass
                            print('Retornando ao menu...')
                            time.sleep(2)
        
                elif int(opc) == 5:
                    os.system('clear')
                    if not addresses_list:
                        print('Não foram encontradas salas conectadas ao servidor central!\n')
                        input('Pressione ENTER para prosseguir.....')
                        continue
                    r = -1
                    tam = len(addresses_list)
                    while r < 0 or r > tam:
                            print('Salas conectadas ao servidor central:')
                            for i in range(len(addresses_list)):
                                 print(f'Sala {i} - IP:{addresses_list[i]}')
                            r = int(input('Digite o numero da sala  '))

                    sendRequest(conns[addresses_list[r]], f'REQUEST_STATE') 
                    getStatusAll(conns[addresses_list[r]])
                    input('Aperte enter para prosseguir...')
                else:
                    menu()
                
                
                            
                                  
               
def main():
 
    try:
        #Lendo dados de configuração da sala
        conf= readFileConfig('../jsons/config-s04.json')

        #Configurando endereço do servidor baseado no json
        ip = conf['ip_servidor_central']
        port = conf['porta_servidor_central']

        ##print(ip)
        #print(port)

        server_add = (ip,port)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(server_add) 
        s.listen(4)

        
        th = threading.Thread(target=menu, ) #thread pra rodar menu
        th.start()  # inicia a thread

        getServers(s)
        
    except KeyboardInterrupt:
         quit()


if __name__ == "__main__":
    main()
 

                    

