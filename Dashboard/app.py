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
from plotly.subplots import make_subplots
from utils.display_data import get_data

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# Declare Constants

MEASURES = [
    "c1_school_closing",
    "c2_workplace_closing",
    "c3_cancel_public_events",
    "c4_restrictions_on_gatherings",
    "c5_close_public_transport",
    "c6_stay_at_home_requirements",
    "c7_movement_restriction",
    "c8_international_travel",
]

MEASURES_COLORS = {
    "c1_school_closing": {1: "#ffb3d1", 2: "#ff0066", 3: "#99003d"},
    "c2_workplace_closing": {1: "#ffffb3", 2: "#ffff00", 3: "#cccc00"},
    "c3_cancel_public_events": {1: "#ffe0b3", 2: "#ff9900", 3: "#995c00"},
    "c4_restrictions_on_gatherings": {1: "#ffcccc", 2: "#ff0000", 3: "#800000",4: "#4d0000"}, #red
    "c5_close_public_transport": {1: "#99ff99", 2: "#00b300", 3: "#004d00"},
    "c6_stay_at_home_requirements": {1: "#99e6ff", 2: "#00bfff", 3: "#006080"},
    "c7_movement_restriction": {1: "#ecb3ff", 2: "##9900cc", 3: "#4d0066"},
    "c8_international_travel":{1: "##ebebe0", 2: "#c2c2a3", 3: "#7a7a52",4:"#2e2e1f"}
}

MEASURES_NAMES = {
    "c1_school_closing": "School Closing",
    "c2_workplace_closing": "Workplace Closing",
    "c3_cancel_public_events": "Public Events Cancelled",
    "c4_restrictions_on_gatherings": "Restrictions on Gatherings",
    "c5_close_public_transport": "Closing of public transport",
    "c6_stay_at_home_requirements": "Stay At Home",
    "c7_movement_restriction": "Movement Restrictions",
    "c8_international_travel": "International Travel Restrictions"
}

BEHAVIOUR_NAMES={
    "Bij_klachten_blijf_thuis": "Stay Home When Sick",
    "Houd_1_5m_afstand":'Keep 1.5m Distance',
    "Bij_klachten_laat_testen": "Get Tested When Sick",
    "Ontvang_max_bezoekers_thuis":  'Restrict the number of visitors at home',
    "Vermijd_drukke_plekken": "Avoid Crowded Spaces",
    "Was_vaak_je_handen": 'Wash your hands frequently',
    "Zorgen_over_Coronavirus":'Worry about COVID-19',
    "Draag_mondkapje_in_publieke_binnenruimtes":'Wear face mask in public indoor spaces',
    "Hoest_niest_in_elleboog":'Cough in your elbow',
    "Werkt_thuis":'Work from home as much as possible',
    "Avondklok":'Curfew'



}
                                        
                                                

SERIES_NAMES = [{'label':'New Cases', 'value':"cases"},
                {'label': 'Number of Tests', 'value': 'tests'},
                {'label': 'ICU admissions', 'value': 'ICU admissions'}]

SERIES_NAMES2 = {'cases': 'New Cases', 'tests':'Number of Tests', 'ICU admissions':'ICU admissions'}
                

TRANSFORMS_NAMES = [{'label':'Seven Day Average', 'value':"Seven Day Average"},]
DROP_DOWN_STYLE = {'margin-top': '10px', 'margin-left': '10px', 'margin-right': '40px','color': 'black'}

SERIES_PROPERTIES = {
    "cases": {
        "filters": ["Sex","Region","Age group"],
        "transformers": ["Seven Day Average"]
    },
    "tests": {
        "filters":["Region"],
        "transformers": ["Seven Day Average", "Per Positive result"],
    },
    "ICU admissions": {
        "filters": [],
        "transformers": ["Seven Day Average"],
    },
}

MARGIN_SPAN = '15px'
MARGIN_SPAN1 = '10px'

# Load Data
data_folder = pathlib.Path(__file__).parent / "data"
daily_data = pd.read_csv(data_folder / 'daily_data.csv', sep=',')
behaviour_data = pd.read_csv(data_folder / 'behaviour_data.csv', sep=',')

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
                            "",
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
                html.H6("MEASURES LEGEND",className="legend-title"),
                html.A(html.Button('More Info', id='btn-nclicks-1', n_clicks=0, className="button_more"), href='https://github.com/OxCGRT/covid-policy-tracker/blob/master/documentation/codebook.md')
            ]
        ),
        #Content0
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Ul(
                                    [
                                        html.Span('Movements', style={'margin-left': MARGIN_SPAN, 'margin-right': MARGIN_SPAN1}),
                                        html.Li([html.Span(style={'background':'#ecb3ff'})]),
                                        html.Li([html.Span(style={'background':'#9900cc'})]),
                                        html.Li([html.Span(style={'background':'#4d0066'})]),
                                        html.Span('Schools', style={'margin-left':MARGIN_SPAN, 'margin-right': MARGIN_SPAN1}),
                                        html.Li([html.Span(style={'background':'#ffb3d1'})]),
                                        html.Li([html.Span(style={'background':'#ff0066'})]),
                                        html.Li([html.Span(style={'background':'#99003d'})]),
                                        html.Span('Gatherings', style={'margin-left':MARGIN_SPAN, 'margin-right': MARGIN_SPAN1}),
                                        html.Li([html.Span(style={'background':'#ffcccc'})]),
                                        html.Li([html.Span(style={'background':'#ff0000'})]),
                                        html.Li([html.Span(style={'background':'#800000'})]),
                                        html.Li([html.Span(style={'background':'#4d0000'})]),
                                        html.Span('Public Events', style={'margin-left': MARGIN_SPAN, 'margin-right': MARGIN_SPAN1}),
                                        html.Li([html.Span(style={'background':'#ffe0b3'})]),
                                        html.Li([html.Span(style={'background':"#ff9900"})]),
                                        html.Li([html.Span(style={'background':"#995c00"})]),
                                        html.Span('Workplace', style={'margin-left': MARGIN_SPAN, 'margin-right': MARGIN_SPAN1}),
                                        html.Li([html.Span(style={'background':'#ffffb3'})]),
                                        html.Li([html.Span(style={'background':"#ffff00"})]),
                                        html.Li([html.Span(style={'background':"#cccc00"})]),
                                        html.Span('Public Transport', style={'margin-left': MARGIN_SPAN, 'margin-right': MARGIN_SPAN1}),
                                        html.Li([html.Span(style={'background':'#99ff99'})]),
                                        html.Li([html.Span(style={'background':"#00b300"})]),
                                        html.Li([html.Span(style={'background':"#004d00"})]),
                                        html.Span('Stay At Home', style={'margin-left': MARGIN_SPAN, 'margin-right': MARGIN_SPAN1}),
                                        html.Li([html.Span(style={'background':"#99e6ff"})]),
                                        html.Li([html.Span(style={'background':"#00bfff"})]),
                                        html.Li([html.Span(style={'background':"#006080"})]),
                                        html.Span('International Travel', style={'margin-left': MARGIN_SPAN, 'margin-right': MARGIN_SPAN1}),
                                        html.Li([html.Span(style={'background':"#ebebe0"})]),
                                        html.Li([html.Span(style={'background':"#c2c2a3"})]),
                                        html.Li([html.Span(style={'background':"#7a7a52"})]),
                                        html.Li([html.Span(style={'background':"#2e2e1f"})]),       
                                    ]
                                    ,className='legend-labels')

                            ],
                            className='legend-scale'
                        )

                    ]
                    ,className="my-legend"
                    )   
            ],
            className="app__content"
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
                                                    className="our_drop"

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
                                                {'label': 'Public Events Cancelled', 'value': 'c3_cancel_public_events'},
                                                {'label': 'Restrictions on Gathering', 'value': "c4_restrictions_on_gatherings"},
                                                {'label': 'Public Transport Closing', 'value': "c5_close_public_transport"},
                                                {'label': 'Stay At Home', 'value': "c6_stay_at_home_requirements"},
                                                {'label': 'Restrictions on Movement', 'value': "c7_movement_restriction"},
                                                {'label': 'Restrictions on International Travel', 'value': "c8_international_travel"}
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
                                                {'label': 'Stay Home When Sick', 'value': "Bij_klachten_blijf_thuis"},
                                                {'label': 'Keep 1.5m Distance', 'value': "Houd_1_5m_afstand"},
                                                {'label': 'Get Tested When Sick', 'value': "Bij_klachten_laat_testen"},
                                                {'label': 'Restrict the number of visitors at home', 'value': "Ontvang_max_bezoekers_thuis"},
                                                {'label': 'Avoid Crowded Spaces', 'value': "Vermijd_drukke_plekken"},
                                                {'label': 'Wash your hands frequently', 'value': "Was_vaak_je_handen"},
                                                {'label': 'Worry about COVID-19', 'value': "Zorgen_over_Coronavirus"},
                                                {'label': 'Wear face mask in public indoor spaces', 'value': "Draag_mondkapje_in_publieke_binnenruimtes"},
                                                {'label': 'Cough in your elbow', 'value': "Hoest_niest_in_elleboog"},
                                                {'label': 'Work from home as much as possible', 'value': "Werkt_thuis"},
                                                #{'label': '', 'value': "Draag_mondkapje_in_ov"},
                                                {'label': 'Curfew', 'value': "Avondklok"}
                                                ],
                                            style=DROP_DOWN_STYLE,
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
    Input('drop-down-series-1-transform', 'value'),
    Input('drop-down-series-2', 'value'),
    Input('drop-down-series-2-sex', 'value'),
    Input('drop-down-series-2-transform', 'value'),
    Input('drop-down-measure-area', 'value'),
)
def main_graph(series1, sex_series1, transform_1, series2, sex_series2, transform_2, measures):
    filters_1 = {}
    filters_2 = {}

    if series1 and'Sex' in SERIES_PROPERTIES[series1]['filters']:
        filters_1 = {"Sex": sex_series1}
    if series2 and 'Sex' in SERIES_PROPERTIES[series2]['filters']:
        filters_2 = {"Sex": sex_series2}
        
    df = daily_data
    measures_dates = get_measure_dates_dict(daily_data)

    series = get_data(series_1=series1,
                            filters_1=filters_1,
                            transform_1=transform_1,
                            series_2=series2,
                            filters_2=filters_2,
                            transform_2=transform_2
                        )
    dates = series.index
    trace1 = dict(x=dates, type="scatter",)
    trace2 = dict()
    if series1: 
        trace1 = dict(
            type="scatter",
            y=series['series_1'],
            x=dates,
            name= SERIES_NAMES2[series1],
            line={"color": "#f2f2f2"}, 
            line_width=3,
            mode="lines",
            showlegend=True
        )

    if series2: 
        trace2 = dict(
            type="scatter",
            y=series['series_2'],
            x=dates,
            name=SERIES_NAMES2[series2],
            line={"color": "#42C4F7"},
            line_width=3,
            mode="lines",
            showlegend=True

        )
    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(trace1, secondary_y=False)
    if series2:
        fig.add_trace(trace2, secondary_y=True)
    fig.update_layout(plot_bgcolor=app_color["graph_bg"],
                      paper_bgcolor=app_color["graph_bg"],
                      font={"color": "#fff"},
                      height=700,
                      xaxis={'showgrid': False},
                      xaxis2={'showgrid': False},
                      yaxis2 = {'showgrid': False},
                      yaxis={'showgrid': False})
                      # legend_x=0.9)
    if series1: 
        fig.update_yaxes(title_text=SERIES_NAMES2[series1], secondary_y=False)
    if series2: 
        fig.update_yaxes(title_text=SERIES_NAMES2[series2], secondary_y=True)
    
    if measures:
        if series1: 
            max_y_axes = series['series_1'].max()
        elif series2: 
            max_y_axes = series['series_2'].max()
        else:
            max_y_axes=1200

        y_0_count = 0
        for measure in measures:
            y_0 = y_0_count
            y_1 = y_0_count + max_y_axes / len(measures)
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
                                line_width=area['line_width'],
                                layer="below"
                            )

            y_0_count += max_y_axes / len(measures)

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
        line={"color": "white"},
        mode="markers",
        showlegend=False
    )

    trace2 = dict(
        type="scatter",
        y=df['Value'],
        x=df['Date_of_measurement'],
        line = dict(width=3, dash='dot', color='white'),
        name=BEHAVIOUR_NAMES[behaviour]

    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=500,
        # width=1850,
        xaxis =  {'showgrid': False},
        yaxis={'showgrid': False},
        showlegend=True,
        )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    fig.update_xaxes(range=[daily_data.loc[0, 'Date_statistics'], daily_data.reset_index(drop=True).loc[len(daily_data)-1, 'Date_statistics']])
    fig.update_xaxes(showline=True, linecolor="white",linewidth=2)
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
    app.run_server(debug=True,host = '127.0.0.1')
    #app.run_server(host='127.0.0.1', port=8050, debug=True)