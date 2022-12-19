import socket
import sys
import threading
import json
import RPi.GPIO as GPIO
import time


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
            print('Houve um problema para trocar o estado do dispositivo!')
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
    print('6- Ligar todos os dispositivos listados acima')
    print('7- Desligar todos os dispositivos listados acima')
    print('\n')
  except:
    print('Erro ao obter o status das saidas!')


def menu():
    opc=-1
    while int (opc)!=0:
                print(' Servidor Central ')
                print('0 - Sair ')
                print('1 - Alterar o estado de um Dispositivo ')
                print('2 - Verificar Status dos sensores e dispositivos ')
                
                opc= input('Escolha uma opção: ')

                if  int (opc) == 0:
                        quit()

                elif int(opc) == 1:
                    if len(addresses_list) == 0:
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
                    
                    device = -1
                    while device < 1 or device > 7:
                           
                            print('-------- Dispositivos--------')
                            sendRequest(conns[addresses_list[r]], f'REQUEST_STATE')
                            showStatusOutputs(conns[addresses_list[r]])
                            device = int(input('Digite o numero do dispositivo que deseja trocar o estado: '))
                            if device == 1:
                                sendRequest(conns[addresses_list[r]], f'1')
                            elif device == 2:
                                sendRequest(conns[addresses_list[r]], f'2')
                            elif device == 3:
                                sendRequest(conns[addresses_list[r]], f'3')
                            elif device == 4:
                                sendRequest(conns[addresses_list[r]], f'4')
                            elif device == 5:
                                sendRequest(conns[addresses_list[r]], f'5')
                            elif device == 6:
                                sendRequest(conns[addresses_list[r]], f'6')
                            elif device == 7:
                                sendRequest(conns[addresses_list[r]], f'7')
                            getStatusDispAlter(conns[addresses_list[r]])
                            print('Retornando ao menu...')
                            time.sleep(2)
        
                elif int(opc) == 2:
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
 

                    

