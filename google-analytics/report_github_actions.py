import asyncio
import pandas as pd
# Google Analytics GA4 API
from google.oauth2.service_account import Credentials
#from google.auth.credentials import AnonymousCredentials
from google.analytics.data_v1beta import BetaAnalyticsDataAsyncClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
# Google Drive API
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
# Getting the date for prepation to Github Actions
from datetime import datetime
from dateutil.relativedelta import relativedelta
# OS to find files, but now also to get environment variables from github repository
import os
import json
# Convert back the TOKEN.PICKLE and load it
import base64
import io

# Get environment variables
service_account_credentials = os.getenv('SERVICE_ACCOUNT_CREDENTIALS')
property_id = os.getenv('PROPERTY_ID')
token_pickle_base64 = os.getenv('TOKEN_PICKLE')
oauth_credentials = os.getenv('OAUTH_CREDENTIALS')

# Convert credentials and token from JSON and base64 to Python objects
service_account_credentials = json.loads(service_account_credentials)
oauth_credentials = json.loads(oauth_credentials)
token_pickle = base64.b64decode(token_pickle_base64)
token = pickle.loads(token_pickle)
#token = pickle.loads(io.BytesIO(token_pickle))

# Get the date of the last month
now = datetime.now()
LAST_MONTH = (now.replace(day=1) - relativedelta(days=1)).strftime('%Y-%m-%d')

# Set up constants
PROPERTY_ID = property_id
CREDENTIALS_FILE = oauth_credentials
TOKEN_FILE = token
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Set up Google Analytics client
credentials = Credentials.from_service_account_info(service_account_credentials)
#credentials = AnonymousCredentials.from_service_account_info(service_account_credentials)
client = BetaAnalyticsDataAsyncClient(credentials=credentials)

async def sample_run_report(property_id = PROPERTY_ID):
    
    credentials = Credentials.from_service_account_info(service_account_credentials)
    client = BetaAnalyticsDataAsyncClient(credentials=credentials)
  
    # Request for page-specific data
    page_request = RunReportRequest(
        property= f"properties/{PROPERTY_ID}",
        dimensions=[
            Dimension(name='pagePath'),
            Dimension(name='year'),
            Dimension(name='month'),
            ],
        metrics=[
            Metric(name='activeUsers'),
            Metric(name='screenPageViews'),
            Metric(name='screenPageViewsPerSession'),
            Metric(name='screenPageViewsPerUser'),
            Metric(name='averageSessionDuration'),
            Metric(name='bounceRate'),
        ],
        date_ranges=[DateRange(start_date="2020-01-01", end_date=LAST_MONTH)],
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


    # Run requests and get responses
    page_response = await client.run_report(page_request)
    website_response = await client.run_report(website_request)
    website_dimensions_response = await client.run_report(website_dimensions_request)

    # Process responses and save data
    print("Report result:")
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
            pages_info.append({
                "pagePath": page_path,
                "year": year,
                "month": month,
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
    
    # Request for earliest recorded data
    earliest_data_request = RunReportRequest(
        property= f"properties/{PROPERTY_ID}",
        dimensions=[
            Dimension(name='date'),
            ],
        metrics=[Metric(name='sessions')],  # Placeholder metric
        date_ranges=[DateRange(start_date="2020-01-01", end_date="today")],  # Large date range
)
    earliest_data_response = await client.run_report(earliest_data_request)
    # Get the earliest date from the first row
    earliest_date = earliest_data_response.rows[0].dimension_values[0].value
    print(f"Data started being recorded on {earliest_date}")

# Run the async function
asyncio.run(sample_run_report())

# Function to upload a file to Google Drive
def upload_file_to_drive(filename, mimetype, title, folder_name, TOKEN_FILE):

    # Load the credentials from the token
    creds = pickle.loads(base64.b64decode(TOKEN_FILE))

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    TOKEN_FILE = base64.b64encode(pickle.dumps(creds)).decode('utf-8')

    # Build the Drive service
    drive_service = build('drive', 'v3', credentials=creds)

    # Search for the folder
    response = drive_service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
        spaces='drive',
        fields='files(id, name)').execute()
    folders = response.get('files', [])

    # If the folder exists, use it. If not, create it.
    if not folders:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        print(f'Folder ID: {folder.get("id")}')
    else:
        folder = folders[0]
        print(f'Folder ID: {folder.get("id")} (existing folder)')

    # Search for the file in the folder
    response = drive_service.files().list(
        q=f"name='{title}' and '{folder.get('id')}' in parents",
        spaces='drive',
        fields='files(id, name)').execute()
    files = response.get('files', [])

    # If the file exists, update it. If not, create it.
    if files:
        file = files[0]
        # Update the file
        media = MediaFileUpload(filename, mimetype=mimetype, resumable=True)
        updated_file = drive_service.files().update(
            fileId=file.get('id'),
            media_body=media).execute()
        print(f'File ID: {updated_file.get("id")} (updated file)')
    else:
        # Create the file
        file_metadata = {
            'name': title,
            'parents': [folder.get('id')]
        }
        media = MediaFileUpload(filename, mimetype=mimetype)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'File ID: {file.get("id")} (new file)')

# Upload the file to Google Drive
upload_file_to_drive("data/pages_info.json", "application/json", "pages_info.json", "Dados-Codaqui", TOKEN_FILE)