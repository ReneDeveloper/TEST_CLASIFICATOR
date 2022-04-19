import pandas as pd
import numpy as np


from sklearn.datasets import make_blobs

# Preprocesado y modelado
# ==============================================================================
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.metrics import silhouette_score

#patients_df = pd.read_json('C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\test_talla_paleta.json')
patients_df = pd.read_json('C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\test_json.json')
print(patients_df.head(3))


campo1 ="y1"
campo2 = "EAN"
campos = ["y1","EAN"]

print(campo1)

#X = np.array(patients_df[["y1","EAN"]])
#X= np.array(patients_df[[campo1,campo2]])

X= np.array(patients_df[campos])

Ncluster = 4

kmeans = KMeans(n_clusters=Ncluster).fit(X)
centroids = kmeans.cluster_centers_
labeles = kmeans.labels_

df2 = pd.DataFrame(labeles, columns=['Fila'])

final = pd.concat([patients_df["id_interno"], df2], axis=1)



print(centroids)
print(kmeans)
print(labeles)
print(patients_df)
print(final)

#print(patients_df.to_string())


