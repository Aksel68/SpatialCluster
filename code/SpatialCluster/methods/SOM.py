from SpatialCluster.utils.data_format import numpy_data_format, position_data_format
from SpatialCluster.utils.get_areas import get_areas
from minisom import MiniSom  
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def SOM_Clustering(features_X, features_position, n_clusters = 4, som_shape = (3,3), sigma=0.5, learning_rate=0.5, num_iterations = 100):
    features_X = numpy_data_format(features_X)
    features_position = position_data_format(features_position)
    if(n_clusters > som_shape[0]*som_shape[1]):
        raise ValueError("n_clusters must be equal or less than the number of neurons")
    som = MiniSom(som_shape[0], som_shape[1], features_X.shape[1], sigma=sigma, learning_rate=learning_rate)
    som.train(features_X, num_iterations)
    winner_coordinates = np.array([som.winner(x) for x in features_X]).T
    neurons_points = np.ravel_multi_index(winner_coordinates, som_shape)
    points = list(zip(features_position.lon, features_position.lat))
    tensor_weights = som.get_weights()
    vector_weights = tensor_weights.reshape(som_shape[0]*som_shape[1], tensor_weights.shape[2])
    clustering = AgglomerativeClustering(n_clusters)
    aglomerative_clusters = clustering.fit_predict(vector_weights)
    clusters = [aglomerative_clusters[i] for i in neurons_points]
    areas_to_points = get_areas(clusters, points)
    return areas_to_points, clusters