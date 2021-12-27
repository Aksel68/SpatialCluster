from sklearn.mixture import GaussianMixture
from SpatialCluster.methods.functions import get_areas


"""
----------------
Parameters:

features_X:         (DataFrame) Table with the features of each point
features_position:  (DataFrame) Table with the position of each point (lon, lat)
n_components:       (int) Number of mixture components

----------------
Return:

areas_to_points:    (dict) Dictionary with the cluster id as keys and a list of points in as values

"""

def GMM_Clustering(features_X, features_position, n_components = 2):
    points = list(zip(features_position.lon, features_position.lat))
    gmm = GaussianMixture(n_components).fit(features_X)
    clusters = gmm.predict(features_X)

    areas_to_points = get_areas(clusters, points)

    return areas_to_points, clusters