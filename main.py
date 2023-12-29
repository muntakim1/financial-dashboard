from datetime import datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from dash import dcc, html
from dash.dependencies import Input, Output

# Load external stylesheets from Dash Bootstrap Components
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Financial Dashboard"
# Layout of the dashboard
app.layout = html.Div(
    [
        dbc.Navbar(
            [
                dbc.Container(
                    [
                        dbc.NavbarBrand("Financial Dashboard", href="#"),
                        dbc.Nav(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Label(
                                                    "Select Stock Symbol:",
                                                    style={"color": "white"},
                                                ),
                                                dcc.Input(
                                                    id="stock-input",
                                                    type="text",
                                                    value="AAPL",
                                                    style={"height": "50px"},
                                                ),
                                            ],
                                            md=4,
                                        ),
                                        dbc.Col(
                                            [
                                                html.Label(
                                                    "Select Date Range:",
                                                    style={"color": "white"},
                                                ),
                                                dcc.DatePickerRange(
                                                    id="date-picker",
                                                    start_date=(
                                                        datetime.now()
                                                        - timedelta(days=365)
                                                    ).date(),
                                                    end_date=datetime.now().date(),
                                                ),
                                            ],
                                            md=6,
                                        ),
                                    ],
                                    class_name="mt-1",
                                    justify="center",
                                ),
                            ],
                            className="ml-auto",
                            navbar=True,
                        ),
                    ]
                )
            ],
            color="dark",
            dark=True,
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="trends-graph"), md=8),
                dbc.Col(dcc.Graph(id="bar-graph"), md=4),
            ],
            class_name="g-0",
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="statistical-info")),
        ),
    ],
)


# Callbacks to update graphs based on user inputs
@app.callback(
    [
        Output("trends-graph", "figure"),
        Output("bar-graph", "figure"),
        Output("statistical-info", "figure"),
    ],
    [
        Input("stock-input", "value"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
    ],
)
def update_graphs(stock_symbol, start_date, end_date):
    # Download historical stock data using yfinance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Trends Graph (Candlestick)
    trends_graph = go.Figure(
        data=[
            go.Candlestick(
                x=stock_data.index,
                open=stock_data["Open"],
                high=stock_data["High"],
                low=stock_data["Low"],
                close=stock_data["Close"],
            )
        ]
    )
    trends_graph.update_layout(
        title=f"{stock_symbol} Trends",
    )

    # Bar Graph (Volume)
    bar_graph = px.bar(
        stock_data,
        x=stock_data.index,
        y="Volume",
        title=f"{stock_symbol} Volume",
    )

    # Statistical Information
    statistical_info = px.scatter(
        stock_data.reset_index(),
        x="Date",
        y="Close",
        title=f"{stock_symbol} Closing Price",
        labels={"Close": "Closing Price"},
        trendline="ols",
    )

    return trends_graph, bar_graph, statistical_info


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
