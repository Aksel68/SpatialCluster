from SpatialCluster.utils.data_format import numpy_data_format, position_data_format
from SpatialCluster.utils.data_structures  import IncrementalCOOMatrix
from SpatialCluster.preprocess import adjacencyMatrix
from SpatialCluster.utils.get_areas import get_areas
from scipy.spatial.distance import jensenshannon
from sklearn.cluster import spectral_clustering
from sklearn.preprocessing import MinMaxScaler 
import pandas as pd
import numpy as np
import scipy as sp

import time

def TDI_Clustering(features_X, features_position, A = None, r=300, k=5, leafsize=10):
    a = time.time()
    features_X = numpy_data_format(features_X)
    features_position = position_data_format(features_position)
    scaler = MinMaxScaler()
    new_features = pd.DataFrame(scaler.fit_transform(features_X))
    criteria = "k"
    directed = False
    if(A == None):
        A = adjacencyMatrix(features_position, r=r, k=k, criteria=criteria, directed=directed, leafsize=leafsize)
    mat = IncrementalCOOMatrix(A.shape, np.float64)
    rows, cols, values = sp.sparse.find(A)
    b = time.time()
    print("First Part:", b-a)
    c = time.time()
    for i in range(rows.shape[0]):
        v1_pos = rows[i]
        v2_pos = cols[i]
        if(v2_pos > v1_pos):
            continue
        vec1 = np.array(new_features.loc[v1_pos])
        vec2 = np.array(new_features.loc[v2_pos])
        dist = jensenshannon(vec1, vec2)
        if np.isnan(dist):
            dist = 0
        mat.append(v1_pos, v2_pos, dist)
    d = time.time()
    print("Matriz de pesos:", d-c)
    e = time.time()
    mat = mat.tocoo() # weight matrix
    mat = mat.tocsr()
    f = time.time()
    print("Transformar matriz:", f-e)
    g = time.time()
    clusters = spectral_clustering(mat)
    h = time.time()
    print("Spectral clustering:", h-g)
    i = time.time()
    points = list(zip(features_position.lon, features_position.lat))
    areas_to_points = get_areas(clusters, points)
    j = time.time()
    print("Areas to points:", j-i)
    return areas_to_points, clusters