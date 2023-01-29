Visualización
===============

.. _installation:

=====

Graficar Mapa completo
-----------------------

El siguiente método genera el mapa con todos los puntos, coloreados según el clúster asignado.

### Parámetros

- **gdf**: *(GeoPandas DataFrame)* Contiene los atributos de los datos (sin longitud y latitud). *TDI* no trabaja con strings y se recomienda que los datos sean tipo float.
- **features_position**: *(Pandas DataFrame)* Contiene longitud y latitud de los datos.
- **A**: *(Numpy matrix)* Matriz de adyacencia que representará la topología del grafo que se utilizará para realizar *Spectral clustering*. Este debe conexo y simétrico para asegurar resultados coherentes. En caso de que no se entregue ninguna matriz, se utilizará *adjacencyMatrix* para crear una. Por defecto: None
- **r**: *(float)* Distancia máxima en metros a la que se considerará a un punto como vecino (Radio del vecindario para cada punto). Por defecto: 300.0
- **k**: *(int)* Cantidad de vecinos máxima que tendrá el vecindario para cada punto. Por defecto: 5
- **leafsize**: Corresponde al número de puntos en los que el algoritmo de KDTree de cambia a fuerza bruta (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html). Por defecto: 10

### Retorno

- **TDI_areas_to_points**: Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **TDI_clusters**: Arreglo con los puntos etiquetados según el cluster al que fueron asignado.  

.. code-block:: python

   plot_map(gdf, markersize=markersize, figsize=figsize)

=====

Graficar Muestreo aleatorio
----------------------------

El siguiente método genera el mapa con un muestreo aleatorio de los puntos, coloreados según el clúster asignado.

.. code-block:: python

   hmap = plot_map_sample(areas_to_points, min_supp=min_supp, max_samples_per_clusters=max_samples_per_clusters, location=location, radius=radius)
   hmap

