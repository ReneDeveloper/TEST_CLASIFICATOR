import pandas as pd
import numpy as np


from sklearn.datasets import make_blobs

# Preprocesado y modelado
# ==============================================================================
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.metrics import silhouette_score

patients_df = pd.read_json('C:\\documentos\\2022\\Rene\\TEST_CLASIFICATOR\\python\\test_json.json')
print(patients_df.head(3))

#kmeans = KMeans(n_clusters=4) # K-Means con K=8
#kmeans.fit(patients_df.y1); 

X = np.array(patients_df[["y1"]])




kmeans = KMeans(n_clusters=4).fit(X)
centroids = kmeans.cluster_centers_
labeles = kmeans.labels_

df2 = pd.DataFrame(labeles, columns=['Fila'])

final = pd.concat([patients_df, df2], axis=1)



print(centroids)
print(kmeans)
print(labeles)
print(patients_df)
print(final)

#print(patients_df.to_string())


