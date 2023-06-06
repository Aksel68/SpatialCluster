Introducción
=============


Spatial Cluster es una librería open source que busca facilitar la generación de mapas de atributos urbanos que agrupen los datos en distintos conjuntos disjuntos (clustering). El proyecto consta de 5 módulos principales, los cuales corresponden a:

   -  **Preprocesamiento**: Ofrece distintas funciones de preprocesamiento de los datos para que puedan ser utilizados provechosamente por los métodos que incluye la librería.

   - **Métodos**: Actualmente cuenta con 5 métodos distintos que realizan la tarea de clustering.

   - **Visualización**: Actualmente cuenta con dos funciones para generar los mapas correspondientes utilizando los resultados obtenidos tras aplicar algún algoritmo de clustering.

   - **Evaluación**: Actualmente cuenta con dos medidas de evaluación para comparar pares de mapas (ARI y AMI).

   - **Dataset**: Ofrece un conjunto de datos recopilados de la Región Metropolitana de Chile que cumple los requisitos necesarios para utilizar cualquier método que ofrece la librería.


Instalación
------------

Para usar SpatialCluster, primero se debe instalar utilizando pip:

```{eval-rst}
.. code-block:: console

   (.venv) $ pip install SpatialCluster
```

Siguientes pasos
-----------------

Para utilizar la librería se recomienda visitar la sección de [Métodos](methods.md) y [Visualización](visualization.md) para ver ejemplos de uso. También se recomienda revisar la sección de [Preprocesamiento](preprocess.md) ya que puede ser bastante útil para obtener buenos resultados.