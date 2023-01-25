from SpatialCluster.utils.data_format import data_format, position_data_format
from scipy import spatial
import pandas as pd
import numpy as np

def rings(features_X, features_position, criteria="k", max_radios=[200.0, 300.0, 400.0], max_neighbours=[200, 500, 1000], weight_mode="Simple", keep_original_value=True, smoothing=1e-08, normalize=True, leafsize=10):

    """
    El algoritmo toma todos los puntos dentro de un radio máximo.
    Luego, toma los K vecinos más cercanos a cada pundo donde K
    está definido según "max_neighbors_per_radio".
    """
    original_radios = max_radios
    meter_to_degree_equivalence = 9.090909091e-6
    max_radios = np.array(max_radios)*meter_to_degree_equivalence # Se transforma de metros a grados
    features_X = data_format(features_X)
    features_position = position_data_format(features_position)
    # Verificar que ambas listas sean de largo igual
    assert len(max_radios) == len(max_neighbours)

    points = np.array(list(zip(features_position.lon, features_position.lat)))
    tree = spatial.KDTree(data=points, leafsize=leafsize)
    final_features_df = pd.DataFrame()

    if keep_original_value:
        final_features_df = features_X.copy()
    len_features = len(features_X.columns)
    if(criteria == "k"):
        for _, k in enumerate(max_neighbours):
            features_array = [ [] for _ in range(len_features)]
            k_neighbours = tree.query(points, k = k)[1] # k vecinos
            for _, neighbourhood in enumerate(k_neighbours):
                for f_index, feature in enumerate(features_X.columns):
                    subset_feature = features_X.iloc[neighbourhood][feature]
                    mean_feature = subset_feature.mean()
                    features_array[f_index].append(mean_feature) 
            for f_index, feature in enumerate(features_X.columns):
                final_features_df[f"{feature}_{k}nb"] = features_array[f_index] # indico cuantos vecinos en el nombre del attributo
        features_X = final_features_df
    elif(criteria == "r"):
        for i, r in enumerate(max_radios):
            features_array = [ [] for _ in range(len_features)]
            nearest_neighbours = tree.query_ball_tree(tree, r) # vecinos dentro de radio r
            for _, neighbourhood in enumerate(nearest_neighbours):
                for f_index, feature in enumerate(features_X.columns):
                    subset_feature = features_X.iloc[neighbourhood][feature]
                    mean_feature = subset_feature.mean()
                    features_array[f_index].append(mean_feature) 
            for f_index, feature in enumerate(features_X.columns):
                final_features_df[f"{feature}_{original_radios[i]}m"] = features_array[f_index]
        features_X = final_features_df
    elif(criteria == "rk"):
        for i, r in enumerate(max_radios):
            features_array = [ [] for _ in range(len_features)]
            k = max_neighbours[i]
            nearest_neighbours = tree.query_ball_tree(tree, r)
            for j, neighbourhood in enumerate(nearest_neighbours): # Para cada punto
                neighbourhood = np.array(neighbourhood) # Saco los vecinos dentro del radio r
                temporal_tree = spatial.KDTree(data=points[neighbourhood], leafsize=leafsize)
                k_length = min(k, len(neighbourhood)) # Conseguir los K puntos más cercanos dentro de ese radio
                distances, nearby_points = temporal_tree.query(points[j], k = k_length)
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
                final_features_df[f"{feature}_{original_radios[i]}m{k}nb"] = features_array[f_index]
        features_X = final_features_df
    return features_X