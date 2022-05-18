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
    kmeans = KMeans(n_clusters=ncluster).fit(ccluster)
    labeles = kmeans.labels_
    df_labels = pd.DataFrame(labeles, columns=['Grupo'])
    Salida = pd.concat([cdato, df_labels], axis=1)
    return Salida


print ("inicia Generador de Filas")
carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
Archivo ="experiencia_ms.json"


ArchivoSalida= f"{Archivo.split('.')[0]}_CONPALETA.json"


Datos = leeJSON(carpeta,Archivo)

ncluster  =4
camposclasificadores = ["R_1","G_1","B_1","R_2","G_2","B_2","R_3","G_3","B_3"]
csalida =clasificador(Datos,camposclasificadores,ncluster)
resultado = csalida.to_dict('records')

rutasalida= carpeta + ArchivoSalida

with open(rutasalida, 'w') as file:
     json.dump(resultado, file, indent = 4)

print (f"Finaliza Generador de Filas OK\n{rutasalida}")