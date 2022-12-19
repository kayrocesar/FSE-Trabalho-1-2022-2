import json

                 
def writeJson(obj):
  try:
        with open('../jsons/statesSituation.json', 'w') as file:
                 json.dump(obj,file) 
       
  except:   
          writeJson()