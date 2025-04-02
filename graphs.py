import pandas as pd
import plotly.express as px
from spectrogram_plot import spectrogram

def multi_graphs(df):
    hover_data = {'time': True}  # Add time to the hover data

    position_temperature = px.scatter(
        df,
        x='longitude',
        y='latitude',
        color='temperature',
        title='Temperature by Position',
        hover_data=hover_data
    )

    position_salinity = px.scatter(
        df,
        x='longitude',
        y='latitude',
        color='salinity',
        title='Salinity by Position',
        hover_data=hover_data
    )

    position_height = px.scatter(
        df,
        x='longitude',
        y='latitude',
        color='significant_height',
        title='Wave Height by Position',
        hover_data=hover_data
    )

    return position_temperature, position_salinity, position_height


def single_graphs(df, buoy_id, selected_time_str):
    # Time Series Graphs
    #peak_direction = px.line(df, x='time', y='peak_direction', title='Peak Direction Over Time')
    peak_period = px.line(df, x='time', y='peak_period', title='Peak Period Over Time')
    wave_height = px.line(df, x='time', y='significant_height', title='Wave Height Over Time')
            
    # Position Graphs
    hover_data = {'time': True}  # Add time to the hover data

    position_temperature = px.scatter(
        df,
        x='longitude',
        y='latitude',
        color='temperature',
        title='Temperature by Position',
        hover_data=hover_data
    )

    position_salinity = px.scatter(
        df,
        x='longitude',
        y='latitude',
        color='salinity',
        title='Salinity by Position',
        hover_data=hover_data
    )

    position_height = px.scatter(
        df,
        x='longitude',
        y='latitude',
        color='significant_height',
        title='Wave Height by Position',
        hover_data=hover_data
    )


    # Frequency vs Energy Graphs
    selected_time = pd.to_datetime(selected_time_str)
    plot_df = pd.DataFrame({
        'Frequency (Hz)': df.loc[(buoy_id, selected_time), "frequency"],
        'Energy Density': df.loc[(buoy_id, selected_time), "energy_density"]
    })
    
    loglog = px.line(plot_df, x='Frequency (Hz)', y='Energy Density', title='Energy Density vs. Frequency (LogLog)', log_x=True, log_y=True)
    linear = px.line(plot_df, x='Frequency (Hz)', y='Energy Density', title='Energy Density vs. Frequency (Linear)')

    # Spectrogram
    spectrogram_fig = spectrogram(df)

    # FIXME: Don't use positional returns, makes it hard to add and remove items
    # return (peak_direction, peak_period, wave_height, position_temperature, position_salinity, position_height, loglog, linear, spectrogram_fig)
    return (peak_period, wave_height, position_temperature, position_salinity, position_height, loglog, linear, spectrogram_fig)