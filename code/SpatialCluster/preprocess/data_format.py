def attributes_format(df):
    position = df[["lon", "lat"]]
    cols = df.columns
    attr_cols = []
    for col in cols:
        if(col != "lon" and col != "lat"):
            if("float" in str(type(df[col].values[0])) or "int" in str(type(df[col].values[0]))):
                attr_cols.append(col)
    attributes = df[attr_cols]
    return position, attributes

def attributes_with_zone_format(df, zona):
    position = df[["lon", "lat"]]
    cols = df.columns
    attr_cols = []
    for col in cols:
        if(col != "lon" and col != "lat"):    
            if("float" in str(type(df[col].values[0])) or "int" in str(type(df[col].values[0]))):
                attr_cols.append(col)
            elif(col == zona):
                attr_cols.append(col)
    attributes = df[attr_cols]
    return position, attributes
