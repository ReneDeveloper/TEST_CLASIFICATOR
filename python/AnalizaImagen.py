import pandas as pd
import numpy as np
import json

from sklearn.cluster import KMeans
from sqlalchemy import false

def LeeJSON(path_, file_):
    completePath = f"{path_}{file_}"
    df = pd.read_json(completePath)
    return df 
def defineAnchoBandeja():
    
    ancho= 1000
    return ancho


def DefBandejas(cdato,CampoFila):
    # cdato es el set de datos original para formar las bandejas
    #print (CampoFila)
    csalida = cdato.groupby(CampoFila).size().reset_index(name = "Cantidad")
    #print(csalida)
    ResObjBandeja= []
    prom= []
    prom_y1 =[]
    AnchoBandeja = []
    botfaltantes =[]

    vAnchoBandeja = defineAnchoBandeja()

    for i in csalida.index: 
        #print(csalida[CampoFila][i])
        
        ctemp = cdato[cdato[CampoFila] == i]                    #datos correspondientes a la fila
        vprom = ctemp['w'].mean()                             #obtiene el promedio de la fila filtrada
        vprom_y1 = int(ctemp['y1'].mean())                             #Obtiene el promedio de las y1
        #print(vprom)
        vcant= (csalida['Cantidad'][i])                         #obtiene la cantidad de botellas de la fila
        vbotfaltantes = int(vAnchoBandeja / vprom) - vcant      #infiere las botellas faltantes de acuerdo al promedio y al ancho en enteros

        # se cargan los arreglos

       
        cbandeja = cdato[cdato[CampoFila] == i]
        cbandejaRecord =cbandeja.to_dict('records')
        ResObjBandeja.append(cbandejaRecord)

        prom.append(vprom)
        prom_y1.append(vprom_y1)
        AnchoBandeja.append(vAnchoBandeja)
        botfaltantes.append(vbotfaltantes)
       


    
    
    csalida['wprom'] = prom
    csalida['y1prom'] = prom_y1
    csalida['anchobandeja'] = AnchoBandeja
    csalida['botFaltantes'] = botfaltantes
    csalida['botellas']     = ResObjBandeja

    return csalida.sort_values(by =['y1prom'] , ascending=True)


carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
Archivo ="OUT__ELEGIDA_27012022165311_FOTO_SALA_BUENA_CONFILA.json"

ArchivoSalida= f"{Archivo.split('.')[0]}_Y_ANALISIS.json"

Datos = LeeJSON(carpeta,Archivo)


CampoFila = "Fila"

cbandejas = DefBandejas(Datos,CampoFila)


print(cbandejas)

resultado = cbandejas.to_dict('records')

rutasalida= carpeta + ArchivoSalida
with open(rutasalida, 'w') as file:
     json.dump(resultado, file, indent = 4)

print (f"Finaliza Generador de bandejas OK\n{rutasalida}")


#js = cbandejas.to_json(orient='records')
#Salida="Databandeja.json"
#rutasalida= carpeta + Salida
#
#
#with open(rutasalida, 'w') as file:
#    print(js, file=file)
#    file.close()
#
#