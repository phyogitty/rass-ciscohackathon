from __future__ import print_function
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import time
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

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    message_count = int(input("How many messages do you want to see?"))
    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages[:message_count]:
            key = message.get('id')
            result = service.users().messages().get(userId='me', id=key).execute()
            msg = dict()
            msg['labelIds'] = result.get('labelIds')
            payload = result.get('payload')

            if payload != None:
                headers = payload.get('headers', [])
                msg['from'] = get_header(headers, 'From')
                msg['to'] = get_header(headers, 'To')
                msg['date'] = get_header(headers, 'Date')
                msg['subject'] = get_header(headers, 'Subject')

                encoded_body_text = result.get('payload').get('parts')[0].get('body').get('data')
                if encoded_body_text != None:
                    msg['body'] = base64.b64decode(encoded_body_text)
                else:
                    msg['body'] = "Text could not be read"

        for k in msg:
            print(k, " is ", msg[k])
            print("---------")
            time.sleep(2)

def get_header(headers, name):
    for header in headers:
        if header.get('name') == name:
            return header.get('value')

if __name__ == '__main__':
    main()
