from dash import html
from data_retrieval import get_recent_data

def multi_card(df, buoy_ids):
    """
    Create a list of HTML card elements displaying the last data row for each specified buoy ID.

    Args:
        df (pd.DataFrame): Multi-index DataFrame containing SWIFT data.
        buoy_ids (list of str): List of buoy IDs to retrieve data for.

    Returns:
        list: List of Dash HTML components representing the data for each buoy ID.
    """
    cards = []
    
    for buoy_id in buoy_ids:
        recent_data = get_recent_data(df, buoy_id)
        
        if recent_data is not None:
            formatted_time = recent_data['time']
            card_content = f'ID: {buoy_id} | {formatted_time}'
            cards.extend([html.P(card_content), html.Br()])
        else:
            card_content = f'ID: {buoy_id} | Data not found'
            cards.extend([html.P(card_content), html.Br()])
    
    return cards

def single_card(df, buoy_id):
    """
    Create a list of HTML card elements displaying the last data row for a buoy ID.

    Args:
        df (pd.DataFrame): Multi-index DataFrame containing SWIFT data.
        buoy_id (str): Buoy ID to retrieve data for.

    Returns:
        list: List of Dash HTML components representing the data for a buoy ID.
    """
    cards = []
    
    recent_data = get_recent_data(df, buoy_id)

    if recent_data is not None:
        card_content = html.P([
                f'Significant Wave Height: {recent_data["significant_height"]:.3f}', html.Br(),
                f'Peak Period: {recent_data["peak_period"]:.3f}', html.Br(),
                f'Peak Direction: {recent_data["peak_direction"]:.3f}', html.Br(),
                f'Timestamp: {recent_data["time"]}'])
        cards.append(card_content)
    else:
        card_content = html.P([f'ID: {buoy_id} | Data not found', html.Br()])
        cards.append(card_content)

    return cards
