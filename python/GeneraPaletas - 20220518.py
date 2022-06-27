from xml.dom.expatbuilder import CDATA_SECTION_NODE
import pandas as pd
import numpy as np
import json

from sklearn.cluster import KMeans

def leeJSON(path_, file_):
    completePath = f"{path_}{file_}"
    df = pd.read_json(completePath)
    return df 

def clasificador(cdato, argcalificador,ncluster):
    # cdato es el set de datos original debe contener el campo id_interno
    # argcalificador # ese el conjunto de campos por el que se nos van a clasificar los grupos, deben ser valores numericos
    # ncluster  la cantidad de cluster a utilizar
    #ejemplos:
    ccluster = np.array(cdato[argcalificador])
    kmeans = KMeans(n_clusters=ncluster,random_state=1234).fit(ccluster)
    labeles = kmeans.labels_
    df_labels = pd.DataFrame(labeles, columns=['GrupoPaleta'])
    Salida = pd.concat([cdato, df_labels], axis=1)
    return Salida


print ("inicia Generador de Paletas")
carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
Archivo ="OUT_22032022115408_FOTO_SALA_BUENA.jpg.json"


ArchivoSalida= f"{Archivo.split('.')[0]}_CONPALETA.json"


Datos = leeJSON(carpeta,Archivo)

ncluster  =5
#camposclasificadores = ["R_1","G_1","B_1","R_2","G_2","B_2","R_3","G_3","B_3"]
camposclasificadores = ["C_1_R","C_1_G","C_1_B","C_2_R","C_2_G","C_2_B","C_3_R","C_3_G","C_3_B"]
csalida =clasificador(Datos,camposclasificadores,ncluster)

#ncampo = ["id_interno","GrupoPaleta"]
#tempo = np.array(csalida[ncampo])

#print (tempo)
#print( csalida.groupby("GrupoPaleta").size().reset_index(name = "Cantidad"))

resultado = csalida.to_dict('records')

rutasalida= carpeta + ArchivoSalida

with open(rutasalida, 'w') as file:
     json.dump(resultado, file, indent = 4)

print (f"Finaliza Generador de Paletas OK\n{rutasalida}")