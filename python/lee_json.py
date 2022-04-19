import pandas as pd
#AUTOTT:::


#Marcelo estuvo aqui

def leeJSON(path_, file_):
    completePath = f"{path_}{file_}"
    df = pd.read_json(completePath)
    print(df.to_string()) 

def clasificaPor(path_, file_,type_):
    type_ # ese el campo por el que se nos va a ocurrir clasificator
    #ejemplos:



leeJSON("","test_json.json")




