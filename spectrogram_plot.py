import numpy as np
import plotly.graph_objects as go

def spectrogram(microswift_df):
    energy_density_2d = np.stack(microswift_df['energy_density'])
    frequency_2d = np.stack(microswift_df['frequency'])
    time_1d = microswift_df['time']
    time_2d = np.tile(time_1d, (frequency_2d.shape[1], 1)).T

    fig = go.Figure(data=go.Heatmap(
        x=frequency_2d.flatten(),
        y=time_2d.flatten(),
        z=np.log10(energy_density_2d.flatten()),
        colorscale='Agsunset',
        colorbar=dict(
            title=dict(
                text='energy density (m^2/Hz) Log Scale',
                side='right',
                font=dict(size=12)
            ),
            tickvals=np.log10([0.01, 0.1, 1, 10]),
            ticktext=['0.01', '0.1', '1', '10']
        ),
        zmin=-2,
        zmax=1,
        zsmooth='best'
    ))

    fig.update_layout(
        title='MicroSWIFT Spectrogram',
        xaxis_title='frequency (Hz)',
        yaxis_title='month-day hour (UTC)',
        yaxis=dict(tickformat='%m-%d %HZ'),
        autosize=False,
        width=500,
        height=500
    )

    return fig
