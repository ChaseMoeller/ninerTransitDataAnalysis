import numpy as np
import pandas as pd
import plotly.express as px
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc

def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
    )

    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas"],
        "Amount": [4,1,2],
        "City":["SF", "NY", "LA"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    dash_app.layout = html.Div(children=[

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
    
    return dash_app.server


#def init_callbacks(dash_app):

    #@app.callback(

    #)
    #def update_graph(rows):