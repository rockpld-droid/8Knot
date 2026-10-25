import logging
import time

import cache_manager.cache_facade as cf
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from components.visualization import VisualizationAIO
from dash import callback
from dash.dependencies import Input, Output
from dateutil.relativedelta import *  # type: ignore
from pages.utils.graph_utils import baby_blue
from pages.utils.job_utils import nodata_graph
from queries.pr_response_query import pr_response_query as prr

PAGE = "contributions"
VIZ_ID = "pr-first-response"

gc_pr_first_response = VisualizationAIO(
    PAGE,
    VIZ_ID,
    title="Pull Request Time to First Response",
    graph_info="""
    Compares the volume of PRs being opened against the number of those PRs that \n
    receive at least one response within the parameterized timeframe after being opened.
    """,
    controls=[
        dbc.Label(
            "Response Days:",
            html_for=f"response-days-{PAGE}-{VIZ_ID}",
            width={"size": "auto"},
        ),
        dbc.Col(
            dbc.Input(
                id=f"response-days-{PAGE}-{VIZ_ID}",
                type="number",
                min=1,
                max=120,
                step=1,
                value=2,
                size="sm",
                style={"width": "80px"},
                className="dark-input",
            ),
            className="me-2",
            width=2,
        ),
    ],
    class_name="dark-card",
    id="pr-first-response",
)


# callback for pr first response graph
@callback(
    Output(f"{PAGE}-{VIZ_ID}", "figure"),
    [
        Input("repo-choices", "data"),
        Input(f"response-days-{PAGE}-{VIZ_ID}", "value"),
        Input("bot-switch", "value"),
    ],
    background=True,
)
def pr_first_response_graph(repolist, num_days, bot_switch):
    while cf.get_uncached(func_name=prr.__name__, repolist=repolist):
        logging.warning("PR_FIRST_RESPONSE - WAITING ON DATA TO BECOME AVAILABLE")
        time.sleep(0.5)

    start = time.perf_counter()
    logging.warning(f"{VIZ_ID}- START")

    # GET ALL DATA FROM POSTGRES CACHE
    df = cf.retrieve_from_cache(
        tablename=prr.__name__,
        repolist=repolist,
    )

    # test if there is data
    if df.empty:
        logging.warning(f"{VIZ_ID} - NO DATA AVAILABLE")
        return nodata_graph

    # remove bot data
    if bot_switch:
        df = df[~df["cntrb_id"].isin(app.bots_list)]

    df = process_data(df, num_days)

    fig = create_figure(df, num_days)

    logging.warning(f"{VIZ_ID} - END - {time.perf_counter() - start}")
    return fig


def process_data(df: pd.DataFrame, num_days):
    # convert to datetime objects rather than strings
    df["msg_timestamp"] = pd.to_datetime(df["msg_timestamp"], utc=True)
    df["pr_created_at"] = pd.to_datetime(df["pr_created_at"], utc=True)
    df["pr_closed_at"] = pd.to_datetime(df["pr_closed_at"], utc=True)

    # drop messages from the pr creator
    df = df[df["cntrb_id"] != df["msg_cntrb_id"]]

    # sort in ascending earlier and only get ealiest value
    df = df.sort_values(by="msg_timestamp", axis=0, ascending=True)
    df = df.drop_duplicates(subset="pull_request_id", keep="first")

    # first and last elements of the dataframe are the
    # earliest and latest events respectively
    earliest = df["pr_created_at"].min()
    latest = max(df["pr_created_at"].max(), df["pr_closed_at"].max())

    # beginning to the end of time by the specified interval
    dates = pd.date_range(start=earliest, end=latest, freq="D", inclusive="both")

    # df for open prs and responded to prs in time interval
    df_pr_responses = dates.to_frame(index=False, name="Date")

    # every day, count the number of PRs that are open on that day and the number of
    # those that were responded to within num_days of their opening
    # Optimization: Vectorized calculation using np.searchsorted
    # Instead of O(N*D) dataframe filtering in a loop, we sort the dates and use binary search
    # open_count = (created <= date) - (closed <= date)
    df["responded_in_time"] = df["msg_timestamp"] < (
        df["pr_created_at"] + pd.DateOffset(days=num_days)
    )

    created_counts = np.searchsorted(
        np.sort(df["pr_created_at"].values), dates.values, side="right"
    )
    closed_counts = np.searchsorted(
        np.sort(df["pr_closed_at"].dropna().values), dates.values, side="right"
    )
    df_pr_responses["Open"] = created_counts - closed_counts

    df_responded = df[df["responded_in_time"]]
    resp_created_counts = np.searchsorted(
        np.sort(df_responded["pr_created_at"].values), dates.values, side="right"
    )
    resp_closed_counts = np.searchsorted(
        np.sort(df_responded["pr_closed_at"].dropna().values),
        dates.values,
        side="right",
    )
    df_pr_responses["Response"] = resp_created_counts - resp_closed_counts

    df_pr_responses["Date"] = df_pr_responses["Date"].dt.strftime("%Y-%m-%d")

    return df_pr_responses


def create_figure(df: pd.DataFrame, num_days):
    fig = go.Figure(
        [
            go.Scatter(
                name="Prs Open",
                x=df["Date"],
                y=df["Open"],
                mode="lines",
                showlegend=True,
                hovertemplate="PR's Open: %{y}<br>%{x|%b %d, %Y} <extra></extra>",
                marker={"color": baby_blue[8]},
            ),
            go.Scatter(
                name="Response <" + str(num_days) + " days",
                x=df["Date"],
                y=df["Response"],
                mode="lines",
                showlegend=True,
                hovertemplate="PRs: %{y}<br>%{x|%b %d, %Y} <extra></extra>",
                marker={"color": baby_blue[2]},
            ),
        ]
    )
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Number of PRs",
        font={"size": 14},
    )

    return fig
