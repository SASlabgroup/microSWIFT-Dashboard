from dash import Dash, html, dcc, callback, Output, Input, no_update
import dash_bootstrap_components as dbc
from mission_utils import get_missions, get_missions_ids, get_mission_time
import pandas as pd
from data_retrieval import get_swift_data
from content_layout import single_layout, single_info_card, multi_layout, multi_info_card
from card_elements import multi_card, single_card
from graphs import multi_graphs, single_graphs

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define the layout of the app
app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1(['MicroSWIFT', html.Br(), 'Dashboard']),
                html.Img(src='/assets/SWIFTlogo_r.png', width="150", height="150"),
                html.Hr(),
                dcc.Dropdown(
                    options=get_missions(),
                    value='Bering Sea June 2024',
                    id='mission_dropdown'
                ),
                html.Br(),
                dcc.Dropdown(id='buoy_id'),
                html.Br(),
                html.Div([
                    html.P('Time Selection | Frequency v Energy'),
                    dcc.Dropdown(id='time_dropdown')
                ], id='time_selection'),
                html.Hr(),
                dbc.Card(id='latest_info', body=True),
                html.Footer('Version 0.8')
                
            ]),
            width=2,
            style={
                'background-color': 'grey',
                'padding': '10px',
                'position': 'fixed',
                'height': '100%',
                'overflow': 'auto'
            }
        ),
        dbc.Col(
            html.Div(id='graph_area', style={
                'margin': 'auto',
                'text-align': 'center',
                'width': '750px',
                'height': '100%',
                'background-color': '#f8f9fa',
            }),
            width={"size": 10, "offset": 2}
        )
    ])
])

# Update buoy IDs based on selected mission
@callback(
    [Output('buoy_id', 'options'), Output('buoy_id', 'value')],
    [Input('mission_dropdown', 'value')]
)
def update_ids(mission):
    buoy_ids = get_missions_ids(mission)
    options = [{'label': buoy_id, 'value': buoy_id} for buoy_id in buoy_ids]
    options.append({'label': 'All Buoys', 'value': 'All'})
    default_id = buoy_ids[0] if buoy_ids else None
    return options, default_id

# Update layout and info based on selected buoy ID
@callback(
    [Output('graph_area', 'children'), Output('latest_info', 'children'), Output('time_selection', 'style')],
    [Input('buoy_id', 'value')]
)
def update_layout(buoy_id):
    if buoy_id == "All":
        style = {'display': 'none'}
        return multi_layout, multi_info_card, style
    else:
        style = {'display': 'block'}
        return single_layout, single_info_card, style

# Update multi-buoy graphs
@callback(
    [Output('position_temperature_multi', 'figure'), Output('position_salinity_multi', 'figure'),
     Output('position_wave_height_multi', 'figure'), Output('buoy_time', 'children')],
    [Input('buoy_id', 'value'), Input('mission_dropdown', 'value')]
)
def update_multi(buoy_id, mission):
    if buoy_id == "All":
        start_date, end_date = get_mission_time(mission)
        df = get_swift_data(get_missions_ids(mission), start_date, end_date)
        position_temperature, position_salinity, position_height = multi_graphs(df)
        return position_temperature, position_salinity, position_height, multi_card(df, get_missions_ids(mission))
    return no_update, no_update, no_update, no_update

# Update time dropdown options for single buoy
@callback(
    [Output('time_dropdown', 'options'), Output('time_dropdown', 'value')],
    [Input('buoy_id', 'value'), Input('mission_dropdown', 'value')]
)
def update_time_dropdown(buoy_id, mission):
    if buoy_id != 'All':
        start_date, end_date = get_mission_time(mission)
        df = get_swift_data([buoy_id], start_date, end_date)
        if df is not None:
            df['times'] = pd.to_datetime(df['time'])
            date_strings = df['times'].dt.strftime("%Y-%m-%d %H:%M:%S%z").tolist()
            options = [{'label': date, 'value': date} for date in date_strings]
            value = date_strings[0]
            return options, value
    return no_update, no_update

# Update single buoy graphs and info
@callback(
    [Output('peak_direction_single', 'figure'), Output('peak_period_single', 'figure'),
     Output('wave_height_single', 'figure'), Output('position_temperature_single', 'figure'),
     Output('position_salinity_single', 'figure'), Output('position_wave_height_single', 'figure'),
     Output('loglog_frequency_energy', 'figure'), Output('linear_frequency_energy', 'figure'), Output('spectrogram_plot', 'figure'),
     Output('current_value', 'children'), Output('buoy_info', 'children')],
    [Input('buoy_id', 'value'), Input('mission_dropdown', 'value'), Input('time_dropdown', 'value')]
)
def update_single(buoy_id, mission, selected_time_str):
    if buoy_id != 'All':
        start_date, end_date = get_mission_time(mission)
        df = get_swift_data([buoy_id], start_date, end_date)
        if df is not None:
            peak_direction, peak_period, wave_height, position_temp, position_salinity, position_height, loglog, linear, spectrogram_fig = single_graphs(df, buoy_id, selected_time_str)
            # Info Card
            current_id = buoy_id
            buoy_info = single_card(df, buoy_id)

            return (peak_direction, peak_period, wave_height, position_temp, position_salinity, position_height, loglog, linear, spectrogram_fig, current_id, buoy_info)
        elif df is None:
            current_id = buoy_id
            buoy_info = 'No valid data retrieved for buoy ID'
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, current_id, buoy_info
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

if __name__ == '__main__':
    app.run_server(debug=True)
