import numpy as np
from scipy import spatial
from scipy.stats import hypergeom
from SpatialCluster.utils.get_areas import get_areas
from SpatialCluster.utils.data_format import data_format

def KNN_Clustering(features_X, attribute, threshold, location, condition=">", k=5, K=30, alfa = 0.01, leafsize=10):
    features_X = data_format(features_X)
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
    tree = spatial.KDTree(data = x_centroid, leafsize = leafsize) # Revisar si hacerlo con centroides o con todos los puntos
    Nk = tree.query(x_centroid, k = k)[1]
    NK = tree.query(x_centroid, k = K)[1]

    Tk = []
    Fk = []
    for j in range(Nk.shape[0]):
        ti = 0
        fi = 0
        for i in Nk[j]:
            ti += t[i]
            fi += f[i]
        Tk.append(ti)
        Fk.append(fi)
    TK = []
    FK = []
    for j in range(NK.shape[0]):
        ti = 0
        fi = 0
        for i in NK[j]:
            ti += t[i]
            fi += f[i]
        TK.append(ti)
        FK.append(fi)

    p_hot = []
    p_cold = []
    for j in range(len(x_centroid)): 
        hpd = hypergeom(TK[j], FK[j], Tk[j])
        p = 0
        for z in range(Fk[j], Tk[j]):
            p += hpd.pmf(z)
        p_hot.append(p)
        p = 0
        for z in range(Fk[j]):
            p += hpd.pmf(z)
        p_cold.append(p)

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

    