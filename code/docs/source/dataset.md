Dataset
=======

.. _dataset:

Origen
--------------

El dataset contiene distintas características, las cuales fueron agrupadas en 3 categorías: Visuales, Sociales, Suelo.

=====

Características Visuales
-------------------------

Estas características fueron obtenidas a partir de fotografías del lugar físico correspondiente, las cuales fueron procesadas por una red neuronal que entregaba las siguientes características:

    - Feature 1
    - Feature 2
    - Feature 3
    - Feature 4
    - Feature 5
    - Feature 6
    - Feature 7

=====

Características Sociales
-------------------------

Estas características fueron obtenidas desde el sitio web oficial del Servicio Electoral de Chile (Servel). De este se obtuvieron las siguientes características:

    - Feature 1
    - Feature 2
    - Feature 3
    - Feature 4
    - Feature 5
    - Feature 6
    - Feature 7

=====

Características de Suelo
-------------------------

Estas características fueron obtenidas a partir del valuo fiscal obtenido del sitio web oficial del Servicio de Impuestos Internos de Chile (SII). De este se obtuvieron las siguientes características:

    - Feature 1
    - Feature 2
    - Feature 3
    - Feature 4
    - Feature 5
    - Feature 6
    - Feature 7

=====

Uso 
------------

Para tener acceso al dataset basta con usar la siguiente función:

.. code-block:: python

   from SpatialCluster.datasets import load_manzana_data
   df = load_manzana_data()


Luego dependiendo del método que se quiera usar, se puede dar el formato correspondiente con las siguientes funciones:

Si se desea usar el método KNN, se debe utilizar esta función.

.. code-block:: python

   from SpatialCluster.preprocess.data_format import attributes_with_zone_format
   features_position, features_X = attributes_with_zone_format(df)


Si se desea usar cualquier otro método que ofrece SpatialCluster, se debe utilizar esta función.

.. code-block:: python

   from SpatialCluster.preprocess.data_format import attributes_format
   features_position, features_X = attributes_format(df)