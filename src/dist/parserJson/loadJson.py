import json

                 
def loadJson():
  try: 
          with open('../jsons/statesSituation.json', 'r') as file:
                  jsonObj = json.load(file)
                  msg = json.dumps(jsonObj).encode('ascii')
          return msg
  except:   
          loadJson()