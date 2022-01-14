import pandas as pd

def data_format(data):
    try:
        data = pd.DataFrame(data)
        return data
    except:
        raise ValueError("Data not compatible with pandas DataFrame format")

def position_data_format(data):
    try:
        data = pd.DataFrame(data, columns=["lon","lat"])
        return data
    except:
        raise ValueError("Data not compatible with pandas DataFrame format")
