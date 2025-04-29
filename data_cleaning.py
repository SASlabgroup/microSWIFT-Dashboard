def clean_data(data):
    if "temperature" in data.columns:
        data.loc[
            (data["temperature"] >= 9999) | (data["temperature"] < -40), "temperature"
        ] = None
    if "salinity" in data.columns:
        data.loc[data["salinity"] >= 9999, "salinity"] = None
    if "significant_height" in data.columns:
        data.loc[data["significant_height"] >= 9999, "significant_height"] = None

    if "latitude" in data.columns and "longitude" in data.columns:
        # Drop rows where both latitude and longitude are 0
        data = data.loc[~((data["latitude"] == 0) & (data["longitude"] == 0))]

    return data
