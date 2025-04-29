def clean_data(data):
    if "temperature" in data.columns:
        data.loc[data["temperature"] >= 9999, "temperature"] = None
        data.loc[data["temperature"] < -40, "temperature"] = None
    if "salinity" in data.columns:
        data.loc[data["salinity"] >= 9999, "salinity"] = None
    if "significant_height" in data.columns:
        data.loc[data["significant_height"] >= 9999, "significant_height"] = None

    return data
