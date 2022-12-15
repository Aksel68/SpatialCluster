import pandas as pd
import numpy as np

def data_format(data):
    try:
        data = pd.DataFrame(data)
        data = data.reset_index(drop=True)
        return data
    except:
        raise ValueError("Data not compatible with pandas DataFrame format")

def numpy_data_format(data):
    try:
        data = np.array(data)
        return data
    except:
        raise ValueError("Data not compatible with numpy Matrix format")

def position_data_format(data):
    try:
        data = pd.DataFrame(data, columns=["lon","lat"])
        data = data.reset_index(drop=True)
        return data
    except:
        raise ValueError("Data not compatible with pandas DataFrame format")
