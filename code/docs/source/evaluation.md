Evaluación
===========

A continuación se ofrecen dos mediciones para comparar clusterings. Ambas son usadas comúnmente de forma conjunta ya que aún cuando su finalidad es la misma, tienen diferente base teórica. El valor es 0 cuando las particiones comparadas son aleatorias e independientes, y es 1 cuando son idénticas.

ARI
------------

Para comparar dos clusterings de mapas de atributos se puede usar la función ARI (Adjusted Rand Index), la cuál retorna un número real entre 0 y 1 que indica el grado de similaridad entre ambas soluciones.

```{eval-rst}
.. code-block:: python

   ari = ARI(clusters_map1, clusters_map2)
   ari
```

En caso de que se quieran comparar más de un par de mapas a la vez, se puede generar una matriz que muestra la relación ARI para cada par de clusterings.

```{eval-rst}
.. code-block:: python

   ari_matr = ARI_matrix(clusterings, plot=True)
   ari_matr
```


AMI
------------

Para comparar dos clusterings de mapas de atributos se puede usar la función AMI (Adjusted Mutual Information), la cuál retorna un número real entre 0 y 1 que indica el grado de similaridad entre ambas soluciones.
```{eval-rst}
.. code-block:: python

   ami = AMI(clusters_map1, clusters_map2)
   ami
```

En caso de que se quieran comparar más de un par de mapas a la vez, se puede generar una matriz que muestra la relación AMI para cada par de clusterings.

```{eval-rst}
.. code-block:: python

   ami_matr = AMI_matrix(clusterings, plot=True)
   ami_matr
```