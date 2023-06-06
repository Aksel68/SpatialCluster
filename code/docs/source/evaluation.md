Evaluación
===========

A continuación se ofrecen dos mediciones para comparar clusterings. Ambas son usadas comúnmente de forma conjunta ya que aún cuando su finalidad es la misma, tienen diferente base teórica. El valor es 0 cuando las particiones comparadas son aleatorias e independientes, y es 1 cuando son idénticas.

ARI
------------

Para comparar dos clusterings de mapas de atributos se puede usar la función ARI (Adjusted Rand Index), la cual retorna un número real entre 0 y 1 que indica el grado de similaridad entre ambas soluciones.

### Parámetros

- **clustering_1**: *(Numpy Array)* Contiene los clusters a los que pertenece cada punto para el clustering 1.
- **clustering_2**: *(Numpy Array)* Contiene los clusters a los que pertenece cada punto para el clustering 2.

### Retorno

- **ARI**: *(float)* ARI score.

```{eval-rst}
.. code-block:: python

   ari = ARI(clustering_1, clustering_2)
   ari
```

En caso de que se quieran comparar más de un par de mapas a la vez, se puede generar una matriz que muestra la relación ARI para cada par de clusterings.

### Parámetros

- **clusterings**: *(Numpy Matrix)* Contiene los clusters a los que pertenece cada punto para los distintos clusterings a comparar.
- **plot**: *(bool)* Indica si se desea mostrar la matriz gráficamente.

### Retorno

- **ARI_matr**: *(Numpy Matrix)* Contiene el ARI score para cada par de clusterings.

```{eval-rst}
.. code-block:: python

   ari_matr = ARI_matrix(clusterings, plot=True)
   ari_matr
```


AMI
------------

Para comparar dos clusterings de mapas de atributos se puede usar la función AMI (Adjusted Mutual Information), la cual retorna un número real entre 0 y 1 que indica el grado de similaridad entre ambas soluciones.

### Parámetros

- **clustering_1**: *(Numpy Array)* Contiene los clusters a los que pertenece cada punto para el clustering 1.
- **clustering_2**: *(Numpy Array)* Contiene los clusters a los que pertenece cada punto para el clustering 2.

### Retorno

- **AMI**: *(float)* AMI score.

```{eval-rst}
.. code-block:: python

   ami = AMI(clusters_map1, clusters_map2)
   ami
```

En caso de que se quieran comparar más de un par de mapas a la vez, se puede generar una matriz que muestra la relación AMI para cada par de clusterings.

### Parámetros

- **clusterings**: *(Numpy Matrix)* Contiene los clusters a los que pertenece cada punto para los distintos clusterings a comparar.
- **plot**: *(bool)* Indica si se desea mostrar la matriz gráficamente.

### Retorno

- **AMI_matr**: *(Numpy Matrix)* Contiene el AMI score para cada par de clusterings.

```{eval-rst}
.. code-block:: python

   ami_matr = AMI_matrix(clusterings, plot=True)
   ami_matr
```