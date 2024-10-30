from __future__ import print_function
import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Upload the CSV file
    file_metadata = {'name': 'data.csv', 'parents': ['1l0cByx6fyTMzU1gk4PuZU6xcsSDxsYLH']}  
    media = MediaFileUpload('data.csv', mimetype='text/csv')
    file = service.files().create(body=file_metadata,
                                   media_body=media,
                                   fields='id').execute()
    print('File ID: %s' % file.get('id'))

if __name__ == '__main__':
    main()
