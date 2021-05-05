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
from utils.display_data import get_data

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State


# Declare Constants
MEASURES_COLORS = {
    "c1_school_closing": {1: "#bbc9e0", 2: "#cad5e7", 3: "#d9e1ee"},
    "c2_workplace_closing": {1: "#bbc9e0", 2: "#cad5e7", 3: "#d9e1ee"},
    "c3_cancel_public_events": {1: "#bbc9e0", 2: "#cad5e7"},

}
MEASURES = [
    "c1_school_closing",
    "c2_workplace_closing",
    "c3_cancel_public_events",
    "c4_restrictions_on_gatherings",
    "c5_close_public_transport",
    "c6_stay_at_home_requirements",
    "c7_movement_restriction",
    "c8_international_travel",
    "h1_public_information_campaigns",
    "h2_testing_policy",
    "h3_contact_tracing",
    "h6_facial_coverings",
    "h7_vaccination_policy",
    "h8_protection_of_elderly_people",
]

MEASURES_NAMES = {'c1_school_closing': 'School Closing', 'c2_workplace_closing':'Workplace Closing', 'c3_cancel_public_events': 'Public Events Cancelled' }
SERIES_NAMES = [{'label':'New Cases', 'value':"cases"},]
TRANSFORMS_NAMES = [{'label':'Seven Day Average', 'value':"Seven Day Average"},]
DROP_DOWN_STYLE = {'margin-top': '10px', 'margin-left': '10px', 'margin-right': '40px'}

# Load Data
daily_data = pd.read_csv('data/daily_data.csv', sep=',')
behaviour_data = pd.read_csv('data/behaviour_data.csv', sep=',')

# Initialize App
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}


# Declare App Structure 
app.layout = html.Div(
    [
        # Header
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
        # Content 1
        html.Div(
            [
                # Series Graph
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
                # Selection box
                html.Div(
                    [
                        
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H5(
                                            "SELECT DATA",
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.Hr(style={'margin-bottom': '0px', 'margin-top': '15px'}),
                                        html.H6(
                                            "Series 1:",
                                            className="graph__title",
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Content:",
                                                    className="graph__sub__title",
                                                ),
                                                dcc.Dropdown(
                                                    id='drop-down-series-1',
                                                    options=SERIES_NAMES,
                                                    value="cases",
                                                    style=DROP_DOWN_STYLE,
                                                    clearable=True,
                                                ),
                                                html.P(
                                                    "Filters:",
                                                    className="graph__sub__title",
                                                ),
                                                dcc.Checklist(
                                                    id='drop-down-series-1-sex',
                                                    options=[
                                                        {'label': 'Males', 'value': 'Male'},
                                                        {'label': 'Females', 'value': 'Female'},
                                                    ],
                                                    inputClassName="auto__checkbox",
                                                    labelClassName="auto__label",
                                                    style={'margin-left': '25px', 'margin-right': '25px'},
                                                    labelStyle={'display': 'inline-block'},
                                                    value=['Male', 'Female']
                                                ),
                                                html.P(
                                                    "Transforms:",
                                                    className="graph__sub__title",
                                                ),
                                                dcc.Dropdown(
                                                    id='drop-down-series-1-transform',
                                                    options=TRANSFORMS_NAMES,
                                                    #value="Seven Day Average",
                                                    style=DROP_DOWN_STYLE,
                                                    clearable=True,
                                                )
                                            ]
                                        )
                                    ],
                                ),
                                html.Div(
                                    [
                                        html.Hr(style={'margin-bottom': '0px', 'margin-top': '15px'}),
                                        html.H6(
                                            "Series 2:",
                                            className="graph__title",
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Content:",
                                                    className="graph__sub__title",
                                                ),
                                                dcc.Dropdown(
                                                    id='drop-down-series-2',
                                                    options=SERIES_NAMES,
                                                    #value="cases",
                                                    style=DROP_DOWN_STYLE,
                                                    clearable=True,
                                                ),
                                                html.P(
                                                    "Filters:",
                                                    className="graph__sub__title",
                                                ),
                                                dcc.Checklist(
                                                    id='drop-down-series-2-sex',
                                                    options=[
                                                        {'label': 'Males', 'value': 'Male'},
                                                        {'label': 'Females', 'value': 'Female'},
                                                    ],
                                                    inputClassName="auto__checkbox",
                                                    labelClassName="auto__label",
                                                    style={'margin-left': '25px', 'margin-right': '25px'},
                                                    labelStyle={'display': 'inline-block'},
                                                    value=['Male', 'Female']
                                                ),
                                                html.P(
                                                    "Transforms:",
                                                    className="graph__sub__title",
                                                ),
                                                dcc.Dropdown(
                                                    id='drop-down-series-2-transform',
                                                    options=TRANSFORMS_NAMES,
                                                    #value="Seven Day Average",
                                                    style=DROP_DOWN_STYLE,
                                                    clearable=True,
                                                )
                                            ]
                                        )
                                    ],
                                ),
                                html.Div(
                                    [
                                        html.Hr(style={'margin-bottom': '0px', 'margin-top': '15px'}),
                                        html.H6(
                                            "Measure:",
                                            className="graph__title",
                                        ),
                                        dcc.Dropdown(
                                            id='drop-down-measure-area',
                                            options=[
                                                {'label': 'School Closing at all Levels', 'value': 'c1_school_closing'},
                                                {'label': 'Closing of all-but-essential Workplaces', 'value': 'c2_workplace_closing'},
                                                {'label': 'Public Events Cancelled', 'value': 'c3_cancel_public_events'}
                                            
                                            ],
                                            #value='c1_school_closing',
                                            clearable=True,
                                            multi=True,
                                            style=DROP_DOWN_STYLE
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
        ),
        # Content 2
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6("Measures compliance and worry about COVID", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="g2",
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
                                        html.H5(
                                            "SELECT BEHAVIOUR",
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            "Measure:",
                                            className="graph__title",
                                        ),
                                        dcc.Dropdown(
                                            id='drop-down-4',
                                            options=[
                                                {   'label': 'Stay Home When Sick', 'value': "Bij_klachten_blijf_thuis"},
                                                    {'label': 'Keep 1.5m Distance', 'value': "Houd_1_5m_afstand"},
                                            ],
                                            value="Bij_klachten_blijf_thuis"
                                        ),
                                    ],
                                ),
                            ],
                            className="graph__container first",
                        ),
                    ],
                    className="one-third column histogram__direction",
                )
            ],
            className="app__content"),
    ],
    className="app__container"
)

# Define Callbacks and Utility Functions
@app.callback(
    Output("g1", "figure"),
    Input('drop-down-series-1', 'value'),
    Input('drop-down-series-1-sex', 'value'),
    Input('drop-down-series-2-transform', 'value'),
    Input('drop-down-series-2', 'value'),
    Input('drop-down-series-2-sex', 'value'),
    Input('drop-down-series-2-transform', 'value'),
    Input('drop-down-measure-area', 'value'),
)
def main_graph(series1, sex_series1, transform_1, series2, sex_series2, transform_2, measures):
   
    df = daily_data
    measures_dates = get_measure_dates_dict(daily_data)

    series = get_data(series_1=series1,
                            filters_1={"Sex": sex_series1},
                            transform_1=transform_1,
                            series_2=series2,
                            filters_2={"Sex": sex_series2},
                            transform_2=transform_2)
    dates = series.index
    trace1 = dict(x=dates, type="scatter",)
    trace2 = dict()
    if series1: 
        trace1 = dict(
            type="scatter",
            y=series['series_1'],
            x=dates,
            name= [x['label'] if x['value'] == series1 else '' for x in SERIES_NAMES][0],
            line={"color": "#42C4F7"},
            mode="lines",
        )

    if series2: 
        trace2 = dict(
            type="scatter",
            y=series['series_2'],
            x=dates,
            name=[x['label'] if x['value'] == series2 else '' for x in SERIES_NAMES][0],
            line={"color": "#43F7EC"},
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
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    
    if measures:
        y_0_count = 0
        for measure in measures:
            print(f"y_0_count: {y_0_count}")
            y_0 = y_0_count
            y_1 = y_0_count + 12000 / len(measures)
            print(f"y_0: {y_0}")
            print(f"y_1: {y_1}")
            areas_dicts = {}
            for level in np.sort(daily_data[measure].unique()):
                this_areas_dicts = []
                if level == 0: 
                    continue
                else: 
                    for i in range(int(len(measures_dates[measure][level]) / 2)):
                        this_dates = [str(measures_dates[measure][level][i + i]), str(measures_dates[measure][level][i + i + 1])]
                        this_areas_dicts.append(get_plot_area_dict(this_dates, measure, MEASURES_COLORS[measure][level]))
                    areas_dicts[level] = this_areas_dicts

            for level in np.sort(daily_data[measure].unique()):

                if level == 0: 
                    continue
                else: 
                    for area in areas_dicts[level]:
                        fig.add_shape(type="rect",
                                x0=area['x0'],
                                x1=area['x1'],
                                y0=y_0,
                                y1=y_1,
                                fillcolor=area['fillcolor'],
                                opacity=area['opacity'],
                                line_width=area['line_width']
                            )

            y_0_count += 12000 / len(measures)

    return fig


@app.callback(
    Output("g2", "figure"), Input('drop-down-4', 'value')
)
def behaviour_plot(behaviour):
    df = behaviour_data.loc[lambda d: d.Indicator == behaviour].sort_values('Date_of_measurement')

    fig = go.Figure()

    trace1 = dict(
        type="scatter",
        y=df['Value'],
        x=df['Date_of_measurement'],
        #line={"color": "#42C4F7"},
        mode="markers",
    )

    trace2 = dict(
        type="scatter",
        y=df['Value'],
        x=df['Date_of_measurement'],
        #line={"color": "#42C4F7"},
        line = dict(width=2, dash='dot'),
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=400,
        xaxis =  {'showgrid': False},
        yaxis={'showgrid': False},
        showlegend=False,
        )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    fig.update_xaxes(range=[daily_data.loc[0, 'Date_statistics'], daily_data.reset_index(drop=True).loc[len(daily_data)-1, 'Date_statistics']])
    fig.update_yaxes(title='Percentage of Positive Respondents')
    fig.update_traces(marker_line_width=2, marker_size=11)

    return fig


def get_plot_area_dict(dates, measure, color):
    return dict(
        x0=dates[0],
        x1=dates[1],
        fillcolor=color,
        opacity=0.50,
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
    measure_dates = {}

    for measure in MEASURES: 
        measure_dates[measure] = {}
        for level in np.sort(daily_data[measure].unique()):
            if level ==0: 
                continue
            else: 
                measure_level = pd.DataFrame()
                measure_level[measure]=make_measures_0_1(daily_data[measure], level)
                measure_level['Date_statistics']=daily_data['Date_statistics']
                measure_dates[measure][level] = find_start_end_dates(measure, measure_level)
    return measure_dates


def make_measures_0_1(column, max_level):
    column=np.where(column==max_level,column, 0)
    column=np.where(column==0,column, 1)
    return column


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)