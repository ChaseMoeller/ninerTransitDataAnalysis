import numpy as np
import pandas as pd
import plotly.express as px
import dash

from dash import dcc, html, Input, Output, dash_table


def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
    )

    #upload file
    df = pd.read_excel('appCode/niner-transit-data/Untitled spreadsheet-2.xlsx')
    

    #default graph
    fig = px.line_geo(df, lat="Latitude", lon="Longitude")
    #options
    options = []

    for col in df.columns:
        if col != 'Route' and col != 'Stop':
            options.append({'label':'{}'.format(col, col),
            'value':col})
        
    npStop = df['Stop'].to_numpy()
    stopNames = []
    for stop in npStop:
        if stop not in stopNames:
            stopNames.append(stop)

    print(stopNames)
    #html layout
    dash_app.layout = html.Div(children=[

    html.Div([
        dcc.RadioItems(
            ['Silver', 'Gold', 'Green'],
            'Silver',
            id='routes'
        )
    ]),
    html.Div([
        dcc.Dropdown(
            ['Map', 'Bar', 'Line', 'Pie'],
            id='graph-type',
            placeholder='Choose Graph Type'
        ),
        dcc.Dropdown(
            id='x-axis-dd',
            options=options,
            placeholder='Choose X Variable'
        ),
        dcc.Dropdown(
            id='y-axis-dd',
            options=options,
            placeholder='Choose Y Variable'
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
        Input(component_id='x-axis-dd', component_property='value'),
        Input(component_id='y-axis-dd', component_property='value')
    )
    #The parameters below correspond to the Input's above respectively
    def update_graph(graph, routes, xaxis, yaxis):

        dff = df[df['Route'] == routes]

        
        if(graph == 'Bar'):
            fig = px.bar(dff, x=xaxis, y=yaxis)
        elif(graph == 'Line'):
            fig = px.line(dff, x=xaxis, y=yaxis)
        elif(graph == 'Map'):
            fig = px.line_geo(dff, lat=xaxis, lon=yaxis)
        elif(graph == 'Pie'):
            fig = px.pie(values=[xaxis, yaxis], names=[xaxis, yaxis])
        return fig

    return dash_app.server

