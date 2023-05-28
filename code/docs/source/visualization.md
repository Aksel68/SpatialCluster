Visualización
===============

Graficar Mapa completo
-----------------------

El siguiente método genera el mapa con todos los puntos, coloreados según el clúster asignado.

### Parámetros

- **gdf**: *(GeoPandas DataFrame)* Contiene los clusters a los que pertenece cada punto y la geometría para localizarlos geográficamente en el mapa. En caso de que la columna "geometry" no exista, el método la generará a partir de las columnas "lon" y "lat".
- **markersize**: *(Int)* Tamaño de los puntos en el mapa. Por defecto: 30
- **figsize**: *(Tupla de ints)* Tamaño de la figura que contendrá el mapa. Por defecto: (12,8)


### Retorno

- No retorna nada, dibuja el mapa generado.

```{eval-rst}
.. code-block:: python

   plot_map(gdf, markersize=30, figsize=(12,8))
```

Graficar Muestreo aleatorio
----------------------------

El siguiente método genera el mapa con un muestreo aleatorio de los puntos, coloreados según el clúster asignado.

### Parámetros

- **areas_to_points**: *(dict)* Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **min_supp**: *(int)* Cantidad mínima de puntos que debe tener un cluster para aparecer.
- **max_samples_per_clusters**: *(int)* Cantidad máxima de puntos que se mostrarán por cada clúster.
- **location**: *(Tupla de ints)* Longitud y latitud de dónde estará posicionado el centro del mapa. Por defecto: (-33.45, -70.65)
- **radius**: *(int)* Tamaño del círculo que representará a cada punto. Por defecto: 10

### Retorno

- **hmap**: Mapa generado.

```{eval-rst}
.. code-block:: python

   hmap = plot_map_sample(areas_to_points, min_supp=min_supp, max_samples_per_clusters=max_samples_per_clusters, location=location, radius=radius)
   hmap
```
