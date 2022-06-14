import pandas as pd
import numpy as np
import json

from sklearn.cluster import KMeans
from class_Agent import Agent


class Bandejero:
    def __init__(self, parameters_):
        self.parameters = parameters_

    def execute_Task(self,taskObject_):
        return False

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

def ejecuta_1_generaFila(nombre_foto):

    #carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
    carpeta ="C:/RSILVA_REPOS/TEST_CLASIFICATOR/python/"

    print ("inicia Generador de Filas")
    #carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
    Archivo ="OUT__ELEGIDA_27012022165311_FOTO_SALA_BUENA.jpg.json"

    ArchivoSalida= f"{Archivo.split('.')[0]}_CONFILA.json"

    Datos = leeJSON(carpeta,Archivo)

    ncluster  =4
    camposclasificadores = ["y1"]
    csalida =clasificador(Datos,camposclasificadores,ncluster)
    resultado = csalida.to_dict('records')

    rutasalida= carpeta + ArchivoSalida
    print(f"resultado:{resultado}")
    with open(rutasalida, 'w') as file:
         json.dump(resultado, file, indent = 4)

    print (f"Finaliza Generador de Filas OK\n{rutasalida}")





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

def ejecuta_2_generaBandeja(nombre_foto):
    carpeta ="C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\"
    Archivo ="OUT__ELEGIDA_27012022165311_FOTO_SALA_BUENA_CONFILA.json"

    ArchivoSalida= f"{Archivo.split('.')[0]}_Y_CANTIDAD.json"

    Datos = leeJSON(carpeta,Archivo)

    CampoFila = "Fila"

    print ("inicia Generador de Filas")

    cbandejas = DefBandejas(Datos,CampoFila)
    resultado = cbandejas.to_dict('records')

    rutasalida= carpeta + ArchivoSalida
    with open(rutasalida, 'w') as file:
         json.dump(resultado, file, indent = 4)

    print (f"Finaliza Generador de bandejas OK\n{rutasalida}")


myAgent = Agent('mamífero', 7, 'Luis')


ejecuta_1_generaFila("hola.jpg")
ejecuta_2_generaBandeja("hola.jpg")

