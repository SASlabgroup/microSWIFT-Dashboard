import pandas as pd
import plotly.express as px
from dash import no_update
from spectrogram_plot import spectrogram


def _style_position_map(fig):
    fig.update_geos(
        projection_type="natural earth",
        fitbounds="locations",
        showcoastlines=True,
        coastlinecolor="black",
        coastlinewidth=1,
        showland=True,
        landcolor="rgb(232, 228, 216)",
        showocean=True,
        oceancolor="rgb(214, 230, 244)",
        showlakes=True,
        lakecolor="rgb(214, 230, 244)",
    )
    fig.update_layout(margin={"l": 10, "r": 10, "t": 40, "b": 10})
    return fig


def multi_graphs(df):
    hover_data = {"time": True}  # Add time to the hover data
    if "Buoy ID" in df.columns:
        hover_data["Buoy ID"] = True

    position_temperature = px.scatter_geo(
        df,
        lon="longitude",
        lat="latitude",
        color="temperature",
        title="Temperature by Position",
        hover_data=hover_data,
    )
    position_temperature = _style_position_map(position_temperature)

    position_salinity = px.scatter_geo(
        df,
        lon="longitude",
        lat="latitude",
        color="salinity",
        title="Salinity by Position",
        hover_data=hover_data,
    )
    position_salinity = _style_position_map(position_salinity)

    position_height = px.scatter_geo(
        df,
        lon="longitude",
        lat="latitude",
        color="significant_height",
        title="Wave Height by Position",
        hover_data=hover_data,
    )
    position_height = _style_position_map(position_height)

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
    if "Buoy ID" in df.columns:
        hover_data["Buoy ID"] = True

    position_temperature = px.scatter_geo(
        df,
        lon="longitude",
        lat="latitude",
        color="temperature",
        title="Temperature by Position",
        hover_data=hover_data,
    )
    position_temperature = _style_position_map(position_temperature)

    position_salinity = px.scatter_geo(
        df,
        lon="longitude",
        lat="latitude",
        color="salinity",
        title="Salinity by Position",
        hover_data=hover_data,
    )
    position_salinity = _style_position_map(position_salinity)

    position_height = px.scatter_geo(
        df,
        lon="longitude",
        lat="latitude",
        color="significant_height",
        title="Wave Height by Position",
        hover_data=hover_data,
    )
    position_height = _style_position_map(position_height)

    # Spectrogram
    spectrogram_fig = spectrogram(df)

    return SingleGraphs(
        wave_height=wave_height,
        position_temperature=position_temperature,
        position_salinity=position_salinity,
        position_height=position_height,
        spectrogram_fig=spectrogram_fig,
    )
