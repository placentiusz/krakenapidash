"""Simple usage of Kraken api and Dash"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import libs.apiCall

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div(
    children=[
        html.H1(children="Hello Kraken"),
        html.Div(
            children="""Dash: Simple public Kraken API visualisation."""
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="currency",
                    options=[
                        {"label": i, "value": i}
                        for i in [
                            "monero",
                            "polkadot",
                            "bitcoin",
                            "litecoin",
                            "Ethereum",
                        ]
                    ],
                    clearable=False,
                    value="monero",
                ),
            ],
            style={"width": "20%", "display": "inline-block"},
        ),
        dcc.Graph(id="graph-api"),
        dcc.Graph(id="graph-volume", config={"displayModeBar": True}),
        dcc.Interval(
            id="interval-component",
            interval=30 * 1000,  # in milliseconds
            n_intervals=0,
        ),
    ]
)


@app.callback(
    Output("graph-api", "figure"),
    [Input("currency", "value"), Input("interval-component", "n_intervals")],
)
def update_figure_main(currency, unused):
    """Update grap-api"""
    filtered_df = libs.apiCall.getData(currency)

    return {
        "data": [
            {
                "x": filtered_df["datetime"],
                "y": filtered_df["close"],
                "name": "Close",
                "mode": "lines",
                "opacity": 0.1,
            },
            {
                "x": filtered_df["datetime"],
                "y": filtered_df["filter"],
                "name": "Filtered",
                "mode": "lines",
            },
            {
                "x": filtered_df["datetime"],
                "y": filtered_df["min"],
                "name": "Local min",
                "mode": "markers",
            },
            {
                "x": filtered_df["datetime"],
                "y": filtered_df["max"],
                "name": "Local max",
                "mode": "markers",
            },
            {
                "x": filtered_df["datetime"],
                "y": filtered_df["maxvol"],
                "name": "Volume 3xmean",
                "mode": "markers",
            },
        ],
        "layout": {
            "autosize": True,
            "margin": {"l": 50, "b": 30, "r": 10, "t": 10},
            "annotations": [
                {
                    "x": 0,
                    "y": 0.85,
                    "xanchor": "left",
                    "yanchor": "bottom",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "align": "left",
                    "bgcolor": "rgba(255, 255, 255, 0.5)",
                    "text": "Confirmed in {}".format("Api"),
                }
            ],
            "legend": {"orientation": "h"},
            "yaxis": {"type": "linear"},
            "xaxis": {
                "showgrid": False,
                "range": [filtered_df["datetime"].min(), filtered_df["datetime"].max()],
            },
        },
    }


@app.callback(
    Output("graph-volume", "figure"),
    [Input("currency", "value"), Input("interval-component", "n_intervals")],
)
def update_figure(currency, unused):
    """Update graph-volume"""
    filtered_df = libs.apiCall.getData(currency)

    return {
        "data": [
            {
                "x": filtered_df["datetime"],
                "y": filtered_df["volume"],
                "marker": {"color": filtered_df["color"]},
                "name": "Volume",
                "type": "bar",
            }
        ],
        "layout": {
            "autosize": True,
            "margin": {"l": 50, "b": 30, "r": 10, "t": 10},
            "annotations": [
                {
                    "x": 0,
                    "y": 0.85,
                    "xanchor": "left",
                    "yanchor": "bottom",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "align": "left",
                    "bgcolor": "rgba(255, 255, 255, 0.5)",
                    "text": "Confirmed in {}".format("Api"),
                }
            ],
            "legend": {"orientation": "h"},
            "yaxis": {"type": "linear"},
            "xaxis": {
                "showgrid": False,
                "range": [filtered_df["datetime"].min(), filtered_df["datetime"].max()],
            },
        },
    }


if __name__ == "__main__":
    app.run_server(debug=True)
