#!/usr/bin/env python3
# coding: utf-8

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
from httplib2 import ServerNotFoundError


class Sheet:
    def __init__(self, spreadsheet_id, spreadsheet_range1, spreadsheet_range2, value_input_option='RAW'):
        '''
        Constructs a Sheet object.

        :param spreadsheet_id: the ID of the spreadsheet taken directly from the document's URL
        :param spreadsheet_range1: the range of the spreadsheet to read (SheetName!topLeftCell:bottomRightCell))
        :param spreadsheet_range2: another range of the spreadsheet to read (SheetName!topLeftCell:bottomRightCell))
        :param value_input_option: the way to modify cell entries into the spreadsheet
        :return: returns nothing
        '''
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.id = spreadsheet_id
        self.value_input_option = value_input_option
        self.range1 = spreadsheet_range1
        self.range2 = spreadsheet_range2

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
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        try:
            service = build('sheets', 'v4', credentials=creds)
            self.wifi = True
        except ServerNotFoundError:
            self.wifi = False
            print('No Wifi Network Found. Google Sheets API not syncing TMS Changes.')

        # Call the Sheets API
        if self.wifi:
            self.sheet = service.spreadsheets()

    def read_sheet(self):
        '''
        Reads values from the Google Spreadsheet Document over the specified range

        :return: a nested list where each list is a row and each entry in the list is a cell
        '''
        if self.wifi:
            # Get values from spreadsheet
            result = self.sheet.values().get(spreadsheetId=self.id, range=self.range1).execute()
            values = result.get('values', [])

            # Print rows if data was found in spreadsheet
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
        :return: returns nothing
        '''
        if self.wifi:
            # Adds times in isoformat as first element in each row
            for i in rows:
                i.insert(0, datetime.now().isoformat())

            body = {
                'values': rows
            }
            
            # Adds data to changes spreadsheet
            result1 = self.sheet.values().append(
                spreadsheetId=self.id,
                range=self.range1,
                valueInputOption=self.value_input_option,
                body=body).execute()
            
            # Adds data to history spreadsheet
            result2 = self.sheet.values().append(
                spreadsheetId=self.id,
                range=self.range2,
                valueInputOption=self.value_input_option,
                body=body).execute()
            
            # Print status update
            print(f'{result1.get("updates").get("updatedCells")} cells updated in changes spreadsheet.')
            print(f'{result2.get("updates").get("updatedCells")} cells updated in history spreadsheet.')

            return True


if __name__ == '__main__':
    sheet = Sheet('1cU243sy8jJz91GATvx_TfjWqdklvTCkbnQKEqDF3T8I', 'TMS Changes!A1:C', 'History Logger!A1:C')

    sheet.read_sheet()

    rows = [
        [1, 2, 3],
        [3, 4, 5],
        [6, 7, 8]
    ]
    sheet.add_rows(rows)