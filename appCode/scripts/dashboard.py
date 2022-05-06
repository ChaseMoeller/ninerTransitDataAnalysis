import os
import numpy as np
import pandas as pd
import plotly.express as px
import dash
from datetime import date, datetime

from dash import dcc, html, Input, Output, dash_table


def create_dashboard(server):

    #Creating the  inital application
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
    )
    
    #Data Upload
    folders = ["niner-transit-data", "spreadsheets"]
    controls = [
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in folders],
            value=folders[0],
        )
    ]

    #upload file
    df = pd.read_excel('niner-transit-data/Copy of Test Log #2.xlsx')

    #Creating the layout for the application
    dash_layout = html.Div([html.Div('bruh'), html.H1('Heading'), 
    html.Div(dcc.Dropdown(id='dropdown', options=[{'label':'thing1', 'value':'value1'}, {'label':'thing2', 'value':'value2'}]))    ])

    return dash_app.server

