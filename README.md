# MicroSWIFT Dashboard
The MicroSWIFT Dashboard is a Python-based tool designed to work with historical and real-time data from the microSWIFT wave buoy, developed by the University of Washington Applied Physics Laboratory (UW-APL).

<a href="https://microswift-dashboard.onrender.com">MicroSWIFT Dashboard</a>
<br>
Note: Currently, it will take 10-30 seconds to load

# Contents
This repository contains all the necessary files for running the application both locally and on Render for deployment. To ensure smooth deployment, avoid altering the file structure.
<ul>
  <li>app.py - The main application file containing all callback functions and layouts. Note: Keep callbacks within this file to avoid issues.</li>
  <li>content_layout.py - Contains the layout templates for displaying data from a single buoy or multiple buoys.</li>
  <li>graphs.py - Manages to create graph objects for visualization.</li>
  <li>Data_retrieval.py - Handles data retrieval from the microSWIFT API, including filtering functions.</li>
  <li>mission_ids.csv - A list of past and current deployments.</li>
</ul>

# Structure
```
microSWIFT-Dashboard
    |   app.py
    |   card_elements.py
    |   content_layout.py
    |   data_cleaning.py
    |   data_retrieval.py
    |   graphs.py
    |   LICENSE
    |   mission_ids.csv
    |   mission_utils.py
    |   README.md
    |   requirements.txt
    |   spectrogram_plot.py
    |   
    +---assets
    |       SWIFTlogo.png
    |       SWIFTlogo_r.png
```

# Local Installation
To run the application locally:
<ul>
  <li>Clone the repository:
    <pre>git clone &lt;repo_url&gt;</pre>
  </li>
  <li>Install the required dependencies:
    <pre>pip install -r requirements.txt</pre>
  </li>
  <li>Run the application:
    <pre>python app.py</pre>
    The application should be accessible through your hostlocal port.
  </li>
</ul>

# Running in a Container
To run the application in a container install a Docker compatible container system (ie: Docker or Podman). Then within this directory run
```shell
docker-compose up
```
```shell
podman-compose up
```

# Deployment
While Dash recommends using Heroku for deployment, we suggest using Render for its simplicity. For deployment on Render, follow their <a href="https://github.com/thusharabandara/dash-app-render-deployment">deployment guide</a>. <b>Note:</b> You will need to create a Render account.

If deploying on a private server, we recommend using Gunicorn for serving the application. <a href="https://gunicorn.org/">Learn more about Gunicorn here</a>.

Alternatively, this app can deployed using the provided [container image](https://github.com/SASlabgroup/microSWIFT-Dashboard/pkgs/container/microswift-dashboard).

# Adding a New Mission
To add a new mission:

<ul>
  <li>Update the <b>mission_ids.csv</b> file with the following details:
    <ul>
      <li>Mission name</li>
      <li>List of buoy IDs (separated by spaces)</li>
      <li>Start time in UTC format</li>
      <li>End time in UTC format or <b>None</b> (to retrieve the latest data)</li>
    </ul>
  </li>
</ul>

Examples:
```
Mission,Bouy_ids,Starttime,Endtime
Bering Sea June 2024, 040 041 065 077 080 082, 2024-06-01T00:00:00, None
Hurricane Idalia, 029 030 037 046 048, 2023-08-28T00:00:00, 2023-09-15T00:00:00
```

# Adding a New Visualization
To add a new visualization:

<ul>
  <li><b>Determine the Type:</b> Decide whether it's for a single buoy or multiple buoys.</li>
  <li><b>Modify <i>graphs.py</i>:</b> Add the graph object within the appropriate function:
    <pre>new_graph = px.&lt;GraphType&gt;(data_frame, x='label', y='label')</pre>
    Refer to the <a href="https://plotly.com/python/">Plotly documentation</a> for details on graph types.
  </li>
  <li><b>Update <i>content_layout.py</i>:</b> Add an <code>html.Card</code> element to allocate space for the new visual. Use a descriptive ID for the card.</li>
  <li><b>Modify <i>app.py</i>:</b> Add the new output in the relevant callback:
    <pre>Output('id_label', 'children')</pre>
  </li>
</ul>

# License
This project is licensed under the MIT License.
