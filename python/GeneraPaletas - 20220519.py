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


def Resumedata (_cdato) :
    #cdato es la data Generada
    CampoFila = "GrupoPaleta"
    vprom_R1 = 0
    vprom_G1 = 0
    vprom_B1 = 0
    vprom_R2 = 0
    vprom_G2 = 0
    vprom_B2 = 0
    vprom_R3 = 0
    vprom_G3 = 0
    vprom_B3 = 0

    vprom_r = []
    vprom_g = []
    vprom_b = []
 
    cdato = _cdato.groupby(CampoFila).size().reset_index(name = "Cantidad")
    #print(cdato)

    for i in cdato.index : 
        #print(cdato[CampoFila][i])
        
        ctemp = _cdato[_cdato[CampoFila] == i] 
        #print(ctemp)                   
        vprom_R1 = ctemp['C_1_R'].mean()
        vprom_G1 = ctemp['C_1_G'].mean()
        vprom_B1 = ctemp['C_1_B'].mean()
        vprom_R2 = ctemp['C_2_R'].mean()
        vprom_G2 = ctemp['C_2_G'].mean()
        vprom_B2 = ctemp['C_2_B'].mean()
        vprom_R3 = ctemp['C_3_R'].mean()
        vprom_G3 = ctemp['C_3_G'].mean()
        vprom_B3 = ctemp['C_3_B'].mean()
        
        #Agrupacion
        prom_r = (vprom_R1 + vprom_R2 + vprom_R3) / 3
        prom_g = (vprom_G1 + vprom_G2 + vprom_G3) / 3
        prom_b = (vprom_B1 + vprom_B2 + vprom_B3) / 3
        
        #print (prom_r)
        # se cargan los arreglos
        vprom_r.append(prom_r)
        vprom_g.append(prom_g)
        vprom_b.append(prom_b)

    #print(vprom_r)

    cdato['promedio_R'] = vprom_r
    cdato['promedio_G'] = vprom_g
    cdato['promedio_B'] = vprom_b
    return cdato






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

tempo3 = Resumedata(csalida)
print(tempo3)

resultado = csalida.to_dict('records')

rutasalida= carpeta + ArchivoSalida

with open(rutasalida, 'w') as file:
     json.dump(resultado, file, indent = 4)

print (f"Finaliza Generador de Paletas OK\n{rutasalida}")