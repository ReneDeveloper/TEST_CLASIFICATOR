from re import A
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
    resp= []

    for i in csalida.index: 
        print(csalida[CampoFila][i])
        resp.append(cdato[cdato[CampoFila] == i])

    csalida['Objetos'] = resp
    return csalida


carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
Archivo ="DataConFila.json"
Datos = LeeJSON(carpeta,Archivo)

#print(Datos)
CampoFila = "Fila"

cbandejas = DefBandejas(Datos,CampoFila)
js = cbandejas.to_json(orient='records')
Salida="Databandeja.json"
rutasalida= carpeta + Salida
with open(rutasalida, 'w') as file:
    print(js, file=file)
    file.close()
    