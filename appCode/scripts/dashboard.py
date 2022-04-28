import numpy as np
import pandas as pd
import plotly.express as px
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc

from dash import Dash, dcc, html, Input, Output


def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
    )

    df = pd.read_excel('appCode/niner-transit-data/Untitled spreadsheet-2.xlsx')
    


    fig = px.line_geo(df, lat="Latitude", lon="Longitude")

    dash_app.layout = html.Div(children=[

    html.Div([
        dcc.Dropdown(
            ['bar', 'line'],
            id='graph-type'
        ),
        dcc.Dropdown(
            df['Latitude'].unique(),
            id='x-axis-dd'
        ),
        dcc.Dropdown(
            df['Longitude'].unique(),
            id='y-axis-dd'
        )
    ]),
    html.Div([
        dcc.RadioItems(
            ['Silver', 'Gold', 'Green'],
            'Silver',
            id='routes'
        )
    ]),
    html.Div([
        dcc.Graph(
            id='graph-1',
            figure=fig
        )
    ])
])
    
    @dash_app.callback(
        Output(component_id='graph-1', component_property='figure'),
        Input(component_id='graph-type', component_property='value'),
        Input(component_id='routes', component_property='value'),
        
    )
    def update_graph(graph, routes):

        if(routes == 'Silver'):
            #sort the routes to only get silver
            dff = df[df['Routes'] == routes]
        elif(routes == 'Gold'):
            #sort the routes
            routes
        elif(routes == 'Green'):
            #sort the routes
            routes

        if(graph == 'bar'):
            fig = px.bar(df, x="Latitude", y="Longitude")
        elif(graph == 'line'):
            fig = px.line_geo(df, lat="Latitude", lon="Longitude")
        return fig

    return dash_app.server

