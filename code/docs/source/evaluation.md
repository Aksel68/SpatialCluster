Evaluación
===========

A continuación se ofrecen dos mediciones para comparar clusterings. Ambas son usadas comúnmente de forma conjunta ya que aún cuando su finalidad es la misma, tienen diferente base teórica. El valor es 0 cuando las particiones comparadas son aleatorias e independientes, y es 1 cuando son idénticas.

ARI
------------

Para comparar dos clusterings de mapas de atributos se puede usar la función ARI (Adjusted Rand Index), la cuál retorna un número real entre 0 y 1 que indica el grado de similaridad entre ambas soluciones.

### Parámetros

- **gdf**: *(GeoPandas DataFrame)* Contiene los clusters a los que pertenece cada punto y la geometría para localizarlos geográficamente en el mapa. En caso de que la columna "geometry" no exista, el método la generará a partir de las columnas "lon" y "lat".
- **markersize**: *(Int)* Tamaño de los puntos en el mapa. Por defecto: 30
- **figsize**: *(Tupla de ints)* Tamaño de la figura que contendrá el mapa. Por defecto: (12,8)

### Retorno

- No retorna nada, dibuja el mapa generado.

```{eval-rst}
.. code-block:: python

   plot_map(gdf, markersize=30, figsize=(12,8))

```{eval-rst}
.. code-block:: python

   ari = ARI(clusters_map1, clusters_map2)
   ari
```

En caso de que se quieran comparar más de un par de mapas a la vez, se puede generar una matriz que muestra la relación ARI para cada par de clusterings.

### Parámetros

- **gdf**: *(GeoPandas DataFrame)* Contiene los clusters a los que pertenece cada punto y la geometría para localizarlos geográficamente en el mapa. En caso de que la columna "geometry" no exista, el método la generará a partir de las columnas "lon" y "lat".
- **markersize**: *(Int)* Tamaño de los puntos en el mapa. Por defecto: 30
- **figsize**: *(Tupla de ints)* Tamaño de la figura que contendrá el mapa. Por defecto: (12,8)

### Retorno

- No retorna nada, dibuja el mapa generado.

```{eval-rst}
.. code-block:: python

   plot_map(gdf, markersize=30, figsize=(12,8))

```{eval-rst}
.. code-block:: python

   ari_matr = ARI_matrix(clusterings, plot=True)
   ari_matr
```


AMI
------------

Para comparar dos clusterings de mapas de atributos se puede usar la función AMI (Adjusted Mutual Information), la cuál retorna un número real entre 0 y 1 que indica el grado de similaridad entre ambas soluciones.

### Parámetros

- **gdf**: *(GeoPandas DataFrame)* Contiene los clusters a los que pertenece cada punto y la geometría para localizarlos geográficamente en el mapa. En caso de que la columna "geometry" no exista, el método la generará a partir de las columnas "lon" y "lat".
- **markersize**: *(Int)* Tamaño de los puntos en el mapa. Por defecto: 30
- **figsize**: *(Tupla de ints)* Tamaño de la figura que contendrá el mapa. Por defecto: (12,8)

### Retorno

- No retorna nada, dibuja el mapa generado.

```{eval-rst}
.. code-block:: python

   plot_map(gdf, markersize=30, figsize=(12,8))

```{eval-rst}
.. code-block:: python

   ami = AMI(clusters_map1, clusters_map2)
   ami
```

En caso de que se quieran comparar más de un par de mapas a la vez, se puede generar una matriz que muestra la relación AMI para cada par de clusterings.

### Parámetros

- **gdf**: *(GeoPandas DataFrame)* Contiene los clusters a los que pertenece cada punto y la geometría para localizarlos geográficamente en el mapa. En caso de que la columna "geometry" no exista, el método la generará a partir de las columnas "lon" y "lat".
- **markersize**: *(Int)* Tamaño de los puntos en el mapa. Por defecto: 30
- **figsize**: *(Tupla de ints)* Tamaño de la figura que contendrá el mapa. Por defecto: (12,8)

### Retorno

- No retorna nada, dibuja el mapa generado.

```{eval-rst}
.. code-block:: python

   plot_map(gdf, markersize=30, figsize=(12,8))

```{eval-rst}
.. code-block:: python

   ami_matr = AMI_matrix(clusterings, plot=True)
   ami_matr
```