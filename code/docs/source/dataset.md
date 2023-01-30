Dataset (En desarrollo)
=======

Origen
--------------

El dataset contiene distintas características, las cuales fueron agrupadas en 3 categorías: Visuales, Sociales, Suelo.


Características Visuales
-------------------------

Estas características fueron obtenidas a partir de fotografías del lugar físico correspondiente, las cuales fueron procesadas por una red neuronal que entregaba las siguientes características:

    - beautiful
    - boring
    - depressing
    - lively
    - safe
    - wealth

Características Sociales
-------------------------

Estas características fueron obtenidas desde el sitio web oficial del Servicio Electoral de Chile (Servel). De este se obtuvieron las siguientes características:

    - prom_nse
    - edad_prom
    - Porcentaje_Emigrantes
    - prop_apruebo_promedio
    - mapuche_prom
    - elite_prom

Características de Suelo
-------------------------

Estas características fueron obtenidas a partir del valuo fiscal obtenido del sitio web oficial del Servicio de Impuestos Internos de Chile (SII). De este se obtuvieron las siguientes características:

    - 'prop_uso_A','prop_uso_C','prop_uso_D','prop_uso_E'
    - 'prop_uso_G','prop_uso_H','prop_uso_I','prop_uso_K','prop_uso_L'
    - 'prop_uso_M','prop_uso_O','prop_uso_P','prop_uso_Q','prop_uso_S'
    - 'prop_uso_T','prop_uso_V','prop_uso_W','prop_uso_Z'
    - 'total_m2_manzana'

Uso 
------------

Para tener acceso al dataset basta con usar la siguiente función:

```{eval-rst}
.. code-block:: python

   from SpatialCluster.datasets import load_manzana_data
   df = load_manzana_data()
```

Luego dependiendo del método que se quiera usar, se puede dar el formato correspondiente con las siguientes funciones:

Si se desea usar el método KNN, se debe utilizar esta función.

```{eval-rst}
.. code-block:: python

   from SpatialCluster.preprocess.data_format import attributes_with_zone_format
   features_position, features_X = attributes_with_zone_format(df)
```

Si se desea usar cualquier otro método que ofrece SpatialCluster, se debe utilizar esta función.

```{eval-rst}
.. code-block:: python

   from SpatialCluster.preprocess.data_format import attributes_format
   features_position, features_X = attributes_format(df)
```