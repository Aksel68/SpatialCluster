from SpatialCluster.utils.data_format import data_format, position_data_format
from SpatialCluster.utils.get_areas import get_areas
from scipy.stats import hypergeom
from scipy import spatial
import pandas as pd
import numpy as np

def KNN_Clustering(features_X, features_position, attribute, threshold, location, condition="<", k=1500, K=5000, alfa = 0.01, leafsize=10):
    features_X = data_format(features_X)
    features_position = position_data_format(features_position)
    if(k > K):
        raise Exception('K has to be greater than k')
    features_X = pd.concat([features_position, features_X], axis=1)
    t = []
    f = []
    x_name = []
    x_centroid = []
    for name, df in features_X.groupby(location):
        x_name.append(name)
        t.append(df.shape[0])
        if(condition == ">"):
            f.append(df[df[attribute] > threshold].shape[0])
        elif(condition == "<"):
            f.append(df[df[attribute] < threshold].shape[0])
        elif(condition == ">="):
            f.append(df[df[attribute] >= threshold].shape[0])
        elif(condition == "<="):
            f.append(df[df[attribute] <= threshold].shape[0])
        elif(condition == "=="):
            f.append(df[df[attribute] == threshold].shape[0])
        x_centroid.append((df["lon"].mean(), df["lat"].mean()))
    tree = spatial.KDTree(data = x_centroid, leafsize = leafsize)
    NK = tree.query(x_centroid, k = len(x_centroid))[1]
    Tk = []
    Fk = []
    TK = []
    FK = []
    for j in range(NK.shape[0]):
        ti = 0
        fi = 0
        Ti = 0
        Fi = 0
        for i in NK[j]:
            if ti < k:
                ti += t[i]
                fi += f[i]
            if Ti < K:
                Ti += t[i]
                Fi += f[i]
            else:
                break
        Tk.append(ti)
        Fk.append(fi)
        TK.append(Ti)
        FK.append(Fi)
    p_hot = []
    p_cold = []
    for j in range(len(x_centroid)):
        hpd = hypergeom(TK[j], FK[j], Tk[j])
        a1 = hpd.cdf(Fk[j])
        b1 = hpd.cdf(Tk[j])
        p_hot.append(b1-a1)
        b = hpd.cdf(Fk[j])
        p_cold.append(b)
    centroid_clusters = {}
    for i in range(len(x_centroid)):
        if(p_hot[i] < alfa):
            centroid_clusters[x_name[i]] = 1
        elif(p_cold[i] < alfa):
            centroid_clusters[x_name[i]] = -1
        else:
            centroid_clusters[x_name[i]] = 0
    clusters = np.zeros(features_X.shape[0])
    for i, row in features_X.iterrows():
        clusters[i] = centroid_clusters[row[location]]
    points = list(zip(features_X.lon, features_X.lat))
    areas_to_points = get_areas(clusters, points)
    return areas_to_points, clusters

    