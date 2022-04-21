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
    df_labels = pd.DataFrame(labeles, columns=['Fila'])
    Salida = pd.concat([cdato, df_labels], axis=1)
    return Salida

carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
Archivo ="test_json.json"
Datos = leeJSON(carpeta,Archivo)

ncluster  =4
camposclasificadores = ["y1"]
csalida =clasificador(Datos,camposclasificadores,ncluster)

js = csalida.to_json(orient='records')
print(js)
Salida="DataConFila.json"
rutasalida= carpeta + Salida

with open(rutasalida, 'w') as file:
    print(js, file=file)
    file.close()
    