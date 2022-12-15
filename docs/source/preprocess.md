Preprocesamiento
====================

.. _installation:

=====

Dar formato a tabla
--------------------

Para obtener los datos separados en variables con el formato que utilizan los métodos de la librería se ofrecen dos funciones distintas.

La primera corresponde a *attributes_format* que entrega *(features_position, features_X)* donde *features_position* corresponde a un dataframe con la longitud y latitud de los datos y *features_X* que corresponde a los atributos de los datos.


{py:func}`SpatialCluster.datasets.load_manzana_data`

```{eval-rst}
   autofunction:: SpatialCluster.datasets.load_manzana_data
```

```{eval-rst}
.. code-block:: python

   features_position, features_X = attributes_format(df)

```

La segunda corresponde a *attributes_with_zone_format* que entrega *(features_position, features_X)* donde *features_position* corresponde a un dataframe con la longitud y latitud de los datos y *features_X* que corresponde a los atributos de los datos con una columna extra que indica a qué zona pertenece el punto (en el dataset de ejemplo corresponde a la comuna).

.. code-block:: python

   features_position, features_X = attributes_with_zone_format(df)

=====

Matriz de adyacencia
---------------------

Para crear la matriz de adyacencia se pueden usar los siguientes criterios:

Por k vecinos más cercanos.

Por vecinos dentro de un radio r.

Por vecinos dentro de un radio r, con un mínimo de k_min vecinos, en caso de que haya menos que ese umbral se usarán k vecinos.

.. code-block:: python

   A = adjacencyMatrix(features_position, r=radius, k=k, min_k=min_k, criteria=criteria, leafsize=leafsize)

=====

Anillos
------------

Para crear los anillos se pueden usar los siguientes criterios:

Por k vecinos más cercanos.

Por vecinos dentro de un radio r.

Por vecinos dentro de un radio r, con un mínimo de k_min vecinos, en caso de que haya menos que ese umbral se usarán k vecinos.

.. code-block:: python

   features_X1 = rings(features_X, features_position, criteria=criteria, max_radios=max_radios, max_neighbours=max_neighbours, weight_mode=weight_mode, keep_original_value=keep_original_value, smoothing=smoothing, normalize=normalize, leafsize=leafsize)


