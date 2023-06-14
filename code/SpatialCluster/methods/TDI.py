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

def TDI_Clustering(features_X, features_position, n_clusters = 4, A = None, k = 20, leafsize = 10):
    features_X = numpy_data_format(features_X)
    features_position = position_data_format(features_position)
    scaler = MinMaxScaler()
    new_features = pd.DataFrame(scaler.fit_transform(features_X))
    criteria = "k"
    r = 300.0
    directed = False
    if(A == None):
        A = adjacencyMatrix(features_position, r=r, k=k, criteria=criteria, directed=directed, leafsize=leafsize)
    mat = IncrementalCOOMatrix(A.shape, np.float64)
    rows, cols, _ = sp.sparse.find(A)
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
        mat.append(v2_pos, v1_pos, dist)
    mat = mat.tocoo() # weight matrix
    mat = mat.tocsr()
    clusters = spectral_clustering(mat, n_clusters = n_clusters)
    points = list(zip(features_position.lon, features_position.lat))
    areas_to_points = get_areas(clusters, points)
    return areas_to_points, clusters