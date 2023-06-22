from SpatialCluster.constants import COLORS, palette
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib.colors as cl
import contextily as cx
from folium import Map
import numpy as np
import geopandas
import folium
import random

def plot_map(df, markersize = 10, figsize = (12,8), path = None):
    if("geometry" not in df.columns):
        gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df['lon'], df['lat']), crs=4326)
    else:
        gdf = geopandas.GeoDataFrame(df, geometry='geometry', crs=4326)
    n_clusters = np.unique(gdf["clusters"]).shape[0]
    if(n_clusters > len(palette)):
        cmap = None
    else:
        cmap = ListedColormap(palette[:n_clusters])
    fig, ax = plt.subplots(1, figsize=figsize)
    
    gdf.plot(column="clusters", cmap=cmap, ax=ax, markersize=markersize)

    try:
        cx.add_basemap(ax, crs=gdf.to_crs(4326).crs.to_string())
    except Exception as e:
        print(f'Basemap error')
        print(e)
    if path != None:
        plt.savefig(f'{path}')
    plt.show()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def plot_map_sample(areas_to_points, min_supp, max_samples_per_clusters, location = (-33.45, -70.65), radius = 10, path = None):
    COLORS_9_SET = [plt.cm.Set1(i) for i in range(10)]
    COLORS_9_SET = [cl.to_hex(c) for c in COLORS_9_SET]

    hmap = Map(location=location, control_scale=True, zoom_start=11, tiles = 'stamen toner')
    if len([x for x in areas_to_points.items() if len(x[1]) > min_supp]) <= 9:
        colors_to_use = COLORS_9_SET
    else:
        colors_to_use = COLORS
    sorted_points = {k: v for k, v in sorted(areas_to_points.items(), key=lambda item: len(item[1]), reverse=True)}
    
    for index, i in enumerate(sorted_points):
        if len(sorted_points[i]) <= min_supp:
            continue
        
        a_ = random.sample(sorted_points[i], min(len(sorted_points[i]), max_samples_per_clusters) )
        for point in a_:
            folium.Circle(location=[point[1], point[0]], popup = str(point),
                            color=colors_to_use[index], radius=radius).add_to(hmap)
    if path != None:
        hmap.save(path)
    return hmap