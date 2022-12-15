Métodos
========

.. _methods:

=====

DMoN
------------

Deep Modular Neural network es una red neuronal basada en grafos (GNN) usada en este caso para realizar clustering.

.. code-block:: python

   DMoN_areas_to_points, DMoN_clusters = DMoN_Clustering(features_X, features_position, r_max=r_max, n_clusters=n_clusters, reg=reg, dropout=dropout , num_epochs=num_epochs)

=====

GMM
------------

Gaussian Mixture Models es un método clásico de clustering para datos urbanos.

.. code-block:: python

   GMM_areas_to_points, GMM_clusters = GMM_Clustering(features_X, features_position, n_clusters=n_clusters, covariance_type=covariance_type, tol=tol, reg_covar=reg_covar)

=====

KNN
------------

K-Nearest Neighbours es un enfoque clásico para realizar clustering en general.

.. code-block:: python

   KNN_areas_to_points, KNN_clusters = KNN_Clustering(features_X, features_position, attribute=attribute, threshold=threshold, location=location, condition=condition, k=k, K=K, alfa=alfa, leafsize=leafsize)

=====

SOM
------------

Self Organized Maps.

.. code-block:: python

   SOM_areas_to_points, SOM_clusters = SOM_Clustering(features_X, features_position, som_shape=som_shape, sigma=sigma, learning_rate=learning_rate, num_iterations=num_iterations)

=====

TDI
------------

TDI corresponde a un método basado en Teoría de la Información, la cual utiliza una matriz de pesos utilizando la divergencia de Shannon como distancia entre los puntos. Luego se aplica Spectral Clustering sobre esta matriz. 

.. code-block:: python

   TDI_areas_to_points, TDI_clusters = TDI_Clustering(features_X, features_position, A=A, r=radius, k=k, leafsize=leafsize)