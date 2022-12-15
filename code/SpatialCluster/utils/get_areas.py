def get_areas(clusters, points):
    num_points = len(points)
    areas_to_points = dict()
    for i in range(num_points):
        area = int(clusters[i])
        if area in areas_to_points:
            areas_to_points[area].append(points[i])
        else:
            areas_to_points[area] = [points[i]]

    return areas_to_points