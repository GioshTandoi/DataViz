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


MEASURES_COLORS = {'c1_school_closing': '#b3c3dd', 'c2_workplace_closing': '#ddb3c3', 'c3_cancel_public_events': '#c3ddb3'}

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
    measures_dates = get_measure_dates_dict(daily_data)

    areas_dicts = []

    for measure in measures:
        for i in range(int(len(measures_dates[measure]) / 2)):
            this_dates = [str(measures_dates[measure][i + i]), str(measures_dates[measure][i + i + 1])]
            areas_dicts.append(get_plot_area_dict(this_dates, measure, MEASURES_COLORS[measure]))

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
    
    for area in areas_dicts:
        fig.add_vrect(x0=area['x0'],
                      x1=area['x1'],
                      annotation_text=area['annotation_text'],
                      fillcolor=area['fillcolor'],
                      annotation_position=area['annotation_position'],
                      annotation=area['annotation'],
                      opacity=area['opacity'],
                      line_width=area['line_width'])
    

    return fig



def get_plot_area_dict(dates, measure, color):
    return dict(
        x0=dates[0],
        x1=dates[1],
        annotation_text=measure,
        fillcolor=color,
        annotation_position="top left",
        annotation=dict(font_size=20,font_family="Times New Roman"),
        opacity=0.25,
        line_width=0
    )


def find_start_end_dates(measure,df):
    dates=[]
    for elem in range(len(df[measure])-1):
        if  df[measure][elem]!=df[measure][elem+1]:
            dates.append(df['Date_statistics'][elem])
    if len(dates)%2==1:
        dates.append(pd.to_datetime('2021-02-16 00:00:00'))
    return dates


def get_measure_dates_dict(df):

    measures=['c1_school_closing',
        'c2_workplace_closing', 'c3_cancel_public_events',
        'c4_restrictions_on_gatherings', 'c5_close_public_transport',
        'c6_stay_at_home_requirements', 'c7_movement_restriction',
        'c8_international_travel', 'h1_public_information_campaigns',
        'h2_testing_policy', 'h3_contact_tracing', 'h6_facial_coverings',
        'h7_vaccination_policy', 'h8_protection_of_elderly_people']
    measure_dates=dict()

    for measure in measures:
        measure_dates[measure] = find_start_end_dates(measure, df)
    
    return measure_dates


if __name__ == "__main__":
    app.run_server(debug=True)