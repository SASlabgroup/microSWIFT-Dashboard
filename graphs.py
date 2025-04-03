import pandas as pd
import plotly.express as px
from dash import no_update
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


class SingleGraphs:
    def __init__(self, peak_direction=no_update, peak_period=no_update, wave_height=no_update, position_temperature=no_update, position_salinity=no_update, position_height=no_update, loglog=no_update, linear=no_update, spectrogram_fig=no_update):
        self.peak_direction = peak_direction
        self.peak_period = peak_period
        self.wave_height = wave_height
        self.position_temperature = position_temperature
        self.position_salinity = position_salinity
        self.position_height = position_height
        self.loglog = loglog
        self.linear = linear
        self.spectrogram_fig = spectrogram_fig
        self.current_id = no_update
        self.buoy_info = no_update


def get_single_graphs(df, buoy_id, selected_time_str) -> SingleGraphs:
    # Time Series Graphs
    # peak_direction = px.line(df, x='time', y='peak_direction', title='Peak Direction Over Time')
    # peak_period = px.line(df, x='time', y='peak_period', title='Peak Period Over Time')
    wave_height = px.line(
        df, x='time', y='significant_height', title='Wave Height Over Time')

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

    loglog = px.line(plot_df, x='Frequency (Hz)', y='Energy Density',
                     title='Energy Density vs. Frequency (LogLog)', log_x=True, log_y=True)
    linear = px.line(plot_df, x='Frequency (Hz)', y='Energy Density',
                     title='Energy Density vs. Frequency (Linear)')

    # Spectrogram
    spectrogram_fig = spectrogram(df)

    return SingleGraphs(wave_height=wave_height, position_temperature=position_temperature, position_salinity=position_salinity,
                        position_height=position_height, loglog=loglog, linear=linear, spectrogram_fig=spectrogram_fig)
