Preprocesamiento
====================


Dar formato a tabla
--------------------

Para obtener los datos separados en variables con el formato que utilizan los métodos de la librería se ofrecen dos funciones distintas.

La primera corresponde a *attributes_format* que entrega los datos separados en posición (longitud, latitud) y atributos.

### Parámetros

- **df**: *(Pandas DataFrame)* Contiene los datos a utilizar.

### Retorno

- **features_position**: *(Pandas DataFrame)* Contiene la longitud y latitud de los datos.

- **features_X**: *(Pandas DataFrame)* Contiene los atributos de los datos (sin longitud ni latitud).


```
   from SpatialCluster.preprocess.data_format import attributes_format
   features_position, features_X = attributes_format(df)
```

La segunda corresponde a *attributes_with_zone_format* que entrega los datos separados en posición (longitud, latitud) y atributos con una columna extra que indica a qué zona pertenece cada punto (en el dataset de ejemplo corresponde a la comuna).

### Parámetros

- **df**: *(Pandas DataFrame)* Contiene los datos a utilizar.

- **zona**: *(string)* Nombre de la columna que contiene la zona a la que pertenece cada punto.

### Retorno

- **features_position**: *(Pandas DataFrame)* Contiene la longitud y latitud de los datos.

- **features_X**: *(Pandas DataFrame)* Contiene los atributos de los datos incluyendo la columna de zona (sin longitud ni latitud).

```
   from SpatialCluster.preprocess.data_format import attributes_with_zone_format
   features_position, features_X = attributes_with_zone_format(df, zona = "comuna")
```


Matriz de adyacencia
---------------------

La función *adjacencyMatrix* crea una matriz de adyacencia en la que cada punto es relacionado con sus vecinos más cercanos siguiendo un criterio en específico.

Para crear la matriz de adyacencia se pueden usar los siguientes criterios para definir una vecindad:

Por k vecinos más cercanos (criterio "*k*").

Por vecinos dentro de un radio r (criterio "*r*").

Por vecinos dentro de un radio r, con un mínimo de k_min vecinos. En caso de que no hayan suficientes puntos para superar ese umbral, se usarán k vecinos más cercanos (criterio "*rk*").

### Parámetros

- **features_X**: *(Pandas DataFrame)* Contiene los atributos de los datos (sin longitud ni latitud).
- **r**: *(float)* Distancia máxima en metros a la que se considerará a un punto como vecino (radio del vecindario para cada punto). Por defecto: 300.0
- **k**: *(int)* Cantidad de vecinos máxima que tendrá el vecindario para cada punto. Por defecto: 5
- **min_k**: *(int)* Cantidad mínima de vecinos que debe tener el vecindario en caso de usar el criterio "*rk*". Por defecto: 2
- **criteria**: *(string)* Criterio que se usará para determinar los vecindarios (*k*, *r*, *rk*). Por defecto: "k"
- **leafsize**: *(int)* Número de puntos en los que el algoritmo de KDTree de cambia a fuerza bruta. Para más información, revisar la [Documentación de KDTree](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html). Por defecto: 10

### Retorno

- **A**: *(Numpy Matrix)* Matriz de adyacencia

```
   from SpatialCluster.preprocess.adjacency import adjacencyMatrix
   A = adjacencyMatrix(features_position, r = 300.0, k = 5, min_k = 2, criteria = "k", directed = True, leafsize = 10)
```


Anillos
------------

La función *rings* utiliza la ponderación de los datos de los vecinos de cada punto, creando una nueva columna con estos datos. Esto se repite para cada columna original del dataset, permitiendo así suavizar la diferencia de los atributos entre puntos cercanos. Para cada columna original se crearán tantas columnas como cantidad de parámetros que se hayan ingresado en *max_radios* o *max_neighbours*, considerando para cada uno la nueva definición de vecindario correspondiente.

Por ejemplo: Si *max_radios* corresponde a (300, 400, 500), por cada columna de *features_X* se creará una columna que pondere definiendo vecindarios de 300 metros, luego otra columna que utilice vecindarios de 400 metros y finalmente otra columna que utilice vecindarios de 500 metros.

Para crear los anillos se pueden usar los siguientes criterios para definir un vecindario:

- Por k vecinos más cercanos (criterio "*k*").

- Por vecinos dentro de un radio r (criterio "*r*").

- Por vecinos dentro de un radio r, con un mínimo de k_min vecinos. En caso de que no hayan suficientes puntos para superar ese umbral, se usarán k vecinos más cercanos (criterio "*rk*").

### Parámetros

- **features_X**: *(Pandas DataFrame)* Contiene los atributos de los datos (sin longitud ni latitud).
- **features_position**: *(Pandas DataFrame)* Contiene longitud y latitud de los datos.
- **criteria**: *(string)* Criterio que se usará para determinar los vecindarios (*k*, *r*, *rk*). Por defecto: "k"
- **max_radios**: *(Lista de floats)* Lista de radios en metros que se utilizarán para definir los vecindarios. Por defecto: [200.0, 300.0, 400.0]
- **max_neighbours**: *(Lista de ints)* Lista de cantidad máxima de puntos que tendrán los vecindarios. Por defecto: [200, 500, 1000]
- **weight_mode**: *(string)* Criterio que se utilizará para la ponderación ("*Simple*" o "*Distance Inverse*"). Por defecto: "Simple"
- **keep_original_value**: *(bool)* Determinará si se conservan las columnas originales o no. Por defecto: True
- **smoothing**: *(float)* Parámetro que se utiliza para suavizar las distancias al momento de ponderar los datos (útil en caso de ponderar con el inverso de la distancia, en caso de que estas sean muy cercanas a 0). Por defecto: 1e-08
- **normalize**: *(bool)* Determina si se normalizan las distancias, lo cual evita que al ponderar por el inverso de la distancia algunos datos sean sobrerrepresentados. Por defecto: True
- **leafsize**: *(int)* Número de puntos en los que el algoritmo de KDTree de cambia a fuerza bruta. Para más información, revisar la [Documentación de KDTree](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html). Por defecto: 10

### Retorno

- **features_rings**: *(Pandas DataFrame)* Contiene las nuevas columnas creadas.

```
   from SpatialCluster.preprocess.rings import rings
   features_rings = rings(features_X, features_position, criteria="k", max_radios=[200.0, 300.0, 400.0], max_neighbours=[200, 500, 1000], weight_mode="Simple", keep_original_value=True, smoothing=1e-08, normalize=True, leafsize=10)
```

