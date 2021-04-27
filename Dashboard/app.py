import os
import pathlib
import numpy as np
import pandas as pd
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State


daily_data = pd.read_csv('daily_data.csv', sep = ',')

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H4("CORONA DASHBOARD", className="app__header__title"),
                        html.P(
                            "This is a dashboard about corona, ejoy. ",
                            className="app__header__title--grey",
                        )
                    ],
                    className="app__header__desc",
                ) 
            ],
            className="app__header"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6("Corona Insights", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="g1",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),

                    ],
                    className="two-thirds column wind__speed__container",
                ),
                html.Div(
                    [
                        # selection box
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "SELECT DATA",
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id='drop-down-1',
                                            options=[
                                                {'label': 'New Cases', 'value': "Number of new cases"},
                                            ],
                                            value="Number of new cases"
                                        ),
                                    ],
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id='drop-down-2',
                                            options=[
                                                {'label': 'School Closing', 'value': 'c1_school_closing'},
                                                {'label': 'Work Place Closing', 'value': 'c2_workplace_closing'},
                                                {'label': 'Public Events Cancelled', 'value': 'c3_cancel_public_events'}
                                                
                                            ],
                                            value=['c1_school_closing'],
                                            multi=True
                                        )
                                    ]
                                )

                             
                            ],
                            className="graph__container first",
                        ),
                    ],
                    className="one-third column histogram__direction",
                )

            ],
            className="app__content",
        )
    ],
    className="app__container"
)

@app.callback(
    Output("g1", "figure"), Input('drop-down-1', 'value'), Input('drop-down-2', 'value')
)
def main_graph(series_name, measures):

    df = daily_data

    
    trace = dict(
        type="scatter",
        y=df[series_name],
        x=df['Date_statistics'],
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=700,
        xaxis =  {'showgrid': False},
        yaxis = {'showgrid': False}
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.add_vrect(x0="2020-03-15", x1="2020-05-10",
        annotation_text="decline", annotation_position="top left",
        annotation=dict(font_size=20, font_family="Times New Roman"),
        fillcolor="yellow", opacity=0.25, line_width=0)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)