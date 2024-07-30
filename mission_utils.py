# mission_utils.py

import pandas as pd

df = pd.read_csv('microSWIFT-Dashboard/mission_ids.csv')
df.set_index(['Mission'], inplace=True)

def get_missions():
    """
    Get a list of mission options for dropdowns.
s
    Returns:
        list: List of dictionaries with 'label' and 'value' for each mission.
    """
    missions = df.index
    options = [{'label': mission, 'value': mission} for mission in missions]
    return options

def get_missions_ids(mission):
    """
    Get a list of buoy IDs for a given mission.

    Args:
        mission (str): Mission name.

    Returns:
        list: List of buoy IDs.
    """
    ids = df.loc[mission]['Bouy_ids'].split()
    return ids

def get_mission_time(mission):
    """
    Get the start and end times for a given mission.

    Args:
        mission (str): Mission name.

    Returns:
        tuple: Start and end times as datetime objects. End time can be None if not available.
    """
    start = pd.Timestamp(df.loc[mission]['Starttime'])
    end = df.loc[mission]['Endtime'].strip()
    if end == 'None':
        return start, None
    end = pd.Timestamp(end)
    return start, end
