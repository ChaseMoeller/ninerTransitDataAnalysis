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
    sortOptions = []
    filterOptions = []
    stopNames = []
    busNumbers = []

    for col in df.columns:
        if col != 'Route' and col != 'Stop' and col != 'Bus':
            sortOptions.append({'label':'{}'.format(col, col),
            'value':col})
        else:
            filterOptions.append({'label':'{}'.format(col, col),
            'value':col})


    npStop = df['Stop'].to_numpy()
    npBus = df['Bus'].to_numpy()
    
    for stop in npStop:
        if stop not in stopNames:
            stopNames.append(stop)

    for bus in npBus:
        if bus not in busNumbers:
            busNumbers.append(bus)

    opt = stopNames
    #default graph
    fig = px.line_geo(df, lat="Latitude", lon="Longitude")
    #options




    print(stopNames)
    print(filterOptions)
    #html layout
    dash_app.layout = html.Div(children=[

    html.Div([
        dcc.RadioItems(
            id='routes',
            options = [{'label': i, 'value': i} for i in ['Silver', 'Gold', 'Green']],
            value= 'Silver'
        ),
        dcc.RadioItems(
            id='stops',
            options = stopNames,
            value= stopNames[0]
        ),
        dcc.RadioItems(
            id='buses',
            options = busNumbers,
            value= busNumbers[0]
        )

    ]),
    html.Div([
        dcc.Dropdown(
            id='graph-type',
            options = [{'label': i, 'value': i} for i in ['Map', 'Bar', 'Line', 'Pie']],
            value='Map',
            placeholder='Choose Graph Type'
        ),
        dcc.Dropdown(
            id='filter-dd',
            options=filterOptions,
            placeholder='Choose Filter'
        ),
        dcc.Dropdown(
            id='x-axis-dd',
            options=sortOptions,
            placeholder='Choose X Variable'
        ),
        dcc.Dropdown(
            id='y-axis-dd',
            options=sortOptions,
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
        Input(component_id='filter-dd', component_property='value'),
        Input(component_id='routes', component_property='value'),
        Input(component_id='stops', component_property='value'),
        Input(component_id='buses', component_property='value'),
        Input(component_id='x-axis-dd', component_property='value'),
        Input(component_id='y-axis-dd', component_property='value')
    )
    #The parameters below correspond to the Input's above respectively
    def update_graph(graph, filter, routes, stops, buses, xaxis, yaxis):

        if(filter == 'Route'):
            dff = df[df[filter] == routes]
        elif(filter == 'Stop'):
            dff = df[df[filter] == stops]
        elif(filter == 'Bus'):
            dff = df[df[filter] == buses]

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

