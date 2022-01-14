# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
import matplotlib.pyplot as plt
import matplotlib.colors as cl
import folium
from folium import Map
import random

def visualize_map_sample(areas_to_points, min_supp, max_samples_per_clusters):
    COLORS_9_SET = [plt.cm.Set1(i) for i in range(10)]
    COLORS_9_SET = [cl.to_hex(c) for c in COLORS_9_SET]

    hmap = Map(location=[-33.45, -70.65], control_scale=True, zoom_start=11, tiles = 'stamen toner')
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
                            color=colors_to_use[index], radius=10).add_to(hmap)
            
    return hmap