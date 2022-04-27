#OUT__ELEGIDA_27012022165311_FOTO_SALA_BUENA_CONFILA_Y_CANTIDAD.json
from tokenize import Exponent
import pandas as pd
import numpy as np
import json
from pandas import json_normalize

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
    
    prom= []
    prom_y1 =[]
    AnchoBandeja = []
    botfaltantes =[]
    exportar = pd.DataFrame()
#
    vAnchoBandeja = defineAnchoBandeja()
    #print(vAnchoBandeja)
    Campos_utilizar = ["w","y1","id_interno"]
    for i in cdato.index: 
        Bandeja_x = cdato["Objetos"][i]
   
        df = json_normalize(Bandeja_x)              #Results contain the required data
        df_work = np.array(df[Campos_utilizar])
        salida= pd.DataFrame(df_work, columns=Campos_utilizar)

        vprom = salida['w'].mean()                             #obtiene el promedio de la fila filtrada
        vprom_y1 = int(salida['y1'].mean())                             #Obtiene el promedio de las y1
        vcant= (cdato['Cantidad'][i])                         #obtiene la cantidad de botellas de la fila
        vbotfaltantes = int(vAnchoBandeja / vprom) - vcant      #infiere las botellas faltantes de acuerdo al promedio y al ancho en enteros
       # se cargan los arreglos
        prom.append(vprom)
        prom_y1.append(vprom_y1)
        AnchoBandeja.append(vAnchoBandeja)
        botfaltantes.append(vbotfaltantes)
    
 

    

    exportar['Fila'] = cdato['Fila'].values
    exportar['Cantidad'] = cdato['Cantidad'].values
    exportar['y1prom'] = prom_y1
    exportar['anchobandeja'] = AnchoBandeja
    exportar['botFaltantes'] = botfaltantes
    exportar['Objetos'] = cdato['Objetos'].values

    return exportar.sort_values(by =['y1prom'] , ascending=True)



print (f"Inicia Generador de bandejas OK")
carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
Archivo ="OUT__ELEGIDA_27012022165311_FOTO_SALA_BUENA_CONFILA_Y_CANTIDAD.json"

ArchivoSalida= f"{Archivo.split('.')[0]}_Y_ANALISIS2.json"

Datos = LeeJSON(carpeta,Archivo)

CampoFila = "Fila"
cbandejas = DefBandejas(Datos,CampoFila)

resultado = cbandejas.to_dict('records')

rutasalida= carpeta + ArchivoSalida
with open(rutasalida, 'w') as file:
     json.dump(resultado, file, indent = 4)

print (f"Finaliza Generador de bandejas OK\n{rutasalida}")


