Visualización
===============

Graficar Mapa completo
-----------------------

El siguiente método genera el mapa con todos los puntos, coloreados según el cluster asignado.

### Parámetros

- **gdf**: *(GeoPandas DataFrame)* Contiene los clusters a los que pertenece cada punto y la geometría para localizarlos geográficamente en el mapa. En caso de que la columna "geometry" no exista, el método la generará a partir de las columnas "lon" y "lat".
- **markersize**: *(int)* Tamaño de los puntos en el mapa. Por defecto: 30
- **figsize**: *(Tupla de ints)* Tamaño de la figura que contendrá el mapa. Por defecto: (12,8)
- **path**: *(string)* Indica la ruta y el nombre que se usará para guardar el archivo (ej: "/mapas/mapa.png"). Por defecto: None

### Retorno

- No retorna nada, dibuja el mapa generado.

```
   from SpatialCluster.visualization.plotters import plot_map
   plot_map(gdf, markersize=30, figsize=(12,8), path=None)
```

Graficar Muestreo aleatorio
----------------------------

El siguiente método genera un mapa interactivo con un muestreo aleatorio de los puntos, coloreados según el cluster asignado.

### Parámetros

- **areas_to_points**: *(dict)* Diccionario que para cada cluster guarda los puntos que pertenecen a este.
- **min_supp**: *(int)* Cantidad mínima de puntos que debe tener un cluster para aparecer.
- **max_samples_per_clusters**: *(int)* Cantidad máxima de puntos que se mostrarán por cada clúster.
- **location**: *(Tupla de ints)* Longitud y latitud de dónde estará posicionado el centro del mapa. Por defecto: (-33.45, -70.65)
- **radius**: *(int)* Tamaño del círculo que representará a cada punto. Por defecto: 10
- **path**: *(string)* Indica la ruta y el nombre que se usará para guardar el archivo (ej: "/mapas/mapa.html"). Por defecto: None

### Retorno

- **hmap**: *(Folium Map)* Mapa interactivo generado.

```
   from SpatialCluster.visualization.plotters import plot_map_sample
   hmap = plot_map_sample(areas_to_points, min_supp=min_supp, max_samples_per_clusters=max_samples_per_clusters, location=location, radius=radius, path=None)
```
