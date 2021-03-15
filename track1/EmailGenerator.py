from __future__ import print_function
import os.path
from . import EmailDatabase
from . import EmailParser
# import base64
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# import import_ipynb
import sys
sys.path.append('../')
# from .. import track3.run_model as track3
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    # Query a list of all possible emails
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=5, includeSpamTrash=True).execute()
    messages = results.get('messages', [])
    count = 1
    success = 0
    db_handler = EmailDatabase.DatabaseHandler()
    parser = EmailParser.EmailParser()
    for message in messages:
        # print("\n- Working on message " + str(count) + "...")
        count += 1
        key = message.get('id')
        results = service.users().messages().get(userId='me', id=key, format='full').execute()
        msg = parser.read_message(results)
        # Upload to the database
        # print("- Information interpreted:")
        # print(msg)
        # print("- Uploading to database...")
        success += db_handler.insert(msg)
        # print("- Classifying usefulness")
        # print("- Is Useful?", track3.predict_usefulness(msg['body']))
        # print("..............")
        time.sleep(5)
    print("Messages stored: " + str(success))
    print("Proceeding to fetch from database to filter through emails...\n")
    return db_handler


def get_header(headers, name):
    for header in headers:
        if header.get('name') == name:
            return header.get('value')


if __name__ == '__main__':
    main()
