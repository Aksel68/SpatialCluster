import pkg_resources
import pandas as pd

def load_manzana_data():
    stream = pkg_resources.resource_stream(__name__, 'data/reduced_data_MinMaxScaler_PCA_manzana_224.csv')
    return pd.read_csv(stream)