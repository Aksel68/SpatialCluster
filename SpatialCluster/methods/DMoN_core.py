from sklearn.metrics import cluster
import tensorflow.compat.v2 as tf
import scipy as sp
import numpy as np
import array


class DMoN(tf.keras.layers.Layer):
    """Implementation of Deep Modularity Network (DMoN) layer.
    Deep Modularity Network (DMoN) layer implementation as presented in
    "Graph Clustering with Graph Neural Networks" in a form of TF 2.0 Keras layer.
    DMoN optimizes modularity clustering objective in a fully unsupervised mode,
    however, this implementation can also be used as a regularizer in a supervised
    graph neural network. Optionally, it does graph unpooling.
    Attributes:
        n_clusters: Number of clusters in the model.
        collapse_regularization: Collapse regularization weight.
        dropout_rate: Dropout rate. Note that the dropout in applied to the
        intermediate representations before the softmax.
        do_unpooling: Parameter controlling whether to perform unpooling of the
        features with respect to their soft clusters. If true, shape of the input
        is preserved.
    """

    def __init__(self,
                n_clusters,
                collapse_regularization = 0.1,
                dropout_rate = 0,
                do_unpooling = False):
        """Initializes the layer with specified parameters."""
        super(DMoN, self).__init__()
        self.n_clusters = n_clusters
        self.collapse_regularization = collapse_regularization
        self.dropout_rate = dropout_rate
        self.do_unpooling = do_unpooling
        

    def build(self, input_shape):
        """Builds the Keras model according to the input shape."""
        self.transform = tf.keras.models.Sequential([
            tf.keras.layers.Dense(
                self.n_clusters,
                kernel_initializer='orthogonal',
                bias_initializer='zeros'),
            tf.keras.layers.Dropout(self.dropout_rate)
        ])
        super(DMoN, self).build(input_shape)

    def call(
        self, inputs):
        """Performs DMoN clustering according to input features and input graph.
        Args:
        inputs: A tuple of Tensorflow tensors. First element is (n*d) node feature
            matrix and the second one is (n*n) sparse graph adjacency matrix.
        Returns:
        A tuple (features, clusters) with (k*d) cluster representations and
        (n*k) cluster assignment matrix, where k is the number of cluster,
        d is the dimensionality of the input, and n is the number of nodes in the
        input graph. If do_unpooling is True, returns (n*d) node representations
        instead of cluster representations.
        """
        features, adjacency = inputs

        assert isinstance(features, tf.Tensor)
        assert isinstance(adjacency, tf.SparseTensor)
        assert len(features.shape) == 2
        assert len(adjacency.shape) == 2
        assert features.shape[0] == adjacency.shape[0]

        assignments = tf.nn.softmax(self.transform(features), axis=1)
        cluster_sizes = tf.math.reduce_sum(assignments, axis=0)  # Size [k].
        assignments_pooling = assignments / cluster_sizes  # Size [n, k].

        degrees = tf.sparse.reduce_sum(adjacency, axis=0)  # Size [n].
        degrees = tf.reshape(degrees, (-1, 1))

        number_of_nodes = adjacency.shape[1]
        number_of_edges = tf.math.reduce_sum(degrees)

        # Computes the size [k, k] pooled graph as S^T*A*S in two multiplications.
        graph_pooled = tf.transpose(
            tf.sparse.sparse_dense_matmul(adjacency, assignments))
        graph_pooled = tf.matmul(graph_pooled, assignments)

        # We compute the rank-1 normalizer matrix S^T*d*d^T*S efficiently
        # in three matrix multiplications by first processing the left part S^T*d
        # and then multyplying it by the right part d^T*S.
        # Left part is [k, 1] tensor.
        normalizer_left = tf.matmul(assignments, degrees, transpose_a=True)
        # Right part is [1, k] tensor.
        normalizer_right = tf.matmul(degrees, assignments, transpose_a=True)

        # Normalizer is rank-1 correction for degree distribution for degrees of the
        # nodes in the original graph, casted to the pooled graph.
        normalizer = tf.matmul(normalizer_left,
                            normalizer_right) / 2 / number_of_edges
        spectral_loss = -tf.linalg.trace(graph_pooled -
                                        normalizer) / 2 / number_of_edges
        self.add_loss(spectral_loss)

        collapse_loss = tf.norm(cluster_sizes) / number_of_nodes * tf.sqrt(
            float(self.n_clusters)) - 1
        self.add_loss(self.collapse_regularization * collapse_loss)

        features_pooled = tf.matmul(assignments_pooling, features, transpose_a=True)
        features_pooled = tf.nn.selu(features_pooled)
        if self.do_unpooling:
            features_pooled = tf.matmul(assignments_pooling, features_pooled)
        return features_pooled, assignments

# -----------------------------------------------------------------------------

class GCN(tf.keras.layers.Layer):
    """Implementation of Graph Convolutional Network (GCN) layer.
    Attributes:
        n_channels: Output dimensionality of the layer.
        skip_connection: If True, node features are propagated without neighborhood
        aggregation.
        activation: Activation function to use for the final representations.
    """

    def __init__(self,
                n_channels,
                activation='selu',
                skip_connection = True):
        """Initializes the layer with specified parameters."""
        super(GCN, self).__init__()
        self.n_channels = n_channels
        self.skip_connection = skip_connection
        if isinstance(activation, str):
            self.activation = tf.keras.layers.Activation(activation)
        elif isinstance(tf.keras.layers.Activation):
            self.activation = activation
        elif activation is None:
            self.activation = tf.keras.layers.Lambda(lambda x: x)
        else:
            raise ValueError('GCN activation of unknown type')

    def build(self, input_shape):
        """Builds the Keras model according to the input shape."""
        self.n_features = input_shape[0][-1]
        self.kernel = self.add_weight(
            'kernel', shape=(self.n_features, self.n_channels))
        self.bias = self.add_weight('bias', shape=(self.n_channels,))
        if self.skip_connection:
            self.skip_weight = self.add_weight(
                'skip_weight', shape=(self.n_channels,))
        else:
            self.skip_weight = 0
        super().build(input_shape)

    def call(self, inputs):
        """Computes GCN representations according to input features and input graph.
        Args:
        inputs: A tuple of Tensorflow tensors. First element is (n*d) node feature
            matrix and the second is normalized (n*n) sparse graph adjacency matrix.
        Returns:
        An (n*n_channels) node representation matrix.
        """
        features, norm_adjacency = inputs

        assert isinstance(features, tf.Tensor)
        assert isinstance(norm_adjacency, tf.SparseTensor)
        assert len(features.shape) == 2
        assert len(norm_adjacency.shape) == 2
        assert features.shape[0] == norm_adjacency.shape[0]

        output = tf.matmul(features, self.kernel)
        if self.skip_connection:
            output = output * self.skip_weight + tf.sparse.sparse_dense_matmul(
                norm_adjacency, output)
        else:
            output = tf.sparse.sparse_dense_matmul(norm_adjacency, output)
        output = output + self.bias
        return self.activation(output)

# -----------------------------------------------------------------------------



def pairwise_precision(y_true, y_pred):
    """Computes pairwise precision of two clusterings.
    Args:
        y_true: An [n] int ground-truth cluster vector.
        y_pred: An [n] int predicted cluster vector.
    Returns:
        Precision value computed from the true/false positives and negatives.
    """
    true_positives, false_positives, _, _ = _pairwise_confusion(y_true, y_pred)
    return true_positives / (true_positives + false_positives)


def pairwise_recall(y_true, y_pred):
    """Computes pairwise recall of two clusterings.
    Args:
        y_true: An (n,) int ground-truth cluster vector.
        y_pred: An (n,) int predicted cluster vector.
    Returns:
        Recall value computed from the true/false positives and negatives.
    """
    true_positives, _, false_negatives, _ = _pairwise_confusion(y_true, y_pred)
    return true_positives / (true_positives + false_negatives)


def pairwise_accuracy(y_true, y_pred):
    """Computes pairwise accuracy of two clusterings.
    Args:
        y_true: An (n,) int ground-truth cluster vector.
        y_pred: An (n,) int predicted cluster vector.
    Returns:
        Accuracy value computed from the true/false positives and negatives.
    """
    true_pos, false_pos, false_neg, true_neg = _pairwise_confusion(y_true, y_pred)
    return (true_pos + false_pos) / (true_pos + false_pos + false_neg + true_neg)


def _pairwise_confusion(
    y_true,
    y_pred):
    """Computes pairwise confusion matrix of two clusterings.
    Args:
        y_true: An (n,) int ground-truth cluster vector.
        y_pred: An (n,) int predicted cluster vector.
    Returns:
        True positive, false positive, true negative, and false negative values.
    """
    contingency = cluster.contingency_matrix(y_true, y_pred)
    same_class_true = np.max(contingency, 1)
    same_class_pred = np.max(contingency, 0)
    diff_class_true = contingency.sum(axis=1) - same_class_true
    diff_class_pred = contingency.sum(axis=0) - same_class_pred
    total = contingency.sum()

    true_positives = (same_class_true * (same_class_true - 1)).sum()
    false_positives = (diff_class_true * same_class_true * 2).sum()
    false_negatives = (diff_class_pred * same_class_pred * 2).sum()
    true_negatives = total * (
        total - 1) - true_positives - false_positives - false_negatives

    return true_positives, false_positives, false_negatives, true_negatives


def modularity(adjacency, clusters):
    """Computes graph modularity.
    Args:
        adjacency: Input graph in terms of its sparse adjacency matrix.
        clusters: An (n,) int cluster vector.
    Returns:
        The value of graph modularity.
        https://en.wikipedia.org/wiki/Modularity_(networks)
    """
    degrees = adjacency.sum(axis=0).A1
    n_edges = degrees.sum()  # Note that it's actually 2*n_edges.
    result = 0
    for cluster_id in np.unique(clusters):
        cluster_indices = np.where(clusters == cluster_id)[0]
        adj_submatrix = adjacency[cluster_indices, :][:, cluster_indices]
        degrees_submatrix = degrees[cluster_indices]
        result += np.sum(adj_submatrix) - (np.sum(degrees_submatrix)**2) / n_edges
    return result / n_edges


def conductance(adjacency, clusters):
    """Computes graph conductance as in Yang & Leskovec (2012).
    Args:
        adjacency: Input graph in terms of its sparse adjacency matrix.
        clusters: An (n,) int cluster vector.
    Returns:
        The average conductance value of the graph clusters.
    """
    inter = 0  # Number of inter-cluster edges.
    intra = 0  # Number of intra-cluster edges.
    cluster_indices = np.zeros(adjacency.shape[0], dtype=np.bool)
    for cluster_id in np.unique(clusters):
        cluster_indices[:] = 0
        cluster_indices[np.where(clusters == cluster_id)[0]] = 1
        adj_submatrix = adjacency[cluster_indices, :]
        inter += np.sum(adj_submatrix[:, cluster_indices])
        intra += np.sum(adj_submatrix[:, ~cluster_indices])
    return intra / (inter + intra)

  # -----------------------------------------------------------------------------

def normalize_graph(graph,
                    normalized = True,
                    add_self_loops = True):
    """Normalized the graph's adjacency matrix in the scipy sparse matrix format.
    Args:
        graph: A scipy sparse adjacency matrix of the input graph.
        normalized: If True, uses the normalized Laplacian formulation. Otherwise,
        use the unnormalized Laplacian construction.
        add_self_loops: If True, adds a one-diagonal corresponding to self-loops in
        the graph.
    Returns:
        A scipy sparse matrix containing the normalized version of the input graph.
    """
    if add_self_loops:
        graph = graph + sp.sparse.identity(graph.shape[0])
    degree = np.squeeze(np.asarray(graph.sum(axis=1)))
    if normalized:
        with np.errstate(divide='ignore'):
            inverse_sqrt_degree = 1. / np.sqrt(degree)
        inverse_sqrt_degree[inverse_sqrt_degree == np.inf] = 0
        inverse_sqrt_degree = sp.sparse.diags(inverse_sqrt_degree)
        return inverse_sqrt_degree @ graph @ inverse_sqrt_degree
    else:
        with np.errstate(divide='ignore'):
            inverse_degree = 1. / degree
        inverse_degree[inverse_degree == np.inf] = 0
        inverse_degree = sp.sparse.diags(inverse_degree)
        return inverse_degree @ graph

# -----------------------------------------------------------------------------

def load_npz(
    filename
):
    """Loads an attributed graph with sparse features from a specified Numpy file.
    Args:
        filename: A valid file name of a numpy file containing the input data.
    Returns:
        A tuple (graph, features, labels, label_indices) with the sparse adjacency
        matrix of a graph, sparse feature matrix, dense label array, and dense label
        index array (indices of nodes that have the labels in the label array).
    """
    with np.load(open(filename, 'rb'), allow_pickle=True) as loader:
        loader = dict(loader)
        adjacency = sp.sparse.csr_matrix(
            (loader['adj_data'], loader['adj_indices'], loader['adj_indptr']),
            shape=loader['adj_shape'])

        features = sp.sparse.csr_matrix(
            (loader['feature_data'], loader['feature_indices'],
            loader['feature_indptr']),
            shape=loader['feature_shape'])

        label_indices = loader['label_indices']
        labels = loader['labels']
    assert adjacency.shape[0] == features.shape[
        0], 'Adjacency and feature size must be equal!'
    assert labels.shape[0] == label_indices.shape[
        0], 'Labels and label_indices size must be equal!'
    return adjacency, features, labels, label_indices

# -----------------------------------------------------------------------------

def convert_scipy_sparse_to_sparse_tensor(
    matrix):
    """Converts a sparse matrix and converts it to Tensorflow SparseTensor.
    Args:
        matrix: A scipy sparse matrix.
    Returns:
        A ternsorflow sparse matrix (rank-2 tensor).
    """
    matrix = matrix.tocoo()
    return tf.sparse.SparseTensor(
        np.vstack([matrix.row, matrix.col]).T, matrix.data.astype(np.float32),
        matrix.shape)

# -----------------------------------------------------------------------------

def build_dmon(input_features,
               input_graph,
               input_adjacency,
               n_clusters,
               reg,
               dropout,
              ):
    """Builds a Deep Modularity Network (DMoN) model from the Keras inputs.
    Args:
        input_features: A dense [n, d] Keras input for the node features.
        input_graph: A sparse [n, n] Keras input for the normalized graph.
        input_adjacency: A sparse [n, n] Keras input for the graph adjacency.
    Returns:
        Built Keras DMoN model.
    """
    output = input_features
    for n_channels in [64]: # architecture
        output = GCN(n_channels)([output, input_graph])
    pool, pool_assignment = DMoN(n_clusters, collapse_regularization=reg, dropout_rate=dropout)([output, input_adjacency])
    return tf.keras.Model(
        inputs=[input_features, input_graph, input_adjacency],
        outputs=[pool, pool_assignment])

# -----------------------------------------------------------------------------