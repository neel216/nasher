#!/usr/bin/env python3
# coding: utf-8

'''
This file contains the functions to read and write data to a Google Spreadsheet
document

TODO: add ability to add multiple rows at once (more info in trello)
TODO: add parameters to functions?
'''

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If you modify this, delete the token.pickle file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1cU243sy8jJz91GATvx_TfjWqdklvTCkbnQKEqDF3T8I' # spreadsheet ID, taken directly from spreadsheet's URL (CURRENTLY UTILIZES A TEST SPREADSHEET)
RANGE_NAME = 'TMS Changes!A1:C1000' # name of the sheet in the document, range of the spreadsheet to read (CURRENTLY UTILIZES A TEST SPREADSHEET)

def load_sheet():
    '''
    Shows basic usage of the Sheets API to load a Google Spreadsheet document
    '''
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet
    
def read_sheet():
    '''
    Reads values from a Google Spreadsheet Document over the specified range
    '''
    sheet = load_sheet()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            print(row)

def add_rows(rows):
    '''
    Adds rows to the bottom of the Google Spreadsheet Document

    TODO: add ability to add multiple rows at once (more info in trello)
    '''
    sheet = load_sheet()
    value_input_option = 'RAW'
    
    values = rows
    body = {
        'values': values
    }
    
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption=value_input_option,
        body=body).execute()
    
    #print(f'{result.get("updates").get("updatedCells")} cells updated.')


if __name__ == '__main__':
    read_sheet()
    '''
    import time
    vals = []
    for i in range(100):
        start = time.time()
        add_row([1, 2, 3])
        end = time.time()
        vals.append(end - start)
    import statistics
    print(statistics.mean(vals))
    '''
    rows = [
        ['neel', 'derrick', 'cole'],
        [1, 2, 3]
    ]
    add_rows(rows)