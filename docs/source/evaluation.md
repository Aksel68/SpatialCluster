Evaluación
===========

.. _evaluation:

=====

ARI
------------

Para comparar dos clusterings de mapas de atributos se puede usar la función ARI, la cuál retorna un número real que indica el grado de relación entre los dos.

.. code-block:: python

   ari = ARI(clusters_map1, clusters_map2)
   ari


En caso de que se quieran comparar más de un par de mapas a la vez, se puede generar una matriz que muestra la relación ARI para cada par de combinaciones.

.. code-block:: python

   ari_matr = ARI_matrix(clusterings, plot=True)
   ari_matr

=====

AMI
------------

Para comparar dos clusterings de mapas de atributos se puede usar la función AMI, la cuál retorna un número real que indica el grado de relación entre los dos.

.. code-block:: python

   ami = AMI(clusters_map1, clusters_map2)
   ami

En caso de que se quieran comparar más de un par de mapas a la vez, se puede generar una matriz que muestra la relación AMI para cada par de combinaciones.

.. code-block:: python

   ami_matr = AMI_matrix(clusterings, plot=True)
   ami_matr
