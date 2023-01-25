from SpatialCluster.methods.DMoN_core import convert_scipy_sparse_to_sparse_tensor, build_dmon, normalize_graph
from SpatialCluster.utils.data_format import data_format, position_data_format
from SpatialCluster.preprocess import adjacencyMatrix
from SpatialCluster.utils.get_areas import get_areas
import tensorflow.compat.v2 as tf
import numpy as np


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

def DMoN_Clustering(features_X, features_position, A = None, criteria = "k", r_max = 300.0, n_clusters = 4, reg = 1.0, dropout = 0.0, num_epochs = 500, learning_rate = 0.001):
    features_X = data_format(features_X)
    features_position = position_data_format(features_position)
    X = features_X.to_numpy(dtype=float)
    x_min, x_max = np.min(X, axis=0), np.max(X, axis=0)
    try:
        X = (X - x_min)/(x_max - x_min)
    except RuntimeWarning:
        X = (X - x_min)/(x_max - x_min)
        print("--------------------Debug------------------------")
        print(f"X:{X}\nx_min:{x_min}\nx_max:{x_max}")
    X = np.asmatrix(X) # feature matrix

    # --------------------------------------------------------------------------
    points = list(zip(features_position.lon, features_position.lat))
    if(A == None):
        A = adjacencyMatrix(features_position, criteria=criteria, r=r_max)
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

    optimizer = tf.keras.optimizers.Adam(learning_rate)
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
