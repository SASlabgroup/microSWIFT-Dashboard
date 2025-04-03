import pandas as pd
import microSWIFTtelemetry
from data_cleaning import clean_data


def get_swift_data(buoy_ids, start_date, end_date=None):
    """
    Retrieve SWIFT data for given buoy IDs starting from a specified date.

    Args:
        buoy_ids (list): List of buoy IDs.
        start_date (str or datetime): Start date for data retrieval.
        end_date (str or datetime, optional): End date for data retrieval. If not provided, retrieves data up to the present.

    Returns:
        DataFrame: Multi-index DataFrame containing data for the specified buoy IDs, or None if no valid data is retrieved.
    """
    if not buoy_ids:
        raise ValueError("buoy_ids list cannot be empty")

    microSWIFT_df = pd.DataFrame()

    for buoy_id in buoy_ids:
        if end_date is None:
            data, error = microSWIFTtelemetry.pull_telemetry_as_var(
                buoy_id, start_date, var_type="pandas"
            )
        else:
            data, error = microSWIFTtelemetry.pull_telemetry_as_var(
                buoy_id, start_date, end_date, var_type="pandas"
            )

        if len(data) != 0:
            data["Buoy ID"] = buoy_id
            data["time"] = data.index
            data = clean_data(data)
            microSWIFT_df = pd.concat([microSWIFT_df, data], ignore_index=False)
        else:
            print(f"Error retrieving data for buoy ID {buoy_id}: {error}")

    if microSWIFT_df.empty:
        print("No valid data retrieved for buoy ID(s).")
        return None

    microSWIFT_df.set_index(["Buoy ID", microSWIFT_df.index], inplace=True)
    return microSWIFT_df


def get_recent_data(df, buoy_id):
    """
    Retrieve the most recent data for a specific buoy ID from the DataFrame.

    Args:
        df (pd.DataFrame): Multi-index DataFrame containing SWIFT data.
        buoy_id (str): The specific buoy ID for which to retrieve the last row.

    Returns:
        pd.Series: The recent data for the specified buoy ID.
    """
    try:
        buoy_data = df.xs(buoy_id, level="Buoy ID")
        last_row = buoy_data.tail(1).squeeze()
        return last_row
    except KeyError:
        print(f"Buoy ID {buoy_id} not found in the DataFrame.")
        return None
