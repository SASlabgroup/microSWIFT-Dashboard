# content_layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc


multi_layout = [
    dbc.Row([
        dbc.Col([
            html.H2('Position'),
            dbc.Card(
                dcc.Graph('position_temperature_multi')
            ),
            dbc.Card(
                dcc.Graph('position_salinity_multi')
            ),
            dbc.Card(
                dcc.Graph('position_wave_height_multi')
            )
        ])
    ])
]

multi_info_card = [html.H4('LATEST DATA'),
                   html.Hr(),
                   html.Div(id='buoy_time')]


single_layout = [
    dbc.Row([
        dbc.Col([
            html.H2('Time Series'),
            # dbc.Card(
            #     dcc.Graph(id='peak_direction_single')
            # ),
            # dbc.Card(
            #     dcc.Graph(id='peak_period_single')
            # ),
            dbc.Card(
                dcc.Graph(id='wave_height_single')
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2('Position'),
            dbc.Card(
                dcc.Graph(id='position_temperature_single')
            ),
            dbc.Card(
                dcc.Graph(id='position_salinity_single')
            ),
            dbc.Card(
                dcc.Graph(id='position_wave_height_single')
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2('Frequency v Energy'),
            dbc.Card(
                dcc.Graph('loglog_frequency_energy')
            ),
            dbc.Card(
                dcc.Graph('linear_frequency_energy')
            ),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2('Frequency v Energy Spectrogram'),
            dbc.Card(
                dcc.Graph(id='spectrogram_plot', style={'margin': 'auto'})
            )
        ])
    ])
]

single_info_card = [html.H4('LATEST DATA'),
                    html.Hr(),
                    html.H2(id='current_value'),
                    html.P(id='buoy_info')]
