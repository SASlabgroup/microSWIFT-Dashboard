import pandas as pd
import plotly.express as px
from dash import no_update
from spectrogram_plot import spectrogram


def multi_graphs(df):
    hover_data = {"time": True}  # Add time to the hover data

    position_temperature = px.scatter(
        df,
        x="longitude",
        y="latitude",
        color="temperature",
        title="Temperature by Position",
        hover_data=hover_data,
    )

    position_salinity = px.scatter(
        df,
        x="longitude",
        y="latitude",
        color="salinity",
        title="Salinity by Position",
        hover_data=hover_data,
    )

    position_height = px.scatter(
        df,
        x="longitude",
        y="latitude",
        color="significant_height",
        title="Wave Height by Position",
        hover_data=hover_data,
    )

    return position_temperature, position_salinity, position_height


class SingleGraphs:
    def __init__(
        self,
        peak_direction=no_update,
        peak_period=no_update,
        wave_height=no_update,
        position_temperature=no_update,
        position_salinity=no_update,
        position_height=no_update,
        loglog=no_update,
        linear=no_update,
        spectrogram_fig=no_update,
    ):
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


def get_single_graphs(df) -> SingleGraphs:
    # Time Series Graphs
    # peak_direction = px.line(df, x='time', y='peak_direction', title='Peak Direction Over Time')
    # peak_period = px.line(df, x='time', y='peak_period', title='Peak Period Over Time')
    wave_height = px.line(
        df, x="time", y="significant_height", title="Wave Height Over Time"
    )

    # Position Graphs
    hover_data = {"time": True}  # Add time to the hover data

    position_temperature = px.scatter(
        df,
        x="longitude",
        y="latitude",
        color="temperature",
        title="Temperature by Position",
        hover_data=hover_data,
    )

    position_salinity = px.scatter(
        df,
        x="longitude",
        y="latitude",
        color="salinity",
        title="Salinity by Position",
        hover_data=hover_data,
    )

    position_height = px.scatter(
        df,
        x="longitude",
        y="latitude",
        color="significant_height",
        title="Wave Height by Position",
        hover_data=hover_data,
    )

    # Spectrogram
    spectrogram_fig = spectrogram(df)

    return SingleGraphs(
        wave_height=wave_height,
        position_temperature=position_temperature,
        position_salinity=position_salinity,
        position_height=position_height,
        spectrogram_fig=spectrogram_fig,
    )
