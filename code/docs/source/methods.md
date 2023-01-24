Métodos
========

DMoN
------------

Deep Modular Neural network es una red neuronal basada en grafos (GNN) usada en este caso para realizar clustering.

### Parámetros

- **features_X**: Pandas DataFrame con los atributos de los datos (sin longitud y latitud). *DMoN* no trabaja con strings y se recomienda que los datos sean tipo float.
- **features_position**: Pandas DataFrame con la longitud y latitud de los datos.
- **A**: Matriz de adyacencia utilizada, en caso de que no se entregue una se utilizará el método de adjacencyMatrix de SpatialCluster para crear una. Por defecto: None
- **criteria**: Criterio que se usará para crear la matriz de adyacencia (*k*, *r*, *rk*). Por defecto: "k"
- **r_max**: Radio máximo en metros que se utilizará para la creación de la matriz de adyacencia. Por defecto: 300
- **n_clusters**: Cantidad de clusters que considerará el método para agrupar los datos. Por defecto: 4
- **reg**: Párametro tipo float dentro del rango [0,1] para regularizar su función de pérdida y así evitar soluciones triviales como agrupar todos los datos en el mismo cluster. Por defecto: 1.0
- **dropout**: Párametro tipo float dentro del rango [0,1] para evitar el sobreajuste a los datos (overfitting). Valores altos permitirán evitar más el sobreajuste, pero afectará el entrenamiento haciendo necesario más datos. Por defecto: 0.0
- **num_epochs**: Parámetro tipo int que indica cuánto durará el entrenamiento. Valores muy altos podrían provocar sobreajuste. Por defecto: 500
- **learning_rate**: Párametro tipo float dentro del rango [0,1] que indica la tasa de ajustes que irá realizando la red en cada época (epoch). Valores muy altos permitirán un cambio más agresivo, lo cual puede provocar que no logre encontrar el punto óptimo. Valores bajos implicará que el aprendizaje será más lento por lo cuál necesitará más épocas y más datos para entrenar.

### Retorno

- **DMoN_areas_to_points**: Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **DMoN_clusters**: Arreglo con los puntos etiquetados según el cluster al que fueron asignado.

.. code-block:: python

   DMoN_areas_to_points, DMoN_clusters = DMoN_Clustering(features_X, features_position, A = None, criteria = "k", r_max = 300, n_clusters = 4, reg = 1.0, dropout = 0.0, num_epochs = 500, learning_rate = 0.001)

=====

GMM
------------

Gaussian Mixture Models es un método clásico de clustering para datos urbanos.

### Parámetros

- **features_X**: Pandas DataFrame con los atributos de los datos (sin longitud y latitud). *GMM* no trabaja con strings y se recomienda que los datos sean tipo float.
- **features_position**: Pandas DataFrame con la longitud y latitud de los datos.
- **n_clusters**: Entero que indica la cantidad de clusters que considerará el método para agrupar los datos. Por defecto: 4
- **covariance_type**: String que describe el tipo de parámetros de covarianza. Debe ser uno de los siguientes:

   - "full": Cada componente ttiene su propia matriz de covarianza general.

   - "tied": Todos los componentes comparten la misma matriz de covarianza general.

   - "diag": Cada componente tiene su propia covarianza de matriz diagonal.

   - "spherical": Cada componente tiene su propia varianza individual.

Por defecto: "full"

- **tol**: Float para el umbral de tolerancia. Las iteraciones del proceso Expectation-Maximization (EM) pararán cuando la ganancia promedio del límite inferior esté por debajo de este umbral. Por defecto: 1e-3
- **reg_covar**: Float no negativo para la regularización añadida a la diagonal de la matriz de covarianza. Permite asegurar que las matrices de covarianza sean positivas. Por defecto: 1e-6

### Retorno

- **GMM_areas_to_points**: Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **GMM_clusters**: Arreglo con los puntos etiquetados según el cluster al que fueron asignado.


.. code-block:: python

   GMM_areas_to_points, GMM_clusters = GMM_Clustering(features_X, features_position, n_clusters = 4, covariance_type = "full", tol=1e-3, reg_covar=1e-6)

=====

KNN
------------

K-Nearest Neighbours es un enfoque clásico para realizar clustering en general.

### Parámetros

- **features_X**: Pandas DataFrame con los atributos de los datos (sin longitud y latitud).
- **features_position**: Pandas DataFrame con la longitud y latitud de los datos.
- **attribute**: String que indica qué columna de *features_X* se utilizará para caracterizar a los datos.
- **threshold**: Float/Int/Bool que corresponde al umbral que determina si un dato cumple o no con el criterio según su columna *attribute*.
- **location**: String que indica qué columna *features_X* se utilizará para determinar la zona geográfica a la que pertenecen los datos (Por ejemplo: "comuna").
- **condition**: String que indica el operador que se utilizará (">", "<", ">=", "<=", "==") para ver si el dato cumple con la condición o no. Por defecto: ">"
- **k**: Int que indica cuántos vecinos cercanos se utilizarán para la unidad de área más pequeña. Por defecto: 5
- **K**: Int que indica cuántos vecinos cercanos se utilizarán para la unidad de área más grande. Por defecto: 30
- **alfa**: Float que define el umbral para evaluar el estadístico de contraste. Por defecto: 0.01
- **leafsize**: Corresponde al número de puntos en los que el algoritmo de KDTree de cambia a fuerza bruta (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html). Por defecto: 10

### Retorno

- **KNN_areas_to_points**: Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **KNN_clusters**: Arreglo con los puntos etiquetados según el cluster al que fueron asignado.

.. code-block:: python

   KNN_areas_to_points, KNN_clusters = KNN_Clustering(features_X, features_position, attribute, threshold, location, condition=">", k=5, K=30, alfa = 0.01, leafsize=10)

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