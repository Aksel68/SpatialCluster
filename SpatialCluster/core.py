from DMoN import IncrementalCOOMatrix, convert_scipy_sparse_to_sparse_tensor, build_dmon, normalize_graph

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import numpy as np
from scipy import spatial
import random
import tensorflow.compat.v2 as tf
import matplotlib.pyplot as plt
import matplotlib.colors as cl


import folium
from folium import Map

from SpatialCluster.constants import COLORS

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def get_areas(clusters, points):
    num_points = len(points)
    areas_to_points = dict()
    for i in range(0,num_points):
        area = int(clusters[i])
        # print(type(area))
        if area in areas_to_points:
            areas_to_points[area].append(points[i])
        else:
            areas_to_points[area] = [points[i]]

    return areas_to_points


"""
----------------
Parameters:

features_X:         (DataFrame) Table with the features of each point
features_position:  (DataFrame) Table with the position of each point (lon, lat)
r_max:              (float) Max ratio to search for neighbours
n_clusters:         (int) Number of clusters
reg:                (int) Collapse regularization
dropout:            (float) Dropout rate for the model
num_epochs:         (int) Number of epochs to train the model

----------------
Return:

areas_to_points:    (dict) Dictionary with the cluster id as keys and a list of points in as values

"""

def DMoN_Clustering(features_X, features_position, r_max = 0.00034, n_clusters = 4, reg = 1, dropout = 0.0, num_epochs = 500):
    X = features_X.to_numpy(dtype=float)
    x_min, x_max = np.min(X, axis=0), np.max(X, axis=0)
    X = (X - x_min)/(x_max - x_min)
    X = np.asmatrix(X) # feature matrix

    # --------------------------------------------------------------------------
    
    data = list(zip(features_position.lon, features_position.lat))
    tree = spatial.KDTree(data = data, leafsize = 10)
    points = list(zip(features_position.lon, features_position.lat))
    answers = tree.query(points, k = 2)[1]

    # --------------------------------------------------------------------------

    shape = len(points), len(points)
    mat = IncrementalCOOMatrix(shape, np.int64)

    ball_points = tree.query_ball_point(points, r_max)

    for x in range(len(ball_points)):
        idxs = list(ball_points[x])
        if len(idxs) < 2:
            idxs = list(answers[x])
        for y in idxs:
            mat.append(x, y, 1)

    A = mat.tocoo() # adjacency matrix
    A = A.tocsr()
    n_nodes = A.shape[0]
    feature_size = X.shape[1]

    # --------------------------------------------------------------------------

    graph = convert_scipy_sparse_to_sparse_tensor(A)
    graph_normalized = convert_scipy_sparse_to_sparse_tensor(normalize_graph(A.copy()))
    input_features = tf.keras.layers.Input(shape=(feature_size,))
    input_graph = tf.keras.layers.Input((n_nodes,), sparse=True)
    input_adjacency = tf.keras.layers.Input((n_nodes,), sparse=True)

    model = build_dmon(input_features, input_graph, input_adjacency, n_clusters, reg, dropout)

    # Computes the gradients wrt. the sum of losses, returns a list of them.
    def grad(model, inputs):
        with tf.GradientTape() as tape:
            _ = model(inputs, training=True)
            loss_value = sum(model.losses)
        return model.losses, tape.gradient(loss_value, model.trainable_variables)

    optimizer = tf.keras.optimizers.Adam(0.001)
    model.compile(optimizer, None)

    # --------------------------------------------------------------------------

    for epoch in range(num_epochs):
        loss_values, grads = grad(model, [X, graph_normalized, graph])
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

    # --------------------------------------------------------------------------

    _, assignments = model([X, graph_normalized, graph], training=False)
    assignments = assignments.numpy()
    clusters = assignments.argmax(axis=1) 

    areas_to_points = get_areas(clusters, points)

    return areas_to_points, clusters


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def visualize_map_sample(areas_to_points, clusters, min_supp, features, max_samples_per_clusters):
    COLORS_9_SET = [plt.cm.Set1(i) for i in range(10)]
    COLORS_9_SET = [cl.to_hex(c) for c in COLORS_9_SET]

    hmap = Map(location=[-33.45, -70.65], control_scale=True, zoom_start=11, tiles = 'stamen toner')
    if len([x for x in areas_to_points.items() if len(x[1]) > min_supp]) <= 9:
        colors_to_use = COLORS_9_SET
    else:
        colors_to_use = COLORS
    sorted_points = {k: v for k, v in sorted(areas_to_points.items(), key=lambda item: len(item[1]), reverse=True)}
    
    for index, i in enumerate(sorted_points):
        if len(sorted_points[i]) <= min_supp:
            continue
        
        a_ = random.sample(sorted_points[i], min(len(sorted_points[i]), max_samples_per_clusters) )
        for point in a_:
            folium.Circle(location=[point[1], point[0]], popup = str(point),
                            color=colors_to_use[index], radius=10).add_to(hmap)
            
    return hmap