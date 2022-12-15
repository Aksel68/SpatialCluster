Visualización
===============

.. _installation:

=====

Graficar Mapa completo
-----------------------

El siguiente método genera el mapa con todos los puntos, coloreados según el clúster asignado.

.. code-block:: python

   plot_map(gdf, markersize=markersize, figsize=figsize)

=====

Graficar Muestreo aleatorio
----------------------------

El siguiente método genera el mapa con un muestreo aleatorio de los puntos, coloreados según el clúster asignado.

.. code-block:: python

   hmap = plot_map_sample(areas_to_points, min_supp=min_supp, max_samples_per_clusters=max_samples_per_clusters, location=location, radius=radius)
   hmap

