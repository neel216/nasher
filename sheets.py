#!/usr/bin/env python3
# coding: utf-8

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Sheet:
    def __init__(self, spreadsheet_id, spreadsheet_range):
        '''
        Constructs a Sheet object.

        :param spreadsheet_id: the ID of the spreadsheet taken directly from the document's URL
        :type spreadsheet_id: str
        :param spreadsheet_range: the range of the spreadsheet to read (SheetName!topLeftCell:bottomRightCell))
        :type spreadsheet_range: str
        :return: returns nothing
        '''
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.id = spreadsheet_id
        self.value_input_option = 'RAW'
        self.range = spreadsheet_range

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
        self.sheet = service.spreadsheets()

    def read_sheet(self):
        '''
        Reads values from the Google Spreadsheet Document over the specified range

        :return: a nested list where each list is a row and each entry in the list is a cell
        :rtype: list 
        '''
        result = self.sheet.values().get(spreadsheetId=self.id, range=self.range).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            for row in values:
                print(row)
        
        return values

    def add_rows(self, rows):
        '''
        Appends rows to the Google Spreadsheet Document

        :param rows: a nested list containing the rows to append to the spreadsheet
        :type rows: list
        :return: returns nothing
        '''
        body = {
            'values': rows
        }
        
        result = self.sheet.values().append(
            spreadsheetId=self.id,
            range=self.range,
            valueInputOption=self.value_input_option,
            body=body).execute()
        
        print(f'{result.get("updates").get("updatedCells")} cells updated.')


if __name__ == '__main__':
    sheet = Sheet('1cU243sy8jJz91GATvx_TfjWqdklvTCkbnQKEqDF3T8I', 'TMS Changes!A1:C1000')

    sheet.read_sheet()

    rows = [
        [1, 2, 3],
        [3, 4, 5],
        [6, 7, 8]
    ]
    sheet.add_rows(rows)