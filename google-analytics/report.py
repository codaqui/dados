import asyncio
import os
import pandas as pd
import json
from google.analytics.data_v1beta import BetaAnalyticsDataAsyncClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

PROPERTY_ID = 337372858

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-analytics\service_account.json'

client = BetaAnalyticsDataAsyncClient()

async def sample_run_report(property_id = PROPERTY_ID):
    client = BetaAnalyticsDataAsyncClient()
  
    # Request for page-specific data
    page_request = RunReportRequest(
        property= f"properties/{PROPERTY_ID}",
        dimensions=[
            Dimension(name='pagePathPlusQueryString'),
            ],
        metrics=[
            Metric(name='activeUsers'),
            Metric(name='screenPageViews'),
            Metric(name='screenPageViewsPerSession'),
            Metric(name='screenPageViewsPerUser'),
            Metric(name='averageSessionDuration'),
            Metric(name='bounceRate'),
        ],
        date_ranges=[DateRange(start_date="2020-01-01", end_date="today")],
    )

    # Request for website-wide data
    website_request = RunReportRequest(
        property= f"properties/{PROPERTY_ID}",
        metrics=[
            Metric(name='activeUsers'),
            Metric(name='screenPageViews'),
            Metric(name='averageSessionDuration'),
            Metric(name='bounceRate'),
            Metric(name='sessions'),
        ],
        date_ranges=[DateRange(start_date="2020-01-01", end_date="today")],
    )

    # Request for website-wide data with dimensions
    website_dimensions_request = RunReportRequest(
        property= f"properties/{PROPERTY_ID}",
        dimensions=[
            Dimension(name='newVsReturning'),
            Dimension(name='sessionSource'),
            ],
        metrics=[Metric(name='sessions')],
        date_ranges=[DateRange(start_date="2020-01-01", end_date="today")],
    )


    page_response = await client.run_report(page_request)
    website_response = await client.run_report(website_request)
    website_dimensions_response = await client.run_report(website_dimensions_request)

    print("Report result:")
    pages_info = []
    for row in page_response.rows:
        page_path = row.dimension_values[0].value
        active_users = row.metric_values[0].value
        screen_page_views = row.metric_values[1].value
        screen_page_views_session = row.metric_values[2].value
        screen_page_views_user = row.metric_values[3].value
        avg_session_duration = row.metric_values[4].value
        bounce_rate = row.metric_values[5].value
      
        if page_path != "/":
            pages_info.append({
                "pagePath": page_path,
                "activeUsers": active_users,
                "screenPageViews": screen_page_views,
                "screenPageViewsPerSession": screen_page_views_session,
                "screenPageViewPerUser": screen_page_views_user,
                "averageSessionDuration": avg_session_duration,
                "bounceRate": bounce_rate,
            })
  
    with open("data/pages_info.json", "w") as f:
        f.write(json.dumps(pages_info, indent = 4))

    website_info = []
    for row in website_response.rows:
        active_users = row.metric_values[0].value
        screen_page_views = row.metric_values[1].value
        avg_session_duration = row.metric_values[2].value
        bounce_rate = row.metric_values[3].value
        sessions = row.metric_values[4].value

        website_info.append({
            "activeUsers": active_users,
            "screenPageViews": screen_page_views,
            "averageSessionDuration": avg_session_duration,
            "bounceRate": bounce_rate,
            "sessions": sessions
        })

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

    with open("data/website_info.json", "w") as f:
        f.write(json.dumps(website_info, indent = 4))

    with open("data/website_dimensions_info.json", "w") as f:
        f.write(json.dumps(website_dimensions_info, indent = 4))
    

# Run the async function
asyncio.run(sample_run_report())