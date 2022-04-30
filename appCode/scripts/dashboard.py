from lib2to3.pgen2 import driver
from types import NoneType
import numpy as np
import pandas as pd
import plotly.express as px
import dash
from datetime import date

from dash import dcc, html, Input, Output, dash_table


def create_dashboard(server):

    #setup dash
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
    )


    #upload file
    df = pd.read_excel('appCode/niner-transit-data/Copy of Test Log #2.xlsx')

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
    minTime = min(df['Time'])
    #minTime = pd.to_datetime(minTime)
    #minTime = minDate.strftime("%H/%m/%s")
    maxTime = max(df['Time'])
    #maxTime = pd.to_datetime(maxTime)
    #maxTime = maxTime.strftime("%m/%m/%s")
    print(minTime)
    print(maxTime)

    minDate = min(df['Date'])
    minDate = pd.to_datetime(minDate)
    minDate = minDate.strftime("%m/%d/%Y")
    maxDate = max(df['Date'])
    maxDate = pd.to_datetime(maxDate)
    maxDate = maxDate.strftime("%m/%d/%Y")
    print(minDate)
    print(maxDate)

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
    fig = px.line_geo(df, lat="Latitude", lon="Longitude")

    #tests
    #print(stopNames)
    #print(filterOptions)

    #html layout
    dash_app.layout = html.Div(children=[

#filter selections
        #html.Div(id='dateSelection', children=[
         #   dcc.DatePickerRange(
          #      id='dateRange',
           #     min_date_allowed=date()
            #    max_date_allowed=
            #)
        #], style={'display':'block'}),

        html.Div(id='routeSelections', children=[
            dcc.RadioItems(
                id='routes',
                options = [{'label': i, 'value': i} for i in ['Silver', 'Gold', 'Green', nanRoute]],
                value= 'Silver'
            )
        ], style={'display':'block'}),
    
        html.Div(id='stopSelections', children=[
            dcc.RadioItems(
                id='stops',
                options = stopNames,
                value= stopNames[0]
            )
        ], style={'display':'block'}),

        html.Div(id='busSelections', children=[
            dcc.RadioItems(
                id='buses',
                options = busNumbers,
                value= busNumbers[0]
            )
        ], style={'display':'block'}),

        html.Div(id='driverSelections', children=[
            dcc.RadioItems(
                id='drivers',
                options = driverIDs,
                value= driverIDs[0]
            )
        ], style={'display':'block'}),

    #Dropdowns for graph, filter, and x/y
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
                value = 'Route',
                placeholder='Choose Filter'
            ),
            dcc.Dropdown(
                id='x-axis-dd',
                options=sortOptions,
                value = 'Latitude',
                placeholder='Choose X Variable'
            ),
            dcc.Dropdown(
                id='y-axis-dd',
                options=sortOptions,
                value = 'Longitude',
                placeholder='Choose Y Variable'
            )
        ]),
    #graph
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
        Input(component_id='drivers', component_property='value'),
        Input(component_id='x-axis-dd', component_property='value'),
        Input(component_id='y-axis-dd', component_property='value')
    )
    #The parameters below correspond to the Input's above respectively
    def updateGraph(graph, filter, route, stop, bus, driver, xaxis, yaxis):
        dfNaN = pd.DataFrame()
        col1 = 'Count'
        col2 = 'Parameters'
        dfNaN[col1] = ""
        dfNaN[col2] = ""
        temp = []
        print(df)
        
        if(filter == 'Route'):
            if route != nanRoute:
                dff = df[df[filter] == route]
            else:
                dff = df[df[filter].isna()]
            if xaxis != None and yaxis != None:
                temp = dff.isna().sum(axis=0).to_numpy()
                dfNaN[col1] = temp.tolist()
                dfNaN[col2] = colNames
                print(dfNaN)

        elif(filter == 'Stop'):
            if stop != nanStop:
                dff = df[df[filter] == stop]
            else:
                dff = df[df[filter].isna()]
            if xaxis != None and yaxis != None:
                temp = dff.isna().sum(axis=0).to_numpy()
                dfNaN[col1] = temp.tolist()
                dfNaN[col2] = colNames
                print(dfNaN)

        elif(filter == 'Bus'):
            if bus != nanBus:
                dff = df[df[filter] == bus]
            else:
                dff = df[df[filter].isna()]
            if xaxis != None and yaxis != None:
                temp = dff.isna().sum(axis=0).to_numpy()
                dfNaN[col1] = temp.tolist()
                dfNaN[col2] = colNames
                print(dfNaN)

        elif(filter == 'Driver ID'):
            if driver != nanRoute:
                dff = df[df[filter] == driver]
            else:
                dff = df[df[filter].isna()]
            if xaxis != None and yaxis != None:
                temp = dff.isna().sum(axis=0).to_numpy()
                dfNaN[col1] = temp.tolist()
                dfNaN[col2] = colNames
                print(dfNaN)

        if(graph == 'Bar'):
            fig = px.bar(dfNaN, x=col2, y=col1)
        elif(graph == 'Line'):
            fig = px.line(dff, x=xaxis, y=yaxis)
        elif(graph == 'Map'):
            fig = px.line_geo(dff, lat=xaxis, lon=yaxis)
        elif(graph == 'Pie'):
            fig = px.pie(values=[xaxis, yaxis], names=[xaxis, yaxis])
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

