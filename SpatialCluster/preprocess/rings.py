import numpy as np
import pandas as pd
from scipy import spatial
from SpatialCluster.utils.data_format import data_format, position_data_format

def rings(features_X, features_position, max_radio=[0.00014, 0.00024, 0.00034], max_neighbors_per_radio=[200, 500, 1000], keep_original_value=True, smoothing=1e-08, normalize=True, leafsize=10):

    """
    El algoritmo toma todos los puntos dentro de un radio máximo.
    Luego, toma los K vecinos más cercanos a cada pundo donde K
    está definido según "max_neighbors_per_radio".
    """
    features_X = data_format(features_X)
    features_position = position_data_format(features_position)
    # Verificar que ambas listas sean de largo igual
    assert len(max_radio) == len(max_neighbors_per_radio)

    pts = np.array(list(zip(features_position.lon, features_position.lat)))
    tree = spatial.cKDTree(data=pts, leafsize=leafsize)
    final_features_df = pd.DataFrame()
    
    if keep_original_value:
        final_features_df = features_X.copy()

    for i in range(len(max_radio)):
        print(f'Looking for the nearest neighbors. Radio: {max_radio[i]}')
        k = max_neighbors_per_radio[i]
        ball_points = tree.query_ball_point(pts, max_radio[i])
        features_array = [ [] for _ in range(len(features_X.columns)) ]

        for point in range(len(ball_points)):               # Para cada punto
            idxs = np.array(ball_points[point])                 # Solo consigo puntos con cierto radio
            temporal_tree = spatial.cKDTree(data=pts[idxs], leafsize=leafsize)
            k_length = min(k, len(idxs))            # Conseguir los K puntos más cercanos dentro de ese radio
            distances, nearby_points = temporal_tree.query(pts[point], k = k_length)
            distances += smoothing
            if(normalize):
                distances = distances/np.linalg.norm(distances)
            
            indexs = idxs[nearby_points]

            for f_index, feature in enumerate(features_X.columns):
                subset_feature = features_X.loc[indexs, :][feature]/distances
                mean_feature = subset_feature.mean()
                features_array[f_index].append(mean_feature) 
        
        for f_index, feature in enumerate(features_X.columns):
            final_features_df[f"{feature}_{i}"] = features_array[f_index]
        
    features_X = final_features_df
    return features_X


"""
Revisar promedio de vecinos para los anillos
Decidir si usar metros o no (ahora está en grados ?)

"""