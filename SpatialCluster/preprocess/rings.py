import numpy as np
import pandas as pd
from scipy import spatial
from SpatialCluster.utils.data_format import data_format, position_data_format

def rings(features_X, features_position, max_radio=[200, 300, 400], max_neighbors_per_radio=[200, 500, 1000], weight_mode="Simple", keep_original_value=True, smoothing=1e-08, normalize=True, leafsize=10):

    """
    El algoritmo toma todos los puntos dentro de un radio máximo.
    Luego, toma los K vecinos más cercanos a cada pundo donde K
    está definido según "max_neighbors_per_radio".
    """
    meter_to_degree_equivalence = 9.090909091e-6
    max_radio = np.array(max_radio)*meter_to_degree_equivalence # Se transforma de metros a grados
    features_X = data_format(features_X)
    features_position = position_data_format(features_position)
    # Verificar que ambas listas sean de largo igual
    assert len(max_radio) == len(max_neighbors_per_radio)

    pts = np.array(list(zip(features_position.lon, features_position.lat)))
    tree = spatial.KDTree(data=pts, leafsize=leafsize)
    final_features_df = pd.DataFrame()

    if keep_original_value:
        final_features_df = features_X.copy()
    len_features = len(features_X.columns)
    for i, r in enumerate(max_radio):
        k = max_neighbors_per_radio[i]
        nearest_neighbours = tree.query_ball_tree(tree, r)
        features_array = [ [] for _ in range(len_features)]
        for j, neighbourhood in enumerate(nearest_neighbours): # Para cada punto
            neighbourhood = np.array(neighbourhood) # Saco los vecinos dentro del radio r
            temporal_tree = spatial.KDTree(data=pts[neighbourhood], leafsize=leafsize)
            k_length = min(k, len(neighbourhood)) # Conseguir los K puntos más cercanos dentro de ese radio
            distances, nearby_points = temporal_tree.query(pts[j], k = k_length)
            distances += smoothing # Tal vez simplemente eliminar el primer elemento que es el punto mismo
            if(normalize):
                distances = distances/np.linalg.norm(distances)
            indexs = neighbourhood[nearby_points]
            for f_index, feature in enumerate(features_X.columns):
                if weight_mode == "Simple":
                    subset_feature = features_X.iloc[indexs][feature]
                elif weight_mode == "Distance Inverse":
                    subset_feature = features_X.iloc[indexs][feature]/distances
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