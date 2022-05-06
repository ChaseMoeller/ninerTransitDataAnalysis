import os
import numpy as np
import pandas as pd
import plotly.express as px
import dash
from datetime import date, datetime

from dash import dcc, html, Input, Output, dash_table


def create_dashboard(server):

    #setup dash
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

    #declare arrays
    nanRoute = 'Route NaN' 
    nanStop = 'Stop NaN'
    nanBus = 'Bus NaN'
    nanDriver = 'Driver NaN'
    sortOptions = []
    filterOptions = []
    stopNames = []
    busNumbers = []
    driverIDs=[]
    colNames = []

    for col in df.columns:
        colNames.append(col)

    #load arrays
    for col in colNames:
        if col != 'Route' and col != 'Stop' and col != 'Bus' and col != 'Driver ID':
            sortOptions.append({'label':'{}'.format(col, col),
            'value':col})
        else:
            filterOptions.append({'label':'{}'.format(col, col),
            'value':col})

    npStop = df['Stop']
    npBus = df['Bus']
    npDriver = df['Driver ID']
    count = 0
    for stop in npStop:
        if pd.notna(stop):
            if stop not in stopNames:
                stopNames.append(stop)
    stopNames.append(nanStop)

    for id in npDriver:
        if pd.notna(id):
            if id not in driverIDs:
                driverIDs.append(id)
    driverIDs.append(nanDriver)

    for bus in npBus:
        if pd.notna(bus):
            if bus not in busNumbers:
                busNumbers.append(bus)
    busNumbers.append(nanBus)


    #load default graph
    fig = px.bar(df, x="Latitude", y="Longitude")

    #html layout
    dash_app.layout = html.Div(children=[

    #Data Upload
    html.H1("Visualization Page", className='title', style={'font-family':'Arial', 'text-align':'center'}),
    html.H4('Files Available:', className='list-title', style={'font-family':'Arial'}),
    html.Div(id="folder-files", className='files'),
    html.H2('Select your file:', className='selector-title', style={'font-family':'Arial'}),
    html.Div(controls), 
    

#filter selections
        html.H4('Select the Column Type you would like to initially filter by:', className='selector-title', style={'font-family':'Arial'}),
        
        #Dropdowns for graph, filter, and x/y
        html.Div([
            dcc.Dropdown(
                id='filter-dd',
                options=filterOptions,
                placeholder='Choose Filter'
            ),
        ]),

        html.H5('Select specific data you would like:', className='radio-title', style={'font-family':'Arial'}),

        html.Div(id='routeSelections', children=[
            dcc.Dropdown(
                id='routes',
                options = [{'label': i, 'value': i} for i in ['Silver', 'Gold', 'Green', nanRoute]],
                value='Silver'

            )
        ], style={'display':'block'}),
    
        html.Div(id='stopSelections', children=[
            dcc.Dropdown(
                id='stops',
                options = stopNames,
                value=stopNames[0]

            )
        ], style={'display':'block'}),

        html.Div(id='busSelections', children=[
            dcc.Dropdown(
                id='buses',
                options = busNumbers,
                value = busNumbers[0]

            )
        ], style={'display':'block'}),

        html.Div(id='driverSelections', children=[
            dcc.Dropdown(
                id='drivers',
                options = driverIDs,
                value= driverIDs[0]
            )
        ], style={'display':'block'}),
        
    
    #graph
        html.Div([
            dcc.Graph(
                id='graph-1',
                figure=fig
            )
        ])
    ])
    
    @dash_app.callback(Output("folder-files", "children"), Input("dropdown", "value"))
    def list_all_files(folder_name):
        # This is relative, but you should be able
        # able to provide the absolute path too
        file_names = os.listdir(folder_name)
        file_list = html.Ul([html.Li(file) for file in file_names])
        return file_list

    @dash_app.callback(
        Output(component_id='graph-1', component_property='figure'),
        Input(component_id='filter-dd', component_property='value'),
        Input(component_id='routes', component_property='value'),
        Input(component_id='stops', component_property='value'),
        Input(component_id='buses', component_property='value'),
        Input(component_id='drivers', component_property='value'),
    )

    #The parameters below correspond to the Input's above respectively
    def updateGraph(filter, route, stop, bus, driver):
        dfNaN = pd.DataFrame()
        col1 = 'Count'
        col2 = 'Parameters'
        dfNaN[col1] = ""
        dfNaN[col2] = ""
        temp = []
        print(df)
        dff = df
        
        if(filter == 'Route'):
            if route != nanRoute:
                dff = df[df[filter] == route]
            else:
                dff = df[df[filter].isna()]
            temp = dff.isna().sum(axis=0).to_numpy()
            dfNaN[col1] = temp.tolist()
            dfNaN[col2] = colNames
            print(dfNaN)

        elif(filter == 'Stop'):
            if stop != nanStop:
                dff = df[df[filter] == stop]
            else:
                dff = df[df[filter].isna()]
            temp = dff.isna().sum(axis=0).to_numpy()
            dfNaN[col1] = temp.tolist()
            dfNaN[col2] = colNames
            print(dfNaN)

        elif(filter == 'Bus'):
            if bus != nanBus:
                dff = df[df[filter] == bus]
            else:
                dff = df[df[filter].isna()]
            temp = dff.isna().sum(axis=0).to_numpy()
            dfNaN[col1] = temp.tolist()
            dfNaN[col2] = colNames
            print(dfNaN)

        elif(filter == 'Driver ID'):
            if driver != nanRoute:
                dff = df[df[filter] == driver]
            else:
                dff = df[df[filter].isna()]
            temp = dff.isna().sum(axis=0).to_numpy()
            dfNaN[col1] = temp.tolist()
            dfNaN[col2] = colNames
            print(dfNaN)

        fig = px.bar(dfNaN, x=col2, y=col1)

        return fig

    @dash_app.callback(
        Output(component_id='routeSelections', component_property='style'),
        Output(component_id='stopSelections', component_property='style'),
        Output(component_id='busSelections', component_property='style'),
        Output(component_id='driverSelections', component_property='style'),
        Input(component_id='filter-dd', component_property='value')
    )
    def updateFilterSelections(filter):
        if(filter=='Route'):
            return {'display':'block'}, {'display':'none'}, {'display':'none'}, {'display':'none'}
        elif(filter=='Stop'):
            return {'display':'none'}, {'display':'block'}, {'display':'none'}, {'display':'none'}
        elif(filter=='Bus'):
            return {'display':'none'}, {'display':'none'}, {'display':'block'}, {'display':'none'}
        elif(filter=='Driver ID'):
            return {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'block'}
        return {'display':'block'}, {'display':'none'}, {'display':'none'}, {'display':'none'} #show route selection if anything fails

    return dash_app.server

