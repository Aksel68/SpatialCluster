Preprocesamiento
====================


Dar formato a tabla
--------------------

Para obtener los datos separados en variables con el formato que utilizan los métodos de la librería se ofrecen dos funciones distintas.

La primera corresponde a *attributes_format* que entrega *(features_position, features_X)* donde *features_position* corresponde a un dataframe con la longitud y latitud de los datos y *features_X* que corresponde a los atributos de los datos.

### Parámetros

- **df**: Pandas DataFrame con los datos a utilizar.

### Retorno

- **features_position**: Pandas DataFrame con la longitud y latitud de los datos.

- **features_X**: Pandas DataFrame con los atributos de los datos (sin longitud y latitud).

{py:func}`SpatialCluster.datasets.load_manzana_data`

```{eval-rst}
   autofunction:: SpatialCluster.datasets.load_manzana_data
```

```{eval-rst}
.. code-block:: python

   features_position, features_X = attributes_format(df)

```

La segunda corresponde a *attributes_with_zone_format* que entrega *(features_position, features_X)* donde *features_position* corresponde a un dataframe con la longitud y latitud de los datos y *features_X* que corresponde a los atributos de los datos con una columna extra que indica a qué zona pertenece el punto (en el dataset de ejemplo corresponde a la comuna).

```{eval-rst}
.. code-block:: python

   features_position, features_X = attributes_with_zone_format(df)
```


Matriz de adyacencia
---------------------

La función *adjacencyMatrix* crea una matriz de adyacencia que para cada punto almacena sus puntos más cercanos siguiendo un criterio en específico.

Para crear la matriz de adyacencia se pueden usar los siguientes criterios para definir una vecindad:

Por k vecinos más cercanos. (Criterio "*k*")

Por vecinos dentro de un radio r. (Criterio "*r*")

Por vecinos dentro de un radio r, con un mínimo de k_min vecinos, en caso de que haya menos que ese umbral se usarán k vecinos más cercanos. (Criterio "*rk*")

### Parámetros

- **features_position**: Pandas DataFrame con la longitud y latitud de los datos.
- **r**: Distancia máxima en metros a la que se considerará a un punto como vecino (Radio del vecindario para cada punto). Por defecto: 300
- **k**: Cantidad de vecinos máxima que tendrá el vecindario para cada punto. Por defecto: 5
- **min_k**: Cantidad mínima de vecinos que debe tener el vecindario en caso de usar el criterio "*rk*". Por defecto: 2
- **criteria**: Criterio que se usará para determinar los vecindarios (*k*, *r*, *rk*). Por defecto: "k"
- **leafsize**: Corresponde al número de puntos en los que el algoritmo de KDTree de cambia a fuerza bruta (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html). Por defecto: 10

### Retorno

- **A**: Matriz de adyacencia

```{eval-rst}
.. code-block:: python

   A = adjacencyMatrix(features_position, r = 300, k = 5, min_k = 2, criteria = "k", directed = True, leafsize = 10)
```


Anillos
------------

La función rings por cada columna de *features_X* crea nuevas columnas de atributos. Cada columna nueva está asociada a una columna de los datos originales, donde cada dato de esta nueva columna corresponde a una ponderación de las características de los vecinos utilizando la columna original asociada. Para cada columna original se crearán tantas columnas como cantidad de parámetros que se hayan ingresado en *max_radios* o *max_neighbours*, considerando para cada uno la nueva definición de vecindario correspondiente.

Por ejemplo: Si *max_radios* corresponde a (300, 400, 500) por cada columna de *features_X* se creará una columna que pondere definiendo vecindarios de 300 metros, luego otra columna que utilice vecindarios de 400 metros y finalmente otra columna que utilice vecindarios de 500 metros.

Para crear los anillos se pueden usar los siguientes criterios para definir un vecindario:

Por k vecinos más cercanos. (Criterio "*k*")

Por vecinos dentro de un radio r. (Criterio "*r*")

Por vecinos dentro de un radio r, con un mínimo de k_min vecinos, en caso de que haya menos que ese umbral se usarán k vecinos. (Criterio "*rk*")

### Parámetros

- **features_X**: Pandas DataFrame con los atributos de los datos (sin longitud y latitud).
- **features_position**: Pandas DataFrame con la longitud y latitud de los datos.
- **criteria**: Criterio que se usará para determinar los vecindarios (*k*, *r*, *rk*). Por defecto: "k"
- **max_radios**: Lista de radios en metros que se utilizarán para definir los vecindarios. Por defecto: [200, 300, 400]
- **max_neighbours**: Lista de cantidad máxima de puntos que tendrán los vecindarios. Por defecto: [200, 500, 1000]
- **weight_mode**: Criterio que se utilizará para la ponderación ("*Simple*" o "*Distance Inverse*"). Por defecto: "Simple"
- **keep_original_value**: Booleano que determinará si se conservan las columnas originales o no. Por defecto: True
- **smoothing**: Parámetro que se utiliza para suavizar las distancias al momento de ponderar los datos (útil en caso de ponderar con el inverso de la distancia, en caso de que estas sean muy cercanas a 0). Por defecto: 1e-08
- **normalize**: Booleano que se utiliza para normalizar las distancias, evita que al ponderar por el inverso de la distancia algunos datos se inflen más de lo deseado. Por defecto: True
- **leafsize**: Corresponde al número de puntos en los que el algoritmo de KDTree de cambia a fuerza bruta (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html). Por defecto: 10

### Retorno

- **features_X1**: Pandas DataFrame con las nuevas columnas creadas.

```{eval-rst}
.. code-block:: python

   features_X1 = rings(features_X, features_position, criteria="k", max_radios=[200, 300, 400], max_neighbours=[200, 500, 1000], weight_mode="Simple", keep_original_value=True, smoothing=1e-08, normalize=True, leafsize=10)
```

