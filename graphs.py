import pandas as pd
import plotly.express as px
from dash import no_update
from spectrogram_plot import spectrogram

# Shared labels for position-based scatter plots
POSITION_LABELS = {
    "longitude": "Longitude (°)",
    "latitude": "Latitude (°)",
    "time": "Time (UTC)",
}


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


def _build_position_hover_data(df):
    hover_data = {"time": True}  # Add time to the hover data
    if "Buoy ID" in df.columns:
        hover_data["Buoy ID"] = True
    return hover_data


def _build_position_map(df, hover_data, color, title, label):
    fig = px.scatter_geo(
        df,
        lon="longitude",
        lat="latitude",
        color=color,
        title=title,
        hover_data=hover_data,
        labels={**POSITION_LABELS, color: label},
    )
    return _style_position_map(fig)


def multi_graphs(df):
    hover_data = _build_position_hover_data(df)
    position_temperature = _build_position_map(
        df,
        hover_data,
        "temperature",
        "Temperature by Position",
        "Temperature (°C)",
    )

    position_salinity = _build_position_map(
        df,
        hover_data,
        "salinity",
        "Salinity by Position",
        "Salinity (PSU)",
    )

    position_height = _build_position_map(
        df,
        hover_data,
        "significant_height",
        "Wave Height by Position",
        "Significant Wave Height (m)",
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
    # peak_direction = px.line(df, x='time', y='peak_direction', title='Peak Direction Over Time', labels={'time': 'Time (UTC)', 'peak_direction': 'Peak Wave Direction (° from)'})
    # peak_period = px.line(df, x='time', y='peak_period', title='Peak Period Over Time', labels={'time': 'Time (UTC)', 'peak_period': 'Peak Wave Period (s)'})
    wave_height = px.line(
        df,
        x="time",
        y="significant_height",
        title="Wave Height Over Time",
        labels={"time": "Time (UTC)", "significant_height": "Significant Wave Height (m)"},
    )

    # Position Graphs
    hover_data = _build_position_hover_data(df)

    position_temperature = _build_position_map(
        df,
        hover_data,
        "temperature",
        "Temperature by Position",
        "Temperature (°C)",
    )

    position_salinity = _build_position_map(
        df,
        hover_data,
        "salinity",
        "Salinity by Position",
        "Salinity (PSU)",
    )

    position_height = _build_position_map(
        df,
        hover_data,
        "significant_height",
        "Wave Height by Position",
        "Significant Wave Height (m)",
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
