Métodos
========

DMoN
------------

Deep Modular Neural network es una red neuronal basada en grafos (GNN) usada en este caso para realizar clustering.

### Parámetros


- **features_X**: *(Pandas DataFrame)* Contiene los atributos de los datos (sin longitud y latitud). *DMoN* no trabaja con strings y se recomienda que los datos sean tipo float.
- **features_position**: *(Pandas DataFrame)* Contiene longitud y latitud de los datos.
- **A**: *(Numpy matrix)* Matriz de adyacencia utilizada, en caso de que no se entregue una se utilizará el método de adjacencyMatrix de SpatialCluster para crear una. Por defecto: None
- **criteria**: *(string)* Criterio que se usará para crear la matriz de adyacencia (*k*, *r*, *rk*). Por defecto: "k"
- **r_max**: *(float)* Radio máximo en metros que se utilizará para la creación de la matriz de adyacencia. Por defecto: 300.0
- **n_clusters**: *(int)* Cantidad de clusters que considerará el método para agrupar los datos. Por defecto: 4
- **reg**: *(float)* Párametro dentro del rango [0,1] para regularizar su función de pérdida y así evitar soluciones triviales como agrupar todos los datos en el mismo cluster. Por defecto: 1.0
- **dropout**: *(float)* Párametro del rango [0,1] para evitar el sobreajuste a los datos (overfitting). Valores altos permitirán evitar más el sobreajuste, pero afectará el entrenamiento haciendo necesario más datos. Por defecto: 0.0
- **num_epochs**: *(int)* Indica cuánto durará el entrenamiento. Valores muy altos podrían provocar sobreajuste. Por defecto: 500
- **learning_rate**: *(float)* Párametro dentro del rango [0,1] que indica la tasa de ajustes que irá realizando la red en cada época (epoch). Valores muy altos permitirán un cambio más agresivo, lo cual puede provocar que no logre encontrar el punto óptimo. Valores bajos implicará que el aprendizaje será más lento por lo cuál necesitará más épocas y más datos para entrenar.

### Retorno

- **DMoN_areas_to_points**: Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **DMoN_clusters**: Arreglo con los puntos etiquetados según el cluster al que fueron asignado.

```{eval-rst}
.. code-block:: python

   DMoN_areas_to_points, DMoN_clusters = DMoN_Clustering(features_X, features_position, A = None, criteria = "k", r_max = 300.0, n_clusters = 4, reg = 1.0, dropout = 0.0, num_epochs = 500, learning_rate = 0.001)

```

GMM
------------

Gaussian Mixture Models es un método clásico de clustering para datos urbanos.

### Parámetros

- **features_X**: *(Pandas DataFrame)* Contiene los atributos de los datos (sin longitud y latitud). *GMM* no trabaja con strings y se recomienda que los datos sean tipo float.
- **features_position**: *(Pandas DataFrame)* Contiene longitud y latitud de los datos.
- **n_clusters**: *(int)* Indica la cantidad de clusters que considerará el método para agrupar los datos. Por defecto: 4
- **covariance_type**: *(string)* Describe el tipo de parámetros de covarianza. Debe ser uno de los siguientes:

   - "full": Cada componente ttiene su propia matriz de covarianza general.

   - "tied": Todos los componentes comparten la misma matriz de covarianza general.

   - "diag": Cada componente tiene su propia covarianza de matriz diagonal.

   - "spherical": Cada componente tiene su propia varianza individual.

Por defecto: "full"

- **tol**: *(float)* Umbral de tolerancia. Las iteraciones del proceso Expectation-Maximization (EM) pararán cuando la ganancia promedio del límite inferior esté por debajo de este umbral. Por defecto: 1e-3
- **reg_covar**: *(float)* Parámetro no negativo para la regularización añadida a la diagonal de la matriz de covarianza. Permite asegurar que las matrices de covarianza sean positivas. Por defecto: 1e-6

### Retorno

- **GMM_areas_to_points**: Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **GMM_clusters**: Arreglo con los puntos etiquetados según el cluster al que fueron asignado.

```{eval-rst}
.. code-block:: python

   GMM_areas_to_points, GMM_clusters = GMM_Clustering(features_X, features_position, n_clusters = 4, covariance_type = "full", tol=1e-3, reg_covar=1e-6)
```

KNN
------------

K-Nearest Neighbours es un enfoque clásico para realizar clustering en general.

### Parámetros

- **features_X**: *(Pandas DataFrame)* Contiene los atributos de los datos (sin longitud y latitud).
- **features_position**: *(Pandas DataFrame)* Contiene longitud y latitud de los datos.
- **attribute**: *(string)* Indica qué columna de *features_X* se utilizará para caracterizar a los datos.
- **threshold**: *(float/int/bool)* Umbral que determina si un dato cumple o no con el criterio según su columna *attribute*.
- **location**: *(string)* Nombre de la columna de *features_X* se utilizará para determinar la zona geográfica a la que pertenecen los datos (Por ejemplo: "comuna").
- **condition**: *(string)* Operador que se utilizará (">", "<", ">=", "<=", "==") para ver si el dato cumple con la condición o no. Por defecto: ">"
- **k**: *(int)* Cantidad de vecinos cercanos se utilizarán para la unidad de área más pequeña. Por defecto: 5
- **K**: *(int)* Cantidad de vecinos cercanos se utilizarán para la unidad de área más grande. Por defecto: 30
- **alfa**: *(float)* Umbral para evaluar el estadístico de contraste. Por defecto: 0.01
- **leafsize**: *(int)* Número de puntos en los que el algoritmo de KDTree de cambia a fuerza bruta (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html). Por defecto: 10

### Retorno

- **KNN_areas_to_points**: Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **KNN_clusters**: Arreglo con los puntos etiquetados según el cluster al que fueron asignado.

```{eval-rst}
.. code-block:: python

   KNN_areas_to_points, KNN_clusters = KNN_Clustering(features_X, features_position, attribute, threshold, location, condition=">", k=5, K=30, alfa = 0.01, leafsize=10)

```

SOM
------------

Self Organized Maps.

### Parámetros

- **features_X**: *(Pandas DataFrame)* Contiene los atributos de los datos (sin longitud y latitud). *SOM* no trabaja con strings y se recomienda que los datos sean tipo float.
- **features_position**: *(Pandas DataFrame)* Contiene longitud y latitud de los datos.
- **som_shape**: *(tupla de ints)* Determina la topología de la red neuronal que usará SOM de la forma (cantidad_filas, cantidad_columnas). Por defecto: (6,6)
- **sigma**: *(float)* Parámetro dentro del rango [0,1] que corresponde a la cantidad de información que se compartirá entre neuronas en cada iteración del proceso de entrenamiento de la red. Por defecto: 0.3
- **learning_rate**: *(float)* Párametro dentro del rango [0,1] que corresponde a la cantidad de información que se compartirá entre neuronas en cada iteración del proceso de entrenamiento de la red. Por defecto: 0.5
- **num_iterations**: *(int)* Cantidad de iteraciones que se realizarán en el proceso de entrenamiento. Por defecto: 100

### Retorno

- **SOM_areas_to_points**: Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **SOM_clusters**: Arreglo con los puntos etiquetados según el cluster al que fueron asignado.

```{eval-rst}
.. code-block:: python

   SOM_areas_to_points, SOM_clusters = SOM_Clustering(features_X, features_position, som_shape = (6,6), sigma=0.3, learning_rate=0.5, num_iterations = 100)
```

TDI
------------

TDI corresponde a un método basado en Teoría de la Información, la cual utiliza una matriz de pesos utilizando la divergencia de Shannon como distancia entre los puntos. Luego se aplica Spectral Clustering sobre esta matriz.

### Parámetros

- **features_X**: *(Pandas DataFrame)* Contiene los atributos de los datos (sin longitud y latitud). *TDI* no trabaja con strings y se recomienda que los datos sean tipo float.
- **features_position**: *(Pandas DataFrame)* Contiene longitud y latitud de los datos.
- **A**: *(Numpy matrix)* Matriz de adyacencia que representará la topología del grafo que se utilizará para realizar *Spectral clustering*. Este debe conexo y simétrico para asegurar resultados coherentes. En caso de que no se entregue ninguna matriz, se utilizará *adjacencyMatrix* para crear una. Por defecto: None
- **r**: *(float)* Distancia máxima en metros a la que se considerará a un punto como vecino (Radio del vecindario para cada punto). Por defecto: 300.0
- **k**: *(int)* Cantidad de vecinos máxima que tendrá el vecindario para cada punto. Por defecto: 5
- **leafsize**: Corresponde al número de puntos en los que el algoritmo de KDTree de cambia a fuerza bruta (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html). Por defecto: 10

### Retorno

- **TDI_areas_to_points**: Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **TDI_clusters**: Arreglo con los puntos etiquetados según el cluster al que fueron asignado.  

```{eval-rst}
.. code-block:: python

   TDI_areas_to_points, TDI_clusters = TDI_Clustering(features_X, features_position, A=A, r=radius, k=k, leafsize=leafsize)
```