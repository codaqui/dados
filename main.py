"""
Codaqui Analytics Extract Data
"""

import asyncio
import json
import os
import sys
import logging
from datetime import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataAsyncClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)


async def sample_run_report(
    property_id: int, start_date: str, end_date: str, folder: str
):
    logging.info("Start report. Dates: %s - %s", start_date, end_date)
    client = BetaAnalyticsDataAsyncClient()

    # Request for page-specific data
    logging.info("Requesting page-specific data")
    page_request = RunReportRequest(
        property=f"properties/{str(property_id)}",
        dimensions=[
            Dimension(name="pagePath"),
            Dimension(name="year"),
            Dimension(name="month"),
        ],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="screenPageViews"),
            Metric(name="screenPageViewsPerSession"),
            Metric(name="screenPageViewsPerUser"),
            Metric(name="averageSessionDuration"),
            Metric(name="bounceRate"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )

    # Request for website-wide data
    logging.info("Requesting website-wide data")
    website_request = RunReportRequest(
        property=f"properties/{str(property_id)}",
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="screenPageViews"),
            Metric(name="averageSessionDuration"),
            Metric(name="bounceRate"),
            Metric(name="sessions"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )

    # Request for website-wide data with dimensions
    logging.info("Requesting website-wide data with dimensions")
    website_dimensions_request = RunReportRequest(
        property=f"properties/{str(property_id)}",
        dimensions=[
            Dimension(name="newVsReturning"),
            Dimension(name="sessionSource"),
        ],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )

    page_response = await client.run_report(page_request)
    website_response = await client.run_report(website_request)
    website_dimensions_response = await client.run_report(website_dimensions_request)

    pages_info = []
    for row in page_response.rows:
        page_path = row.dimension_values[0].value
        year = row.dimension_values[1].value
        month = row.dimension_values[2].value
        active_users = row.metric_values[0].value
        screen_page_views = row.metric_values[1].value
        screen_page_views_session = row.metric_values[2].value
        screen_page_views_user = row.metric_values[3].value
        avg_session_duration = row.metric_values[4].value
        bounce_rate = row.metric_values[5].value

        if page_path != "/":
            pages_info.append(
                {
                    "pagePath": page_path,
                    "year": year,
                    "month": month,
                    "activeUsers": active_users,
                    "screenPageViews": screen_page_views,
                    "screenPageViewsPerSession": screen_page_views_session,
                    "screenPageViewPerUser": screen_page_views_user,
                    "averageSessionDuration": avg_session_duration,
                    "bounceRate": bounce_rate,
                }
            )

    logging.info("Saving data to file")
    with open(f"{folder}/pages_info.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(pages_info, indent=4))

    website_info = []
    for row in website_response.rows:
        active_users = row.metric_values[0].value
        screen_page_views = row.metric_values[1].value
        avg_session_duration = row.metric_values[2].value
        bounce_rate = row.metric_values[3].value
        sessions = row.metric_values[4].value

        website_info.append(
            {
                "activeUsers": active_users,
                "screenPageViews": screen_page_views,
                "averageSessionDuration": avg_session_duration,
                "bounceRate": bounce_rate,
                "sessions": sessions,
            }
        )

    website_dimensions_info = {}
    for row in website_dimensions_response.rows:
        new_vs_returning = row.dimension_values[0].value
        session_source = row.dimension_values[1].value
        sessions = int(row.metric_values[0].value)

        # Aggregate sessions by newVsReturning and sessionSource
        if new_vs_returning not in website_dimensions_info:
            website_dimensions_info[new_vs_returning] = sessions
        else:
            website_dimensions_info[new_vs_returning] += sessions

        if session_source not in website_dimensions_info:
            website_dimensions_info[session_source] = sessions
        else:
            website_dimensions_info[session_source] += sessions

    with open(f"{folder}/website_info.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(website_info, indent=4))

    with open(f"{folder}/website_dimensions_info.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(website_dimensions_info, indent=4))


# Main
# Example: python main.py property_id start_date end_date
# Example: python main.py 337372858 01-01-2024 31-01-2024
# Date format: DD-MM-YYYY

# Validate args
if len(sys.argv) != 4:
    raise ValueError(
        "Invalid arguments, use example: python main.py property_id start_date end_date"
    )

# Retrieve args
property_id_arg: int = int(sys.argv[1])
start_date_arg: str = sys.argv[2]
end_date_arg: str = sys.argv[3]

# Convert date format
start_date_arg = datetime.strptime(start_date_arg, "%d-%m-%Y").strftime("%Y-%m-%d")
end_date_arg = datetime.strptime(end_date_arg, "%d-%m-%Y").strftime("%Y-%m-%d")

# Set service account
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# Config logger to Console
logging.basicConfig(level=logging.INFO)

# Create a folder to save the data
os.makedirs("data", exist_ok=True)

# Create a month folder to save the data
month_folder = datetime.strptime(start_date_arg, "%Y-%m-%d").strftime("%Y-%m")
os.makedirs(f"data/{month_folder}", exist_ok=True)
folder_path = f"data/{month_folder}"

# Call the function
asyncio.run(
    sample_run_report(
        property_id=property_id_arg,
        start_date=start_date_arg,
        end_date=end_date_arg,
        folder=folder_path,
    )
)
