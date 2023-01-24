from SpatialCluster.utils.data_format import data_format, position_data_format
from SpatialCluster.utils.get_areas import get_areas
from sklearn.mixture import GaussianMixture

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

def GMM_Clustering(features_X, features_position, n_clusters = 4, covariance_type = "full", tol=1e-3, reg_covar=1e-6):
    features_X = data_format(features_X)
    features_position = position_data_format(features_position)
    points = list(zip(features_position.lon, features_position.lat))
    gmm = GaussianMixture(n_components=n_clusters, covariance_type=covariance_type, tol=tol, reg_covar=reg_covar).fit(features_X)
    clusters = gmm.predict(features_X)

    areas_to_points = get_areas(clusters, points)

    return areas_to_points, clusters