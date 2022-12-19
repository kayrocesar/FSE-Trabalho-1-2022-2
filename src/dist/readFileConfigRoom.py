import json


def readFileConfigRoom(name):
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



