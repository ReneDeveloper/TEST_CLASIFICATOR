import pandas as pd
import numpy as np
import json

from sklearn.cluster import KMeans

def LeeJSON(path_, file_):
    completePath = f"{path_}{file_}"
    df = pd.read_json(completePath)
    return df 

def DefBandejas(cdato,CampoFila):
    # cdato es el set de datos original para formar las bandejas
    #print (CampoFila)
    csalida = cdato.groupby(CampoFila).size().reset_index(name = "Cantidad")
    ResObjBandeja= []
    expo = {}
  
    for i in csalida.index: 
        #print(csalida[CampoFila][i])
        cbandeja = cdato[cdato[CampoFila] == i]
        cbandejaRecord =cbandeja.to_dict('records')
        ResObjBandeja.append(cbandejaRecord)
         
    
    csalida['Objetos'] = ResObjBandeja
    return csalida


carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
Archivo ="OUT__ELEGIDA_27012022165311_FOTO_SALA_BUENA_CONFILA.json"

ArchivoSalida= f"{Archivo.split('.')[0]}_Y_CANTIDAD.json"

Datos = LeeJSON(carpeta,Archivo)

CampoFila = "Fila"

print ("inicia Generador de Filas")

cbandejas = DefBandejas(Datos,CampoFila)
resultado = cbandejas.to_dict('records')

rutasalida= carpeta + ArchivoSalida
with open(rutasalida, 'w') as file:
     json.dump(resultado, file, indent = 4)

print (f"Finaliza Generador de bandejas OK\n{rutasalida}")
