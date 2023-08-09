from SpatialCluster.utils.data_format import data_format, numpy_data_format
from sklearn.metrics import normalized_mutual_info_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def AMI(clustering_1, clustering_2):
    clustering_1 = numpy_data_format(clustering_1)
    clustering_2 = numpy_data_format(clustering_2)
    return normalized_mutual_info_score(clustering_1, clustering_2)

def AMI_matrix(clusterings, plot=True, figsize = (10,8), linewidth=1):
    clusterings = data_format(clusterings)
    NMI_array = []
    len_columns = len(clusterings.columns)
    for i, cluster_1 in enumerate(clusterings.columns): 
        for j in range(i+1, len_columns):
            cluster_2 = clusterings.columns[j]
            df_cluster_1 = clusterings[cluster_1]
            df_cluster_2 = clusterings[cluster_2]
            NMI = normalized_mutual_info_score(df_cluster_1, df_cluster_2)
            NMI_array.append([cluster_2, cluster_1, NMI])
    NMI_df = pd.DataFrame(NMI_array)
    NMI_df_pivot = NMI_df.pivot(index=0, columns=1, values=2,).fillna(0)
    if(plot):
        plt.figure(figsize = figsize)
        mask = np.zeros_like(NMI_df_pivot)
        mask[np.triu_indices_from(mask)] = True
        for i in range(mask.shape[0]):
            mask[i,i] = False
        g = sns.heatmap(
            NMI_df_pivot, 
            cmap='OrRd',
            linewidth=linewidth,
            mask=mask,
            annot=True, fmt="0.2f")
        g.set_title('Normalized Mutual Info')
        g.set_xticklabels(g.get_xticklabels(), rotation=45, horizontalalignment='right')
        plt.show()
    return NMI_df_pivot