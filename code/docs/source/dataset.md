Dataset
=======

Origen
--------------

El dataset originalmente corresponde a datos de unidades administrativas del censo de Santiago de Chile y otras fuentes a nivel de manzana, las cuales contienen distintas características que fueron agrupadas en 3 categorías: Visuales, Sociales y Suelo.


Características Visuales
-------------------------

Estas características fueron obtenidas a partir de fotografías del lugar físico correspondiente, las cuales fueron procesadas por una red neuronal de las cuales se consideraron las siguientes 6 características.

    - beautiful: (float) Indica qué tanta belleza se percibe en el lugar de la imagen.
    - boring: (float) Indica qué tan monótono se ve el lugar de la imagen.
    - depressing: (float) Indica qué tan triste se percibe el lugar de la imagen.
    - lively: (float) Indica qué tan vivo o emocionante se ve el lugar de la imagen.
    - safe: (float) Indica qué tan seguro se ve el lugar de la imagen.
    - wealth: (float) Indica qué tan lujoso se ve el lugar de la imagen.

Se aplicó Principal Components Analysis (PCA) para reducir el número de características. Se escogió el número de dimensiones de PCA que capturaran al menos 80% de la varianza, por lo que para las características visuales bastó con solo dos ("visual_0", "visual_1").

Características Sociales
-------------------------

Estas características fueron obtenidas apartir del nivel socioeconómico del Censo 2012, la proporción de habitantes inmigrantes del Censo 2017, el plebiscito constitucional 2020 y la primera ronda de las elecciones presidenciales 2021 estimadas a nivel de manzana, y por último se obtuvo datos de la distribución de apellidos basados en el índice alfa de Bro, N., Mendoza, M. (2021):

    - prom_nse: (float) Nivel socioeconómico promedio.
    - edad_prom: (float) Edad promedio.
    - porcentaje_inmigrantes: (float) Proporción de habitantes inmigrantes.
    - prop_apruebo_promedio: (float) Proporción de habitantes que votaron apruebo en el Plebiscito Constitucional 2020.
    - mapuche_prom: (float) Proporción de habitantes promedio con apellido mapuche.
    - elite_prom: (float) Proporción de habitantes promedio con apellido de clase alta.

Se aplicó Principal Components Analysis (PCA) para reducir el número de características. Se escogió el número de dimensiones de PCA que capturaran al menos 80% de la varianza, por lo que para las características sociales bastó con solo dos ("social_0", "social_1").

Características de Suelo
-------------------------

Estas características corresponden a cómo el Estado clasifica las diferentes áreas de la ciudad con el propósito para la declaración de impuestos. De este se obtuvieron las siguientes características:

    - prop_uso_A: (float) Proporción de uso de suelo destinado a Armamento.
    - prop_uso_C: (float) Proporción de uso de suelo destinado a Comercio.
    - prop_uso_D: (float) Proporción de uso de suelo destinado a Deporte.
    - prop_uso_E: (float) Proporción de uso de suelo destinado a Educación.
    - prop_uso_F: (float) Proporción de uso de suelo destinado a Forestal.
    - prop_uso_G: (float) Proporción de uso de suelo destinado a Hotelería.
    - prop_uso_H: (float) Proporción de uso de suelo destinado a Vivienda.
    - prop_uso_I: (float) Proporción de uso de suelo destinado a Industria.
    - prop_uso_K: (float) Proporción de uso de suelo destinado a No codificado.
    - prop_uso_L: (float) Proporción de uso de suelo destinado a Almacenamiento.
    - prop_uso_M: (float) Proporción de uso de suelo destinado a Minería.
    - prop_uso_O: (float) Proporción de uso de suelo destinado a Negocio.
    - prop_uso_P: (float) Proporción de uso de suelo destinado a Gobierno.
    - prop_uso_Q: (float) Proporción de uso de suelo destinado a Culto.
    - prop_uso_S: (float) Proporción de uso de suelo destinado a Salud.
    - prop_uso_T: (float) Proporción de uso de suelo destinado a Transporte.
    - prop_uso_V: (float) Proporción de uso de suelo destinado a Otro.
    - prop_uso_W: (float) Proporción de uso de suelo destinado a Baldío.
    - prop_uso_Z: (float) Proporción de uso de suelo destinado a Estacionamiento.
    - total_m2_manzana: (float) Total de metros cuadrados que utiliza la manzana.

Se aplicó Principal Components Analysis (PCA) para reducir el número de características. Se escogió el número de dimensiones de PCA que capturaran al menos 80% de la varianza, por lo que para las características de suelo se necesitaron cuatro("suelo_0", "suelo_1", "suelo_2", "suelo_3").

Uso 
------------

Para tener acceso al dataset basta con usar la siguiente función:

```
   from SpatialCluster.datasets import load_manzana_data
   df = load_manzana_data()
```

Luego dependiendo del método que se quiera usar, se puede dar el formato correspondiente con las siguientes funciones:

Si se desea usar el método KNN, se debe utilizar esta función.

```
   from SpatialCluster.preprocess.data_format import attributes_with_zone_format
   features_position, features_X = attributes_with_zone_format(df, zona = "comuna")
```

Si se desea usar cualquier otro método que ofrece SpatialCluster, se debe utilizar esta función.

```
   from SpatialCluster.preprocess.data_format import attributes_format
   features_position, features_X = attributes_format(df)
```