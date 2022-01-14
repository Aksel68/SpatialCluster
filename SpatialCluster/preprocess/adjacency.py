from SpatialCluster.methods.DMoN_core import IncrementalCOOMatrix
from SpatialCluster.utils.data_format import position_data_format
from scipy import spatial
import numpy as np

def adjacencyMatrix(features_position, r_max = 0.00034, leafsize = 10, k = 2):
    features_position = position_data_format(features_position)
    points = list(zip(features_position.lon, features_position.lat))

    # --------------------------------------------------------------------------

    shape = len(points), len(points)
    mat = IncrementalCOOMatrix(shape, np.int64)

    data = list(zip(features_position.lon, features_position.lat))
    tree = spatial.KDTree(data = data, leafsize = leafsize)
    ball_points = tree.query_ball_point(points, r_max)
    answers = tree.query(points, k = k)[1]

    for x in range(len(ball_points)):
        idxs = list(ball_points[x])
        if len(idxs) < 2:
            idxs = list(answers[x])
        for y in idxs:
            mat.append(x, y, 1)

    A = mat.tocoo() # adjacency matrix
    A = A.tocsr()

    return A
